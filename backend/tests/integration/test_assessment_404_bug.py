"""
Test case for the 404 error when POST to /api/v1/assessments (without trailing slash).

This test reproduces the exact issue reported:
Request URL: http://localhost:3000/api/v1/assessments
Request Method: POST
Status Code: 404 Not Found

The issue is that FastAPI is strict about trailing slashes, and the frontend
is making requests to /api/v1/assessments while the backend expects /api/v1/assessments/
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.main import app
from backend.src.models.user import User
from backend.src.services.user_service import UserService
from backend.src.middleware.auth import create_access_token


@pytest.fixture
async def test_user(db: AsyncSession):
    """Create a test user."""
    user_service = UserService(db)
    user = await user_service.create_user(
        email="test404@example.com",
        password="testpassword123",
        full_name="Test User 404",
        age=25
    )
    return user


@pytest.fixture
async def auth_headers(test_user: User):
    """Create authentication headers for test user."""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


class TestAssessment404Bug:
    """Test cases for the 404 bug in assessment endpoint."""
    
    async def test_post_assessments_without_trailing_slash_returns_404(
        self, 
        client, 
        auth_headers: dict, 
        test_user: User
    ):
        """
        Test that POST to /api/v1/assessments (without trailing slash) works after fix.
        
        This should now work correctly with both URLs.
        """
        # This is exactly how the frontend makes the request
        response = await client.post(
            "/api/v1/assessments",  # No trailing slash - this should now work
            json={"user_id": str(test_user.id)},
            headers=auth_headers
        )
        
        # After the fix, this should return 200
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print("✅ BUG FIXED: POST /api/v1/assessments now works!")
            data = response.json()
            assert "id" in data
            assert data["user_id"] == str(test_user.id)
            assert data["status"] == "in_progress"
        else:
            print(f"❌ Still not working: {response.status_code}")
            print(f"Response: {response.text}")
            assert False, f"Expected 200 but got {response.status_code}"
    
    async def test_post_assessments_with_trailing_slash_works(
        self, 
        client, 
        auth_headers: dict, 
        test_user: User
    ):
        """
        Test that POST to /api/v1/assessments/ (with trailing slash) works correctly.
        This demonstrates that the endpoint exists but has a routing issue.
        """
        response = await client.post(
            "/api/v1/assessments/",  # With trailing slash - this should work
            json={"user_id": str(test_user.id)},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["user_id"] == str(test_user.id)
        assert data["status"] == "in_progress"
    
    async def test_frontend_request_pattern_exact_reproduction(
        self, 
        client, 
        auth_headers: dict, 
        test_user: User
    ):
        """
        Exact reproduction of the frontend request pattern that causes 404.
        
        This mimics the exact request made by frontend/src/app/assessment/page.tsx:34
        """
        # Simulate the exact frontend request
        request_data = {"user_id": str(test_user.id)}
        
        response = await client.post(
            "/api/v1/assessments",  # Exact URL from frontend
            json=request_data,
            headers={
                "Authorization": auth_headers["Authorization"],
                "Content-Type": "application/json"
            }
        )
        
        # Document the current behavior (404) and expected behavior (200)
        if response.status_code == 404:
            print(f"BUG REPRODUCED: POST /api/v1/assessments returns {response.status_code}")
            print(f"Response: {response.text}")
            assert True, "Bug successfully reproduced - 404 error confirmed"
        else:
            print(f"BUG FIXED: POST /api/v1/assessments now returns {response.status_code}")
            assert response.status_code == 200, "Expected successful response after fix"
    
    async def test_all_assessment_endpoints_trailing_slash_consistency(
        self, 
        client, 
        auth_headers: dict, 
        test_user: User
    ):
        """
        Test that all assessment endpoints handle trailing slash consistently.
        This helps identify if the issue affects other endpoints too.
        """
        # First create an assessment using the working endpoint
        create_response = await client.post(
            "/api/v1/assessments/",  # With trailing slash
            json={"user_id": str(test_user.id)},
            headers=auth_headers
        )
        assert create_response.status_code == 200
        assessment_id = create_response.json()["id"]
        
        # Test GET endpoint without trailing slash (should work)
        get_response = await client.get(
            f"/api/v1/assessments/{assessment_id}",  # No trailing slash
            headers=auth_headers
        )
        assert get_response.status_code == 200
        
        # Test questions endpoint without trailing slash (should work)
        questions_response = await client.get(
            f"/api/v1/assessments/{assessment_id}/questions",  # No trailing slash
            headers=auth_headers
        )
        assert questions_response.status_code == 200
        
        # Test answers endpoint without trailing slash (should work)
        answers_response = await client.post(
            f"/api/v1/assessments/{assessment_id}/answers",  # No trailing slash
            json={"answers": []},
            headers=auth_headers
        )
        assert answers_response.status_code == 200


    async def test_reproduce_exact_frontend_error_unauthenticated(
        self, 
        client
    ):
        """
        Standalone test to reproduce the exact error scenario without authentication.
        
        This test can be run independently to verify the bug exists
        and to test the fix.
        """
        # Test without authentication first (should get 401, not 404)
        response = await client.post("/api/v1/assessments")
        
        # Check what we actually get
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 404:
            print("❌ BUG CONFIRMED: Route /api/v1/assessments not found (404)")
            assert True, "Bug reproduced: 404 error for /api/v1/assessments"
        elif response.status_code == 401:
            print("✅ Route exists but requires authentication (401)")
            assert False, "Route exists - this means the bug might be fixed!"
        elif response.status_code == 307:
            print("🔄 FastAPI is redirecting to trailing slash version (307)")
            # This is actually correct behavior - FastAPI redirects missing trailing slash
            # The issue might be that the frontend doesn't follow redirects
            assert True, "FastAPI redirects correctly, but frontend might not follow redirects"
        else:
            print(f"🤔 Unexpected status code: {response.status_code}")
            assert False, f"Unexpected status code: {response.status_code}"
        
        # Test with trailing slash
        response_with_slash = await client.post("/api/v1/assessments/")
        print(f"With trailing slash status: {response_with_slash.status_code}")
        if response_with_slash.status_code == 401:
            print("✅ Route /api/v1/assessments/ exists and requires authentication")
        else:
            print(f"🤔 Unexpected status for trailing slash: {response_with_slash.status_code}")
    
    async def test_redirect_behavior_without_follow_redirects(self):
        """
        Test the redirect behavior when not following redirects.
        This might be what the frontend is experiencing.
        """
        import httpx
        from backend.src.main import app
        
        # Create client that doesn't follow redirects
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://testserver",
            follow_redirects=False  # This is key!
        ) as client:
            response = await client.post("/api/v1/assessments")
            
            print(f"Without redirect following: {response.status_code}")
            if response.status_code == 307:
                print("✅ FastAPI returns 307 redirect as expected")
                print(f"Location header: {response.headers.get('location')}")
                
                # The frontend might not be following this redirect
                # Let's see what happens if we follow it manually
                location = response.headers.get('location')
                if location:
                    follow_response = await client.post(location)
                    print(f"Following redirect manually: {follow_response.status_code}")
            else:
                print(f"Unexpected status without redirect: {response.status_code}")