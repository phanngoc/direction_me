"""
Test configuration and fixtures for MyWay Career Assessment backend tests.

This module provides:
- Pytest configuration with asyncio support
- Hypothesis settings with minimum 100 examples
- Database session fixtures for async tests
- Common test fixtures for mocking
"""
import pytest
from unittest.mock import Mock, AsyncMock
from typing import List, Dict, Any, Optional
from hypothesis import settings, Verbosity

# Configure Hypothesis profiles
settings.register_profile(
    "ci",
    max_examples=100,
    verbosity=Verbosity.normal,
    deadline=5000  # 5 seconds deadline per test
)
settings.register_profile(
    "dev",
    max_examples=10,
    verbosity=Verbosity.verbose,
    deadline=10000
)
settings.register_profile(
    "debug",
    max_examples=5,
    verbosity=Verbosity.verbose,
    deadline=None
)

# Load CI profile by default
settings.load_profile("ci")


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "property: mark test as a property-based test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest.fixture
def mock_db_session():
    """Create a mock database session for unit tests."""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    session.execute = AsyncMock()
    session.add = Mock()
    session.delete = Mock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
async def async_db_session(mock_db_session):
    """Async context manager for database session."""
    yield mock_db_session


# ============================================================================
# HTTP Client Fixtures
# ============================================================================

@pytest.fixture
async def client():
    """Create an HTTP client for integration tests."""
    import httpx
    from backend.src.main import app
    
    # Use AsyncClient with ASGI transport for FastAPI
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver"
    ) as ac:
        yield ac


@pytest.fixture
async def db():
    """Create a database session for integration tests."""
    from backend.src.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        yield session


# ============================================================================
# Profile Vector Fixtures
# ============================================================================

@pytest.fixture
def mock_profile_vector():
    """
    Factory fixture to create mock ProfileVector with configurable scores.
    
    Usage:
        pv = mock_profile_vector([50.0] * 16)
        pv = mock_profile_vector()  # defaults to all 50.0
    """
    from backend.src.models.profile_vector import ProfileVector
    
    def _create(scores: Optional[List[float]] = None) -> Mock:
        if scores is None:
            scores = [50.0] * 16
        
        pv = Mock(spec=ProfileVector)
        pv.to_vector.return_value = scores
        
        # Set individual attributes
        facet_names = [
            'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
            'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
            'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
            'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
        ]
        for i, name in enumerate(facet_names):
            setattr(pv, name, scores[i] if i < len(scores) else 0.0)
        
        return pv
    
    return _create


@pytest.fixture
def mock_profile_vector_with_nulls():
    """
    Factory fixture to create ProfileVector with null values at specified indices.
    
    Usage:
        pv = mock_profile_vector_with_nulls([0, 4, 8])  # nulls at indices 0, 4, 8
    """
    from backend.src.models.profile_vector import ProfileVector
    
    def _create(null_indices: List[int]) -> Mock:
        scores = [50.0] * 16
        for idx in null_indices:
            if 0 <= idx < 16:
                scores[idx] = 0.0  # Null values become 0.0 in to_vector()
        
        pv = Mock(spec=ProfileVector)
        pv.to_vector.return_value = scores
        
        facet_names = [
            'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
            'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
            'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
            'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
        ]
        for i, name in enumerate(facet_names):
            if i in null_indices:
                setattr(pv, name, None)
            else:
                setattr(pv, name, scores[i])
        
        return pv
    
    return _create


# ============================================================================
# Question Fixtures
# ============================================================================

@pytest.fixture
def eq_questions():
    """Create standard EQ questions for testing."""
    facets = ["Empathy", "Social", "SelfAwareness", "SelfRegulation"]
    return [
        Mock(
            id=f"eq_{i}",
            category="EQ",
            facet=facet,
            reverse_score=False,
            question_type="Likert",
            difficulty_weight=1.0,
            is_active=True
        )
        for i, facet in enumerate(facets)
    ]


@pytest.fixture
def iq_questions():
    """Create standard IQ questions for testing."""
    facets = ["LR", "NR", "VR", "SR"]
    return [
        Mock(
            id=f"iq_{i}",
            category="IQ",
            facet=facet,
            reverse_score=False,
            question_type="MCQ",
            difficulty_weight=1.0,
            is_active=True
        )
        for i, facet in enumerate(facets)
    ]


@pytest.fixture
def dq_questions():
    """Create standard DQ questions for testing."""
    facets = ["InfoLiteracy", "Creativity", "Safety", "Collaboration"]
    return [
        Mock(
            id=f"dq_{i}",
            category="DQ",
            facet=facet,
            reverse_score=False,
            question_type="Likert",
            difficulty_weight=1.0,
            is_active=True
        )
        for i, facet in enumerate(facets)
    ]


@pytest.fixture
def aq_questions():
    """Create standard AQ questions for testing."""
    facets = ["Control", "Ownership", "Reach", "Endurance"]
    return [
        Mock(
            id=f"aq_{i}",
            category="AQ",
            facet=facet,
            reverse_score=False,
            question_type="Likert",
            difficulty_weight=1.0,
            is_active=True
        )
        for i, facet in enumerate(facets)
    ]


@pytest.fixture
def all_questions(iq_questions, eq_questions, dq_questions, aq_questions):
    """Combine all question types into a single list."""
    return iq_questions + eq_questions + dq_questions + aq_questions


# ============================================================================
# Career Rule Fixtures
# ============================================================================

@pytest.fixture
def mock_career_rule():
    """
    Factory fixture to create mock CareerRule.
    
    Usage:
        rule = mock_career_rule("Software Engineer", is_active=True)
    """
    def _create(
        career_name: str = "Test Career",
        is_active: bool = True,
        weights: Optional[Dict[str, float]] = None,
        thresholds: Optional[Dict[str, float]] = None,
        bonus_keys: Optional[List[str]] = None
    ) -> Mock:
        facet_keys = [
            'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
            'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
            'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
            'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
        ]
        
        if weights is None:
            weights = {key: 0.5 for key in facet_keys}
        if thresholds is None:
            thresholds = {key: 30.0 for key in facet_keys}
        if bonus_keys is None:
            bonus_keys = []
        
        rule = Mock()
        rule.career_name = career_name
        rule.is_active = is_active
        rule.weights = weights
        rule.thresholds = thresholds
        rule.bonus_keys = bonus_keys
        
        return rule
    
    return _create


@pytest.fixture
def sample_career_rules(mock_career_rule):
    """Create a set of sample career rules for testing."""
    return [
        mock_career_rule("Software Engineer", is_active=True),
        mock_career_rule("Data Scientist", is_active=True),
        mock_career_rule("Product Manager", is_active=True),
        mock_career_rule("UX Designer", is_active=True),
        mock_career_rule("Inactive Career", is_active=False),
    ]


# ============================================================================
# Answer Fixtures
# ============================================================================

@pytest.fixture
def create_answers():
    """
    Factory fixture to create answer dictionaries.
    
    Usage:
        answers = create_answers(questions, value=4)
        answers = create_answers(questions)  # random values
    """
    def _create(
        questions: List[Mock],
        value: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        import random
        return [
            {
                "question_id": q.id,
                "answer_value": value if value is not None else random.randint(1, 5)
            }
            for q in questions
        ]
    
    return _create


# ============================================================================
# Assessment Fixtures
# ============================================================================

@pytest.fixture
def mock_assessment():
    """Create a mock assessment object."""
    import uuid
    from datetime import datetime
    
    assessment = Mock()
    assessment.id = uuid.uuid4()
    assessment.user_id = uuid.uuid4()
    assessment.status = "in_progress"
    assessment.answered_questions = 0
    assessment.started_at = datetime.utcnow()
    assessment.completed_at = None
    
    return assessment


@pytest.fixture
def mock_assessment_result():
    """Create a mock assessment result object."""
    import uuid
    from datetime import datetime
    
    result = Mock()
    result.id = uuid.uuid4()
    result.assessment_id = uuid.uuid4()
    result.iq_score = 75.0
    result.eq_score = 80.0
    result.dq_score = 70.0
    result.aq_score = 65.0
    result.created_at = datetime.utcnow()
    
    return result
