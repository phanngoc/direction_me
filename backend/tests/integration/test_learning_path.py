"""
Integration tests for learning path API
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
import json


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    """Get authentication token"""
    # Register test user
    response = client.post(
        "/auth/register",
        json={
            "email": "learningpath@test.com",
            "password": "testpass123",
            "full_name": "Learning Path Test",
            "age": 20
        }
    )

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "learningpath@test.com",
            "password": "testpass123"
        }
    )

    return response.json()["access_token"]


@pytest.fixture
def completed_assessment(client, auth_token):
    """Create a completed assessment with results"""
    # Create assessment
    response = client.post(
        "/assessments",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assessment_id = response.json()["id"]

    # Submit answers and complete assessment
    # (simplified - in real test would submit actual answers)
    response = client.post(
        f"/assessments/{assessment_id}/complete",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    result_id = response.json()["result_id"]
    return result_id


class TestLearningPathAPI:
    """Test suite for learning path API endpoints"""

    def test_get_learning_path_success(self, client, auth_token, completed_assessment):
        """Test successful learning path retrieval"""
        response = client.get(
            f"/results/{completed_assessment}/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "id" in data
        assert "career_name" in data
        assert "skills" in data
        assert "projects" in data
        assert "habits" in data
        assert "timeline_weeks" in data
        assert "priority" in data

    def test_get_learning_path_unauthorized(self, client, completed_assessment):
        """Test learning path retrieval without authentication"""
        response = client.get(f"/results/{completed_assessment}/learning-path")

        assert response.status_code == 401

    def test_get_learning_path_invalid_result(self, client, auth_token):
        """Test learning path retrieval with invalid result ID"""
        response = client.get(
            "/results/invalid-uuid/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code in [400, 404]

    def test_get_learning_path_for_specific_career(self, client, auth_token, completed_assessment):
        """Test learning path generation for specific career"""
        response = client.get(
            f"/results/{completed_assessment}/learning-path?career=Software%20Engineer",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["career_name"] == "Software Engineer"

    def test_learning_path_skills_structure(self, client, auth_token, completed_assessment):
        """Test that skills in learning path have correct structure"""
        response = client.get(
            f"/results/{completed_assessment}/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        for skill in data["skills"]:
            assert "name" in skill
            assert "level" in skill
            assert "duration_weeks" in skill
            assert "resources" in skill
            assert skill["level"] in ["beginner", "intermediate", "advanced"]

    def test_learning_path_projects_structure(self, client, auth_token, completed_assessment):
        """Test that projects in learning path have correct structure"""
        response = client.get(
            f"/results/{completed_assessment}/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        for project in data["projects"]:
            assert "name" in project
            assert "description" in project
            assert "duration_weeks" in project
            assert "skills_required" in project

    def test_learning_path_habits_structure(self, client, auth_token, completed_assessment):
        """Test that habits in learning path have correct structure"""
        response = client.get(
            f"/results/{completed_assessment}/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        for habit in data["habits"]:
            assert "name" in habit
            assert "frequency" in habit
            assert "duration_minutes" in habit
            assert habit["frequency"] in ["daily", "weekly", "monthly"]

    def test_learning_path_caching(self, client, auth_token, completed_assessment):
        """Test that learning path is cached after first generation"""
        # First request
        response1 = client.get(
            f"/results/{completed_assessment}/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Second request (should use cache)
        response2 = client.get(
            f"/results/{completed_assessment}/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Results should be identical
        assert response1.json() == response2.json()

    def test_learning_path_update_after_reassessment(self, client, auth_token):
        """Test that learning path updates after reassessment"""
        # First assessment
        response = client.post(
            "/assessments",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assessment1_id = response.json()["id"]

        response = client.post(
            f"/assessments/{assessment1_id}/complete",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        result1_id = response.json()["result_id"]

        # Get first learning path
        response = client.get(
            f"/results/{result1_id}/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        learning_path1 = response.json()

        # Second assessment
        response = client.post(
            "/assessments",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assessment2_id = response.json()["id"]

        response = client.post(
            f"/assessments/{assessment2_id}/complete",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        result2_id = response.json()["result_id"]

        # Get second learning path
        response = client.get(
            f"/results/{result2_id}/learning-path",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        learning_path2 = response.json()

        # Learning paths should exist for both
        assert "skills" in learning_path1
        assert "skills" in learning_path2

    def test_learning_path_multiple_careers(self, client, auth_token, completed_assessment):
        """Test learning path generation for multiple career options"""
        careers = ["Software Engineer", "Data Scientist", "Product Manager"]

        for career in careers:
            response = client.get(
                f"/results/{completed_assessment}/learning-path?career={career}",
                headers={"Authorization": f"Bearer {auth_token}"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["career_name"] == career
            assert len(data["skills"]) > 0

    def test_skill_gap_analysis_endpoint(self, client, auth_token, completed_assessment):
        """Test skill gap analysis endpoint"""
        response = client.get(
            f"/results/{completed_assessment}/skill-gaps?career=Software%20Engineer",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "skill_gaps" in data
        assert "prioritized_gaps" in data
        assert "readiness_score" in data
        assert 0 <= data["readiness_score"] <= 100

    def test_learning_recommendations_endpoint(self, client, auth_token, completed_assessment):
        """Test learning recommendations endpoint"""
        response = client.get(
            f"/results/{completed_assessment}/recommendations",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "iq_recommendations" in data
        assert "eq_recommendations" in data
        assert "dq_recommendations" in data
        assert "aq_recommendations" in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
