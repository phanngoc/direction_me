# Design Document: Backend Test Suite

## Overview

This design document specifies a comprehensive test suite for the MyWay Career Assessment backend system. The test suite validates scoring algorithms, Ikigai calculations, career mapping, services, and API endpoints using both unit tests and property-based tests to ensure correctness and reliability.

## Architecture

The test suite follows a layered testing approach:

```
┌─────────────────────────────────────────────────────────────┐
│                    Integration Tests                         │
│  (API endpoints, full request/response cycles)              │
├─────────────────────────────────────────────────────────────┤
│                    Service Tests                             │
│  (AssessmentService, CareerService, UserService)            │
├─────────────────────────────────────────────────────────────┤
│                    Algorithm Tests                           │
│  (IQ/EQ/DQ/AQ Scoring, Ikigai, Career Mapping)             │
├─────────────────────────────────────────────────────────────┤
│                    Model Tests                               │
│  (ProfileVector, QuestionBank, CareerRule)                  │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Test Generators

Property-based tests require generators for creating random test data:

```python
# generators.py
from hypothesis import strategies as st
from hypothesis.strategies import composite

# Likert scale values (1-5)
likert_value = st.integers(min_value=1, max_value=5)

# Score values (0-100)
score_value = st.floats(min_value=0.0, max_value=100.0, allow_nan=False)

# Difficulty weights (positive floats)
difficulty_weight = st.floats(min_value=0.1, max_value=3.0, allow_nan=False)

@composite
def profile_vector_scores(draw):
    """Generate 16-dimensional profile vector scores."""
    return [draw(score_value) for _ in range(16)]

@composite
def mock_question(draw, category: str, facet: str):
    """Generate a mock question with given category and facet."""
    return Mock(
        id=draw(st.uuids()),
        category=category,
        facet=facet,
        difficulty_weight=draw(difficulty_weight),
        reverse_score=draw(st.booleans()),
        question_type="Likert" if category != "IQ" else "MCQ"
    )

@composite
def answer_for_question(draw, question_id):
    """Generate an answer for a given question."""
    return {
        "question_id": question_id,
        "answer_value": draw(likert_value)
    }

@composite
def career_rule(draw, career_name: str = None):
    """Generate a mock career rule."""
    return Mock(
        career_name=career_name or draw(st.text(min_size=1, max_size=50)),
        weights={f"facet_{i}": draw(st.floats(0.1, 1.0)) for i in range(16)},
        thresholds={f"facet_{i}": draw(st.floats(0.0, 80.0)) for i in range(16)},
        bonus_keys=draw(st.lists(st.sampled_from([f"facet_{i}" for i in range(16)]), max_size=4)),
        is_active=True
    )
```

### Test Fixtures

```python
# conftest.py
import pytest
from hypothesis import settings

# Configure Hypothesis for minimum 100 iterations
settings.register_profile("ci", max_examples=100)
settings.load_profile("ci")

@pytest.fixture
def mock_profile_vector():
    """Create a mock ProfileVector with configurable scores."""
    def _create(scores: list[float] = None):
        pv = Mock(spec=ProfileVector)
        pv.to_vector.return_value = scores or [50.0] * 16
        return pv
    return _create

@pytest.fixture
def eq_questions():
    """Create standard EQ questions for testing."""
    facets = ["Empathy", "Social", "SelfAwareness", "SelfRegulation"]
    return [
        Mock(id=f"eq_{i}", category="EQ", facet=facet, reverse_score=False)
        for i, facet in enumerate(facets)
    ]
```

## Data Models

### Test Data Structures

```python
@dataclass
class ScoringTestCase:
    """Test case for scoring algorithm validation."""
    answers: List[Dict[str, Any]]
    questions: List[QuestionBank]
    expected_score_range: Tuple[float, float]
    description: str

@dataclass
class IkigaiTestCase:
    """Test case for Ikigai calculation validation."""
    profile_scores: List[float]
    expected_love: float
    expected_good_at: float
    expected_world_needs: float
    expected_paid_for: float

@dataclass
class CareerFitTestCase:
    """Test case for career fit calculation."""
    profile_scores: List[float]
    career_rule: CareerRule
    expected_fit_range: Tuple[float, float]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Likert Normalization Produces Valid Range

*For any* valid Likert scale answer (1-5), the normalized score SHALL be in the range [0, 100] and follow the formula t̂_j = 25*(t_j-1).

**Validates: Requirements 1.1, 1.6**

```python
@given(answer_value=st.integers(min_value=1, max_value=5))
def test_likert_normalization_range(answer_value):
    # t̂_j = 25*(t_j-1)
    expected = 25 * (answer_value - 1)
    assert 0 <= expected <= 100
    assert expected == normalize_likert(answer_value)
```

### Property 2: Reverse Scoring Transformation

*For any* Likert answer value and reverse_score=true, the transformation t_j = (6-x_j) SHALL be applied before normalization, resulting in inverted scores.

**Validates: Requirements 1.2**

```python
@given(answer_value=st.integers(min_value=1, max_value=5))
def test_reverse_scoring_transformation(answer_value):
    normal_score = normalize_likert(answer_value, reverse=False)
    reverse_score = normalize_likert(answer_value, reverse=True)
    # Reverse of 1 should equal normal of 5, etc.
    assert normal_score + reverse_score == 100
```

### Property 3: Facet Score is Average of Question Scores

*For any* set of questions within a facet and their corresponding answers, the facet score SHALL equal the arithmetic mean of all normalized question scores.

**Validates: Requirements 1.3**

```python
@given(answers=st.lists(st.integers(1, 5), min_size=1, max_size=10))
def test_facet_score_is_average(answers):
    normalized = [25 * (a - 1) for a in answers]
    expected_average = sum(normalized) / len(normalized)
    # Create mock questions and answers
    facet_score = calculate_facet_score(answers, questions)
    assert abs(facet_score - expected_average) < 0.001
```

### Property 4: Domain Score is Average of Facet Scores

*For any* domain (IQ, EQ, DQ, AQ), the domain score SHALL equal the arithmetic mean of all facet scores within that domain.

**Validates: Requirements 1.4**

```python
@given(facet_scores=st.lists(score_value, min_size=4, max_size=4))
def test_domain_score_is_facet_average(facet_scores):
    expected_domain_score = sum(facet_scores) / len(facet_scores)
    domain_score = calculate_domain_score(facet_scores)
    assert abs(domain_score - expected_domain_score) < 0.001
```

### Property 5: IQ Weighted Difficulty Scoring

*For any* set of IQ questions with difficulty weights and correctness values, the IQ score SHALL follow the formula: S_IQ = 100 * (Σ(d_i * r_i)) / Σ(d_i).

**Validates: Requirements 1.5**

```python
@given(
    weights=st.lists(st.floats(0.1, 3.0), min_size=1, max_size=10),
    correctness=st.lists(st.integers(0, 1), min_size=1, max_size=10)
)
def test_iq_weighted_scoring(weights, correctness):
    assume(len(weights) == len(correctness))
    weighted_sum = sum(w * c for w, c in zip(weights, correctness))
    total_weight = sum(weights)
    expected = 100 * weighted_sum / total_weight if total_weight > 0 else 0
    actual = calculate_iq_score(weights, correctness)
    assert abs(actual - expected) < 0.001
```

### Property 6: Profile Vector Dimension and Ordering

*For any* ProfileVector, the to_vector() method SHALL return exactly 16 elements in the order: [iq_lr, iq_nr, iq_vr, iq_sr, eq_empathy, eq_social, eq_self_awareness, eq_self_regulation, dq_info_literacy, dq_creativity, dq_safety, dq_collaboration, aq_control, aq_ownership, aq_reach, aq_endurance].

**Validates: Requirements 2.1, 2.2**

```python
@given(scores=st.lists(score_value, min_size=16, max_size=16))
def test_profile_vector_structure(scores):
    pv = create_profile_vector(scores)
    vector = pv.to_vector()
    assert len(vector) == 16
    # Verify ordering by checking specific indices
    assert vector[0] == pv.iq_lr
    assert vector[4] == pv.eq_empathy
    assert vector[8] == pv.dq_info_literacy
    assert vector[12] == pv.aq_control
```

### Property 7: Profile Vector Null Handling

*For any* ProfileVector with null facet values, the to_vector() method SHALL return 0.0 for null positions.

**Validates: Requirements 2.4**

```python
@given(null_indices=st.lists(st.integers(0, 15), unique=True, max_size=8))
def test_profile_vector_null_handling(null_indices):
    pv = create_profile_vector_with_nulls(null_indices)
    vector = pv.to_vector()
    for idx in null_indices:
        assert vector[idx] == 0.0
```

### Property 8: Ikigai Axis Formulas

*For any* valid profile vector, the Ikigai axis scores SHALL be calculated using the correct formulas:
- love = (eq_empathy + eq_social + dq_creativity) / 3
- good_at = (iq_lr + iq_nr + iq_vr + iq_sr) / 4
- world_needs = (dq_info_literacy + dq_safety + aq_control + aq_ownership) / 4
- paid_for = (aq_reach + aq_endurance + eq_self_awareness + eq_self_regulation) / 4

**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

```python
@given(scores=profile_vector_scores())
def test_ikigai_axis_formulas(scores):
    pv = create_mock_profile_vector(scores)
    result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
    
    # Verify love axis
    expected_love = (scores[4] + scores[5] + scores[9]) / 3
    assert abs(result['ikigai_love'] - expected_love) < 0.001
    
    # Verify good_at axis
    expected_good_at = sum(scores[0:4]) / 4
    assert abs(result['ikigai_good_at'] - expected_good_at) < 0.001
    
    # Verify world_needs axis
    expected_world_needs = (scores[8] + scores[10] + scores[12] + scores[13]) / 4
    assert abs(result['ikigai_world_needs'] - expected_world_needs) < 0.001
    
    # Verify paid_for axis
    expected_paid_for = (scores[14] + scores[15] + scores[6] + scores[7]) / 4
    assert abs(result['ikigai_paid_for'] - expected_paid_for) < 0.001
```

### Property 9: Harmonic Mean Formula

*For any* four positive axis scores, the harmonic mean SHALL equal 4 / (1/love + 1/good_at + 1/world_needs + 1/paid_for).

**Validates: Requirements 3.5**

```python
@given(
    love=st.floats(0.1, 100.0),
    good_at=st.floats(0.1, 100.0),
    world_needs=st.floats(0.1, 100.0),
    paid_for=st.floats(0.1, 100.0)
)
def test_harmonic_mean_formula(love, good_at, world_needs, paid_for):
    expected = 4 / (1/love + 1/good_at + 1/world_needs + 1/paid_for)
    actual = IkigaiCalculationAlgorithm._calculate_harmonic_mean(
        love, good_at, world_needs, paid_for
    )
    assert abs(actual - expected) < 0.001
```

### Property 10: Geometric Mean Formula

*For any* four positive axis scores, the geometric mean SHALL equal (love * good_at * world_needs * paid_for)^(1/4).

**Validates: Requirements 3.6**

```python
@given(
    love=st.floats(0.1, 100.0),
    good_at=st.floats(0.1, 100.0),
    world_needs=st.floats(0.1, 100.0),
    paid_for=st.floats(0.1, 100.0)
)
def test_geometric_mean_formula(love, good_at, world_needs, paid_for):
    import math
    expected = math.pow(love * good_at * world_needs * paid_for, 0.25)
    actual = IkigaiCalculationAlgorithm._calculate_geometric_mean(
        love, good_at, world_needs, paid_for
    )
    assert abs(actual - expected) < 0.001
```

### Property 11: Career Suggestions Sorted and Limited

*For any* set of career fit calculations, the results SHALL be sorted by fit_score in descending order and limited to maximum 8 suggestions.

**Validates: Requirements 4.5, 4.6**

```python
@given(
    profile_scores=profile_vector_scores(),
    num_rules=st.integers(1, 15)
)
def test_career_suggestions_sorted_and_limited(profile_scores, num_rules):
    pv = create_mock_profile_vector(profile_scores)
    rules = [create_mock_career_rule(f"Career{i}") for i in range(num_rules)]
    
    result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
    
    # Verify sorted descending
    for i in range(len(result) - 1):
        assert result[i]['fit_score'] >= result[i + 1]['fit_score']
    
    # Verify limited to 8
    assert len(result) <= 8
```

### Property 12: Inactive Career Rules Excluded

*For any* set of career rules where some have is_active=false, only active rules SHALL be included in calculations.

**Validates: Requirements 4.7**

```python
@given(
    profile_scores=profile_vector_scores(),
    active_count=st.integers(0, 5),
    inactive_count=st.integers(1, 5)
)
def test_inactive_rules_excluded(profile_scores, active_count, inactive_count):
    pv = create_mock_profile_vector(profile_scores)
    active_rules = [create_mock_career_rule(f"Active{i}", is_active=True) for i in range(active_count)]
    inactive_rules = [create_mock_career_rule(f"Inactive{i}", is_active=False) for i in range(inactive_count)]
    
    result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, active_rules + inactive_rules)
    
    # Verify no inactive careers in results
    career_names = [r['career_name'] for r in result]
    for inactive in inactive_rules:
        assert inactive.career_name not in career_names
```

### Property 13: Career Fit Threshold Filtering

*For any* career with fit score below 30%, it SHALL be excluded from suggestions.

**Validates: Requirements 4.4**

```python
@given(profile_scores=profile_vector_scores())
def test_career_fit_threshold_filtering(profile_scores):
    pv = create_mock_profile_vector(profile_scores)
    rules = [create_mock_career_rule(f"Career{i}") for i in range(10)]
    
    result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
    
    # Verify all results have fit_score >= 30
    for career in result:
        assert career['fit_score'] >= 30
```

### Property 14: Assessment Initialization State

*For any* newly created assessment, the status SHALL be 'in_progress' and answered_questions SHALL be 0.

**Validates: Requirements 5.1**

```python
@given(user_id=st.uuids())
async def test_assessment_initialization(user_id, db_session):
    service = AssessmentService(db_session)
    assessment = await service.create_assessment(str(user_id))
    
    assert assessment.status == 'in_progress'
    assert assessment.answered_questions == 0
```

### Property 15: Assessment State Transitions

*For any* assessment, completing it SHALL set status to 'completed' and abandoning SHALL set status to 'abandoned', both recording completed_at timestamp.

**Validates: Requirements 5.3, 5.4**

```python
@given(user_id=st.uuids())
async def test_assessment_state_transitions(user_id, db_session):
    service = AssessmentService(db_session)
    assessment = await service.create_assessment(str(user_id))
    
    # Test completion
    completed = await service.complete_assessment(str(assessment.id))
    assert completed.status == 'completed'
    assert completed.completed_at is not None
    
    # Test abandonment (new assessment)
    assessment2 = await service.create_assessment(str(user_id))
    abandoned = await service.abandon_assessment(str(assessment2.id))
    assert abandoned.status == 'abandoned'
    assert abandoned.completed_at is not None
```

### Property 16: Answer Validation Completeness

*For any* set of required questions, validation SHALL return true only if all required questions have answers.

**Validates: Requirements 9.1, 9.2**

```python
@given(
    num_questions=st.integers(1, 20),
    num_answers=st.integers(0, 20)
)
def test_answer_validation_completeness(num_questions, num_answers):
    questions = [create_mock_question(f"q{i}") for i in range(num_questions)]
    answers = [{"question_id": f"q{i}", "answer_value": 3} for i in range(num_answers)]
    
    result = validate_answers(answers, questions)
    
    if num_answers >= num_questions:
        assert result == True
    else:
        assert result == False
```

### Property 17: Algorithm Determinism

*For any* valid inputs, multiple calls to scoring, Ikigai, and career mapping algorithms with identical inputs SHALL produce identical outputs.

**Validates: Requirements 10.1, 10.2, 10.3**

```python
@given(profile_scores=profile_vector_scores())
def test_algorithm_determinism(profile_scores):
    pv = create_mock_profile_vector(profile_scores)
    
    # Test Ikigai determinism
    ikigai1 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
    ikigai2 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
    assert ikigai1 == ikigai2
    
    # Test career mapping determinism
    rules = [create_mock_career_rule(f"Career{i}") for i in range(5)]
    career1 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
    career2 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
    assert career1 == career2
```

### Property 18: Career Analysis Response Structure

*For any* valid assessment result, the career analysis SHALL include ikigai_scores, interpretation, quadrant, and recommendations.

**Validates: Requirements 6.3**

```python
@given(profile_scores=profile_vector_scores())
async def test_career_analysis_structure(profile_scores, db_session):
    # Setup assessment result with profile vector
    assessment_result = await create_test_assessment_result(db_session, profile_scores)
    
    service = CareerService(db_session)
    analysis = await service.get_career_analysis(str(assessment_result.id))
    
    assert 'ikigai_scores' in analysis
    assert 'ikigai_interpretation' in analysis
    assert 'ikigai_quadrant' in analysis
    assert 'development_recommendations' in analysis
    assert 'career_suggestions' in analysis
```

## Error Handling

### Edge Case Handling

The test suite validates proper handling of edge cases:

1. **Empty Inputs**: Scoring algorithms return 0.0 for empty answers or questions
2. **Zero Scores**: Ikigai calculations handle division by zero gracefully
3. **Boundary Values**: All calculations handle 0 and 100 score boundaries
4. **Invalid Ranges**: Graceful handling of out-of-range answer values

### API Error Responses

| Scenario | Expected Status | Response Body |
|----------|-----------------|---------------|
| Missing authentication | 401 | `{"detail": "Not authenticated"}` |
| Unauthorized access | 403 | `{"detail": "Not authorized to access this assessment"}` |
| Resource not found | 404 | `{"detail": "Assessment not found"}` |
| Validation error | 422 | `{"detail": [{"loc": [...], "msg": "...", "type": "..."}]}` |
| Invalid comparison | 400 | `{"detail": "At least 2 careers required for comparison"}` |

## Testing Strategy

### Dual Testing Approach

The test suite employs both unit tests and property-based tests:

**Unit Tests** (pytest):
- Specific examples demonstrating correct behavior
- Edge cases (empty inputs, boundary values, null handling)
- Error conditions and exception handling
- Integration points between components
- API endpoint response validation

**Property-Based Tests** (Hypothesis):
- Universal properties that hold for all valid inputs
- Mathematical formula verification
- Invariant checking (sorting, limiting, range constraints)
- Determinism verification

### Test Configuration

```python
# pytest.ini
[pytest]
testpaths = backend/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto

# Hypothesis settings
[hypothesis]
max_examples = 100
deadline = 5000
```

### Property-Based Testing Framework

The test suite uses **Hypothesis** for property-based testing in Python:

```python
from hypothesis import given, strategies as st, settings

@settings(max_examples=100)
@given(...)
def test_property_name(...):
    # Property test implementation
```

### Test Organization

```
backend/tests/
├── conftest.py              # Shared fixtures and configuration
├── generators.py            # Hypothesis strategies for test data
├── unit/
│   ├── test_scoring.py      # Scoring algorithm tests
│   ├── test_ikigai.py       # Ikigai calculation tests
│   ├── test_career_mapping.py # Career mapping tests
│   ├── test_profile_vector.py # Profile vector tests
│   └── test_validation.py   # Input validation tests
├── property/
│   ├── test_scoring_properties.py    # Scoring property tests
│   ├── test_ikigai_properties.py     # Ikigai property tests
│   ├── test_career_properties.py     # Career mapping property tests
│   └── test_consistency_properties.py # Determinism tests
├── integration/
│   ├── test_assessment.py   # Assessment API tests
│   ├── test_careers.py      # Career API tests
│   ├── test_ikigai.py       # Ikigai API tests
│   └── test_auth.py         # Authentication tests
└── fixtures/
    ├── questions.json       # Sample question data
    └── career_rules.json    # Sample career rules
```

### Coverage Requirements

- Minimum 80% code coverage for algorithms
- 100% coverage for critical scoring formulas
- All API endpoints tested for success and error cases
- All edge cases documented and tested
