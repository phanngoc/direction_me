"""
Integration tests for career API endpoints.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.main import app
from backend.src.models.user import User
from backend.src.models.assessment import Assessment
from backend.src.models.assessment_result import AssessmentResult
from backend.src.models.profile_vector import ProfileVector
from backend.src.models.career_suggestion import CareerSuggestion


@pytest.fixture
async def test_user(db: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="Test User",
        age=20
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def test_assessment(db: AsyncSession, test_user: User) -> Assessment:
    """Create a test assessment."""
    assessment = Assessment(
        user_id=test_user.id,
        status="completed",
        total_questions=16,
        answered_questions=16
    )
    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)
    return assessment


@pytest.fixture
async def test_assessment_result(db: AsyncSession, test_assessment: Assessment) -> AssessmentResult:
    """Create a test assessment result."""
    result = AssessmentResult(
        assessment_id=test_assessment.id,
        iq_score=75.0,
        eq_score=80.0,
        dq_score=70.0,
        aq_score=85.0,
        ikigai_love=80.0,
        ikigai_good_at=75.0,
        ikigai_world_needs=70.0,
        ikigai_paid_for=85.0,
        ikigai_harmonic=77.5,
        ikigai_geometric=77.2
    )
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


@pytest.fixture
async def test_profile_vector(db: AsyncSession, test_assessment_result: AssessmentResult) -> ProfileVector:
    """Create a test profile vector."""
    vector = ProfileVector(
        assessment_result_id=test_assessment_result.id,
        iq_lr=80.0,
        iq_nr=70.0,
        iq_vr=75.0,
        iq_sr=65.0,
        eq_empathy=85.0,
        eq_social=75.0,
        eq_self_awareness=80.0,
        eq_self_regulation=70.0,
        dq_info_literacy=75.0,
        dq_creativity=70.0,
        dq_safety=80.0,
        dq_collaboration=75.0,
        aq_control=85.0,
        aq_ownership=80.0,
        aq_reach=70.0,
        aq_endurance=75.0
    )
    db.add(vector)
    await db.commit()
    await db.refresh(vector)
    return vector


@pytest.fixture
async def test_career_suggestions(db: AsyncSession, test_assessment_result: AssessmentResult) -> list[CareerSuggestion]:
    """Create test career suggestions."""
    suggestions = []
    careers = ["Software Engineer", "Data Scientist", "UX Designer"]
    
    for i, career in enumerate(careers):
        suggestion = CareerSuggestion(
            assessment_result_id=test_assessment_result.id,
            career_name=career,
            fit_score=85.0 - (i * 5),
            rank=i + 1,
            explanation=f"Good fit for {career}"
        )
        db.add(suggestion)
        suggestions.append(suggestion)
    
    await db.commit()
    for suggestion in suggestions:
        await db.refresh(suggestion)
    
    return suggestions


class TestCareerAPI:
    """Test cases for career API endpoints."""
    
    async def test_get_career_suggestions(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_assessment_result: AssessmentResult,
        test_career_suggestions: list[CareerSuggestion]
    ):
        """Test getting career suggestions."""
        response = await client.get(
            f"/api/v1/careers/suggestions/{test_assessment_result.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) == 3
        
        # Check that suggestions are ranked
        for i, suggestion in enumerate(data["data"]):
            assert suggestion["rank"] == i + 1
            assert "career_name" in suggestion
            assert "fit_score" in suggestion
            assert "explanation" in suggestion
    
    async def test_get_career_suggestions_not_found(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test getting career suggestions for non-existent result."""
        response = await client.get(
            "/api/v1/careers/suggestions/non-existent-id",
            headers=auth_headers
        )
        
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"].lower()
    
    async def test_generate_career_suggestions(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_assessment_result: AssessmentResult,
        test_profile_vector: ProfileVector
    ):
        """Test generating new career suggestions."""
        response = await client.post(
            f"/api/v1/careers/suggestions/{test_assessment_result.id}/generate",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert len(data["data"]) > 0
        
        # Check that suggestions are properly formatted
        for suggestion in data["data"]:
            assert "career_name" in suggestion
            assert "fit_score" in suggestion
            assert "rank" in suggestion
            assert "explanation" in suggestion
            assert 0 <= suggestion["fit_score"] <= 100
    
    async def test_get_career_details(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test getting career details."""
        response = await client.get(
            "/api/v1/careers/details/Software Engineer",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        career_data = data["data"]
        assert "career_name" in career_data
        assert "description" in career_data
        assert "key_skills" in career_data
        assert "education_requirements" in career_data
        assert "experience_level" in career_data
        assert "salary_range" in career_data
        assert "growth_outlook" in career_data
    
    async def test_get_career_details_not_found(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test getting career details for unknown career."""
        response = await client.get(
            "/api/v1/careers/details/Unknown Career",
            headers=auth_headers
        )
        
        assert response.status_code == 200  # Should return default structure
        data = response.json()
        assert data["success"] is True
        assert data["data"]["career_name"] == "Unknown Career"
    
    async def test_compare_careers(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test comparing multiple careers."""
        response = await client.get(
            "/api/v1/careers/compare?career_names=Software Engineer,Data Scientist,UX Designer",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        comparison_data = data["data"]
        assert len(comparison_data) == 3
        
        # Check that all careers are included
        career_names = [career["career_name"] for career in comparison_data]
        assert "Software Engineer" in career_names
        assert "Data Scientist" in career_names
        assert "UX Designer" in career_names
    
    async def test_compare_careers_single(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test comparing single career."""
        response = await client.get(
            "/api/v1/careers/compare?career_names=Software Engineer",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 1
        assert data["data"][0]["career_name"] == "Software Engineer"
    
    async def test_compare_careers_no_names(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test comparing careers with no names provided."""
        response = await client.get(
            "/api/v1/careers/compare",
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "career_names" in data["message"].lower()
    
    async def test_search_careers(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test searching careers."""
        response = await client.get(
            "/api/v1/careers/search?query=engineer",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        # Should return careers matching "engineer"
        for career in data["data"]:
            assert "engineer" in career["career_name"].lower()
    
    async def test_search_careers_no_query(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test searching careers with no query."""
        response = await client.get(
            "/api/v1/careers/search",
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "query" in data["message"].lower()
    
    async def test_get_career_statistics(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test getting career statistics."""
        response = await client.get(
            "/api/v1/careers/statistics",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        
        stats = data["data"]
        assert "total_careers" in stats
        assert "active_careers" in stats
        assert "average_fit_score" in stats
        assert "top_careers" in stats
    
    async def test_unauthorized_access(
        self,
        client: AsyncClient
    ):
        """Test accessing career endpoints without authentication."""
        response = await client.get("/api/v1/careers/suggestions/test-id")
        
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "unauthorized" in data["message"].lower()
    
    async def test_invalid_assessment_result_id(
        self,
        client: AsyncClient,
        auth_headers: dict
    ):
        """Test with invalid assessment result ID format."""
        response = await client.get(
            "/api/v1/careers/suggestions/invalid-uuid",
            headers=auth_headers
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "invalid" in data["message"].lower()
    
    async def test_career_suggestions_pagination(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_assessment_result: AssessmentResult,
        test_career_suggestions: list[CareerSuggestion]
    ):
        """Test career suggestions with pagination."""
        response = await client.get(
            f"/api/v1/careers/suggestions/{test_assessment_result.id}?limit=2&offset=0",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 2
        
        # Test second page
        response = await client.get(
            f"/api/v1/careers/suggestions/{test_assessment_result.id}?limit=2&offset=2",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 1  # Only one remaining suggestion
    
    async def test_career_suggestions_sorting(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_assessment_result: AssessmentResult,
        test_career_suggestions: list[CareerSuggestion]
    ):
        """Test career suggestions sorting."""
        response = await client.get(
            f"/api/v1/careers/suggestions/{test_assessment_result.id}?sort_by=fit_score&sort_order=asc",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Check that suggestions are sorted by fit_score ascending
        fit_scores = [s["fit_score"] for s in data["data"]]
        assert fit_scores == sorted(fit_scores)
    
    async def test_career_suggestions_filtering(
        self,
        client: AsyncClient,
        auth_headers: dict,
        test_assessment_result: AssessmentResult,
        test_career_suggestions: list[CareerSuggestion]
    ):
        """Test career suggestions filtering."""
        response = await client.get(
            f"/api/v1/careers/suggestions/{test_assessment_result.id}?min_fit_score=80",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Check that all suggestions meet minimum fit score
        for suggestion in data["data"]:
            assert suggestion["fit_score"] >= 80