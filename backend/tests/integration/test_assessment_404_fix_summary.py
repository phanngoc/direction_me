"""
Summary test for the assessment 404 bug fix.

ISSUE: Frontend POST requests to /api/v1/assessments were returning 404 Not Found
CAUSE: FastAPI router only had @router.post("/") which becomes /api/v1/assessments/ (with trailing slash)
       Frontend was requesting /api/v1/assessments (without trailing slash)
       
SOLUTION: Added explicit route @router.post("") to handle requests without trailing slash
          Now both /api/v1/assessments and /api/v1/assessments/ work correctly

This test verifies the fix is working and documents the solution.
"""
import pytest
import httpx
from backend.src.main import app


class TestAssessment404BugFix:
    """Test that verifies the 404 bug has been fixed."""
    
    async def test_bug_is_fixed_both_routes_work(self):
        """
        MAIN TEST: Verify that both URL patterns work correctly.
        
        Before fix: POST /api/v1/assessments → 404 Not Found
        After fix:  POST /api/v1/assessments → 401/403 (route exists, needs auth)
        """
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://testserver",
            follow_redirects=False
        ) as client:
            
            # Test the problematic URL (without trailing slash)
            response_no_slash = await client.post("/api/v1/assessments")
            
            # Test the working URL (with trailing slash)  
            response_with_slash = await client.post("/api/v1/assessments/")
            
            print(f"❌ BEFORE FIX: POST /api/v1/assessments would return 404")
            print(f"✅ AFTER FIX:  POST /api/v1/assessments returns {response_no_slash.status_code}")
            print(f"✅ REFERENCE:  POST /api/v1/assessments/ returns {response_with_slash.status_code}")
            
            # CRITICAL: Both should NOT return 404 (route not found)
            assert response_no_slash.status_code != 404, (
                "❌ BUG NOT FIXED: /api/v1/assessments still returns 404. "
                "The route should exist and return 401/403 for authentication errors."
            )
            
            assert response_with_slash.status_code != 404, (
                "❌ REGRESSION: /api/v1/assessments/ should still work"
            )
            
            # Both should return the same status (both routes work identically)
            assert response_no_slash.status_code == response_with_slash.status_code, (
                f"Both routes should behave identically. "
                f"Got {response_no_slash.status_code} vs {response_with_slash.status_code}"
            )
            
            # Should be authentication error (401/403), not route error (404)
            assert response_no_slash.status_code in [401, 403], (
                f"Expected authentication error (401/403), got {response_no_slash.status_code}. "
                f"This indicates the route exists and is working correctly."
            )
            
            print("✅ BUG FIXED: Both /api/v1/assessments and /api/v1/assessments/ work correctly!")
    
    async def test_frontend_request_pattern_now_works(self):
        """
        Test the exact request pattern that was failing in the frontend.
        
        This simulates the frontend code:
        fetch('/api/v1/assessments', { method: 'POST', ... })
        """
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://testserver"
        ) as client:
            
            # Exact frontend request pattern
            response = await client.post(
                "/api/v1/assessments",  # No trailing slash - this was the problem
                json={"user_id": "test-user-id"},
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Frontend request simulation: {response.status_code}")
            
            # Should NOT be 404 anymore
            assert response.status_code != 404, (
                f"Frontend request should not get 404. Got {response.status_code}. "
                f"Response: {response.text}"
            )
            
            # Should be authentication error since we didn't provide auth
            assert response.status_code in [401, 403], (
                f"Expected auth error for unauthenticated request, got {response.status_code}"
            )
            
            print("✅ Frontend request pattern now works correctly!")
    
    def test_route_registration_shows_both_endpoints(self):
        """
        Verify that FastAPI now registers both route patterns.
        """
        # Check registered routes
        assessment_post_routes = []
        for route in app.routes:
            if (hasattr(route, 'path') and hasattr(route, 'methods') and 
                'assessments' in route.path and 'POST' in route.methods and
                '{' not in route.path):  # Exclude parameterized routes
                assessment_post_routes.append(route.path)
        
        print(f"Assessment POST routes: {assessment_post_routes}")
        
        # Should have both patterns
        assert '/api/v1/assessments' in assessment_post_routes, (
            "Missing route: /api/v1/assessments (without trailing slash)"
        )
        assert '/api/v1/assessments/' in assessment_post_routes, (
            "Missing route: /api/v1/assessments/ (with trailing slash)"
        )
        
        print("✅ Both route patterns are properly registered!")


@pytest.mark.asyncio 
async def test_comprehensive_fix_verification():
    """
    Comprehensive test that verifies the complete fix.
    
    This test can be run to verify that the 404 bug is completely resolved.
    """
    print("\n" + "="*60)
    print("TESTING ASSESSMENT 404 BUG FIX")
    print("="*60)
    
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver"
    ) as client:
        
        # Test 1: The problematic URL should not return 404
        print("\n1. Testing problematic URL: POST /api/v1/assessments")
        response = await client.post("/api/v1/assessments")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 404:
            print("   ❌ FAIL: Still getting 404 - bug not fixed!")
            assert False, "Bug not fixed: still getting 404"
        elif response.status_code in [401, 403]:
            print("   ✅ PASS: Getting auth error (route exists)")
        else:
            print(f"   ⚠️  UNEXPECTED: Got {response.status_code}")
        
        # Test 2: The working URL should still work
        print("\n2. Testing reference URL: POST /api/v1/assessments/")
        response2 = await client.post("/api/v1/assessments/")
        print(f"   Status: {response2.status_code}")
        
        if response2.status_code == 404:
            print("   ❌ FAIL: Regression - reference URL broken!")
            assert False, "Regression: reference URL broken"
        elif response2.status_code in [401, 403]:
            print("   ✅ PASS: Reference URL still works")
        
        # Test 3: Both should behave identically
        print(f"\n3. Comparing responses: {response.status_code} vs {response2.status_code}")
        if response.status_code == response2.status_code:
            print("   ✅ PASS: Both URLs behave identically")
        else:
            print("   ⚠️  WARNING: URLs behave differently")
    
    print("\n" + "="*60)
    print("✅ ASSESSMENT 404 BUG FIX VERIFICATION COMPLETE")
    print("✅ Frontend POST /api/v1/assessments now works correctly!")
    print("="*60)