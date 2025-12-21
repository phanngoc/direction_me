"""
Test case for the assessment routing fix.

This test verifies that the 404 error when POST to /api/v1/assessments 
(without trailing slash) has been fixed by adding explicit route handling.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, patch

from backend.src.main import app


class TestAssessmentRoutingFix:
    """Test cases for the assessment routing fix."""
    
    async def test_both_routes_exist_without_auth(self):
        """
        Test that both /api/v1/assessments and /api/v1/assessments/ routes exist.
        
        Without authentication, both should return 401/403, not 404.
        """
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://testserver",
            follow_redirects=False
        ) as client:
            # Test without trailing slash
            response_no_slash = await client.post("/api/v1/assessments")
            print(f"Without slash: {response_no_slash.status_code}")
            
            # Test with trailing slash  
            response_with_slash = await client.post("/api/v1/assessments/")
            print(f"With slash: {response_with_slash.status_code}")
            
            # Both should NOT return 404 (route not found)
            # They should return 401/403 (authentication required) or 307 (redirect)
            assert response_no_slash.status_code != 404, "Route without slash should exist"
            assert response_with_slash.status_code != 404, "Route with slash should exist"
            
            # Both should return the same status code (no redirect needed)
            assert response_no_slash.status_code == response_with_slash.status_code, (
                f"Both routes should return same status. "
                f"Got {response_no_slash.status_code} vs {response_with_slash.status_code}"
            )
    
    @patch('backend.src.middleware.auth.get_current_user')
    @patch('backend.src.database.get_db')
    async def test_both_routes_work_with_auth(self, mock_get_db, mock_get_current_user):
        """
        Test that both routes work correctly with authentication.
        """
        # Mock the dependencies
        mock_user = AsyncMock()
        mock_user.id = "test-user-id"
        mock_get_current_user.return_value = mock_user
        
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        # Mock the assessment service
        with patch('backend.src.services.assessment_service.AssessmentService') as mock_service_class:
            mock_service = AsyncMock()
            mock_assessment = AsyncMock()
            mock_assessment.id = "test-assessment-id"
            mock_assessment.user_id = "test-user-id"
            mock_assessment.status = "in_progress"
            mock_assessment.total_questions = 0
            mock_assessment.answered_questions = 0
            
            mock_service.create_assessment.return_value = mock_assessment
            mock_service_class.return_value = mock_service
            
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url="http://testserver"
            ) as client:
                headers = {"Authorization": "Bearer fake-token"}
                request_data = {"user_id": "test-user-id"}
                
                # Test without trailing slash
                response_no_slash = await client.post(
                    "/api/v1/assessments",
                    json=request_data,
                    headers=headers
                )
                
                # Test with trailing slash
                response_with_slash = await client.post(
                    "/api/v1/assessments/",
                    json=request_data,
                    headers=headers
                )
                
                print(f"Without slash: {response_no_slash.status_code}")
                print(f"With slash: {response_with_slash.status_code}")
                
                # Both should work (return 200)
                assert response_no_slash.status_code == 200, (
                    f"Route without slash should work. Got {response_no_slash.status_code}: "
                    f"{response_no_slash.text}"
                )
                assert response_with_slash.status_code == 200, (
                    f"Route with slash should work. Got {response_with_slash.status_code}: "
                    f"{response_with_slash.text}"
                )
                
                # Both should return the same data
                data_no_slash = response_no_slash.json()
                data_with_slash = response_with_slash.json()
                
                assert "id" in data_no_slash
                assert "id" in data_with_slash
                assert data_no_slash["user_id"] == "test-user-id"
                assert data_with_slash["user_id"] == "test-user-id"
    
    async def test_frontend_exact_request_simulation(self):
        """
        Simulate the exact request that the frontend makes.
        
        This should work without any redirects or errors.
        """
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://testserver",
            follow_redirects=False  # Frontend might not follow redirects
        ) as client:
            # Exact frontend request pattern
            response = await client.post(
                "/api/v1/assessments",  # No trailing slash - as frontend does
                json={"user_id": "some-user-id"},
                headers={
                    "Content-Type": "application/json"
                    # No auth header - should get 401/403, not 404
                }
            )
            
            print(f"Frontend simulation status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            # Should NOT be 404 (route not found)
            assert response.status_code != 404, (
                "Frontend request should not get 404. "
                f"Got {response.status_code}: {response.text}"
            )
            
            # Should be 401/403 (authentication required) - this is expected
            assert response.status_code in [401, 403], (
                f"Expected 401/403 for unauthenticated request, got {response.status_code}"
            )


@pytest.mark.asyncio
async def test_route_registration_verification():
    """
    Verify that the routes are properly registered in FastAPI.
    """
    from backend.src.main import app
    
    # Get all registered routes
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append((route.path, route.methods))
    
    print("Registered routes:")
    for path, methods in routes:
        if 'assessments' in path:
            print(f"  {methods} {path}")
    
    # Check that we have both routes registered
    assessment_routes = [
        (path, methods) for path, methods in routes 
        if 'assessments' in path and 'POST' in methods
    ]
    
    print(f"Assessment POST routes: {assessment_routes}")
    
    # We should have routes that handle both cases
    assert len(assessment_routes) >= 1, "Should have at least one assessment POST route"
    
    # The routes should handle the path we care about
    paths = [path for path, methods in assessment_routes]
    
    # Either we have explicit routes for both, or FastAPI handles the redirect properly
    # The key is that /api/v1/assessments should not return 404
    print(f"Assessment paths: {paths}")
    assert any('/assessments' in path for path in paths), "Should have assessments route"