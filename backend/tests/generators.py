"""
Hypothesis generators (strategies) for property-based testing.

This module provides reusable strategies for generating test data:
- likert_value: Likert scale values (1-5)
- score_value: Score values (0-100)
- profile_vector_scores: 16-dimensional profile vectors
- mock_question: Question objects with configurable attributes
- answer_for_question: Answer dictionaries for questions
- career_rule: Career rule objects with weights and thresholds
"""
import uuid
from typing import Optional, List
from unittest.mock import Mock

from hypothesis import strategies as st
from hypothesis.strategies import composite


# ============================================================================
# Basic Value Strategies
# ============================================================================

# Likert scale values (1-5) for EQ, DQ, AQ questions
likert_value = st.integers(min_value=1, max_value=5)

# Score values (0-100) for normalized scores
score_value = st.floats(
    min_value=0.0,
    max_value=100.0,
    allow_nan=False,
    allow_infinity=False
)

# Difficulty weights for IQ questions (positive floats)
difficulty_weight = st.floats(
    min_value=0.1,
    max_value=3.0,
    allow_nan=False,
    allow_infinity=False
)

# Binary correctness for IQ answers (0 or 1)
correctness_value = st.integers(min_value=0, max_value=1)


# ============================================================================
# Composite Strategies
# ============================================================================

@composite
def profile_vector_scores(draw, min_score: float = 0.0, max_score: float = 100.0):
    """
    Generate a 16-dimensional profile vector with scores.
    
    Args:
        draw: Hypothesis draw function
        min_score: Minimum score value (default 0.0)
        max_score: Maximum score value (default 100.0)
    
    Returns:
        List of 16 float values representing facet scores
    """
    score_strategy = st.floats(
        min_value=min_score,
        max_value=max_score,
        allow_nan=False,
        allow_infinity=False
    )
    return [draw(score_strategy) for _ in range(16)]


@composite
def profile_vector_scores_positive(draw):
    """
    Generate a 16-dimensional profile vector with positive scores (> 0.1).
    Useful for testing harmonic/geometric mean calculations.
    """
    score_strategy = st.floats(
        min_value=0.1,
        max_value=100.0,
        allow_nan=False,
        allow_infinity=False
    )
    return [draw(score_strategy) for _ in range(16)]


@composite
def mock_question(
    draw,
    category: Optional[str] = None,
    facet: Optional[str] = None,
    question_type: Optional[str] = None
):
    """
    Generate a mock question object with configurable attributes.
    
    Args:
        draw: Hypothesis draw function
        category: Question category (IQ, EQ, DQ, AQ) or None for random
        facet: Question facet or None for random based on category
        question_type: Question type (MCQ, Likert) or None for auto-detect
    
    Returns:
        Mock question object
    """
    # Define valid facets per category
    facets_by_category = {
        "IQ": ["LR", "NR", "VR", "SR"],
        "EQ": ["Empathy", "Social", "SelfAwareness", "SelfRegulation"],
        "DQ": ["InfoLiteracy", "Creativity", "Safety", "Collaboration"],
        "AQ": ["Control", "Ownership", "Reach", "Endurance"]
    }
    
    # Select category
    if category is None:
        category = draw(st.sampled_from(["IQ", "EQ", "DQ", "AQ"]))
    
    # Select facet based on category
    if facet is None:
        facet = draw(st.sampled_from(facets_by_category[category]))
    
    # Determine question type
    if question_type is None:
        question_type = "MCQ" if category == "IQ" else "Likert"
    
    # Generate question attributes
    question = Mock()
    question.id = str(draw(st.uuids()))
    question.category = category
    question.facet = facet
    question.question_type = question_type
    question.difficulty_weight = draw(difficulty_weight)
    question.reverse_score = draw(st.booleans())
    question.is_active = True
    question.question_text = f"Test question for {category} - {facet}"
    
    return question


@composite
def mock_question_set(draw, category: str, questions_per_facet: int = 2):
    """
    Generate a complete set of questions for a category.
    
    Args:
        draw: Hypothesis draw function
        category: Question category (IQ, EQ, DQ, AQ)
        questions_per_facet: Number of questions per facet
    
    Returns:
        List of mock question objects
    """
    facets_by_category = {
        "IQ": ["LR", "NR", "VR", "SR"],
        "EQ": ["Empathy", "Social", "SelfAwareness", "SelfRegulation"],
        "DQ": ["InfoLiteracy", "Creativity", "Safety", "Collaboration"],
        "AQ": ["Control", "Ownership", "Reach", "Endurance"]
    }
    
    questions = []
    for facet in facets_by_category[category]:
        for i in range(questions_per_facet):
            q = draw(mock_question(category=category, facet=facet))
            q.id = f"{category.lower()}_{facet.lower()}_{i}"
            questions.append(q)
    
    return questions


@composite
def answer_for_question(draw, question_id: str, category: str = "EQ"):
    """
    Generate an answer dictionary for a given question.
    
    Args:
        draw: Hypothesis draw function
        question_id: ID of the question being answered
        category: Question category to determine answer type
    
    Returns:
        Dictionary with question_id and answer_value
    """
    if category == "IQ":
        # IQ answers are binary (0 or 1 for incorrect/correct)
        answer_value = draw(correctness_value)
    else:
        # EQ, DQ, AQ use Likert scale (1-5)
        answer_value = draw(likert_value)
    
    return {
        "question_id": question_id,
        "answer_value": answer_value
    }


@composite
def answers_for_questions(draw, questions: List[Mock]):
    """
    Generate answers for a list of questions.
    
    Args:
        draw: Hypothesis draw function
        questions: List of question objects
    
    Returns:
        List of answer dictionaries
    """
    answers = []
    for q in questions:
        answer = draw(answer_for_question(
            question_id=q.id,
            category=q.category
        ))
        answers.append(answer)
    return answers


@composite
def career_rule(
    draw,
    career_name: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """
    Generate a mock career rule with weights and thresholds.
    
    Args:
        draw: Hypothesis draw function
        career_name: Career name or None for random
        is_active: Active status or None for random
    
    Returns:
        Mock career rule object
    """
    facet_keys = [
        'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
        'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
        'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
        'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
    ]
    
    # Generate career name
    if career_name is None:
        career_name = draw(st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N', 'Zs')),
            min_size=3,
            max_size=50
        ))
    
    # Generate active status
    if is_active is None:
        is_active = draw(st.booleans())
    
    # Generate weights (0.0 to 1.0 for each facet)
    weight_strategy = st.floats(
        min_value=0.0,
        max_value=1.0,
        allow_nan=False,
        allow_infinity=False
    )
    weights = {key: draw(weight_strategy) for key in facet_keys}
    
    # Generate thresholds (0.0 to 80.0 for each facet)
    threshold_strategy = st.floats(
        min_value=0.0,
        max_value=80.0,
        allow_nan=False,
        allow_infinity=False
    )
    thresholds = {key: draw(threshold_strategy) for key in facet_keys}
    
    # Generate bonus keys (subset of facet keys)
    bonus_keys = draw(st.lists(
        st.sampled_from(facet_keys),
        min_size=0,
        max_size=4,
        unique=True
    ))
    
    # Create mock career rule
    rule = Mock()
    rule.id = str(draw(st.uuids()))
    rule.career_name = career_name
    rule.is_active = is_active
    rule.weights = weights
    rule.thresholds = thresholds
    rule.bonus_keys = bonus_keys
    
    return rule


@composite
def career_rule_set(draw, num_active: int = 5, num_inactive: int = 2):
    """
    Generate a set of career rules with specified active/inactive counts.
    
    Args:
        draw: Hypothesis draw function
        num_active: Number of active career rules
        num_inactive: Number of inactive career rules
    
    Returns:
        List of mock career rule objects
    """
    rules = []
    
    # Generate active rules
    for i in range(num_active):
        rule = draw(career_rule(
            career_name=f"Active Career {i+1}",
            is_active=True
        ))
        rules.append(rule)
    
    # Generate inactive rules
    for i in range(num_inactive):
        rule = draw(career_rule(
            career_name=f"Inactive Career {i+1}",
            is_active=False
        ))
        rules.append(rule)
    
    return rules


# ============================================================================
# Helper Strategies for Edge Cases
# ============================================================================

def empty_profile_vector():
    """Generate a profile vector with all zeros."""
    return st.just([0.0] * 16)


def max_profile_vector():
    """Generate a profile vector with all maximum values (100)."""
    return st.just([100.0] * 16)


@composite
def partial_null_indices(draw, max_nulls: int = 8):
    """
    Generate a list of indices to be set as null in a profile vector.
    
    Args:
        draw: Hypothesis draw function
        max_nulls: Maximum number of null indices
    
    Returns:
        List of unique indices (0-15)
    """
    return draw(st.lists(
        st.integers(min_value=0, max_value=15),
        min_size=0,
        max_size=max_nulls,
        unique=True
    ))


# ============================================================================
# Validation Strategies
# ============================================================================

@composite
def valid_likert_answers(draw, num_answers: int):
    """
    Generate a list of valid Likert scale answers.
    
    Args:
        draw: Hypothesis draw function
        num_answers: Number of answers to generate
    
    Returns:
        List of answer values (1-5)
    """
    return [draw(likert_value) for _ in range(num_answers)]


@composite
def iq_answers_with_weights(draw, num_questions: int):
    """
    Generate IQ answers with corresponding difficulty weights.
    
    Args:
        draw: Hypothesis draw function
        num_questions: Number of questions
    
    Returns:
        Tuple of (weights list, correctness list)
    """
    weights = [draw(difficulty_weight) for _ in range(num_questions)]
    correctness = [draw(correctness_value) for _ in range(num_questions)]
    return weights, correctness
