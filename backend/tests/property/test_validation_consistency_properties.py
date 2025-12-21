"""
Property-based tests for validation and consistency algorithms.

This module contains property tests that validate:
- Answer validation completeness (Property 16)
- Algorithm determinism (Property 17)

Feature: backend-test-suite
"""
import pytest
from unittest.mock import Mock
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from backend.src.utils.validation import AnswerValidator
from backend.src.algorithms.ikigai_calculation import IkigaiCalculationAlgorithm
from backend.src.algorithms.career_mapping import CareerMappingAlgorithm
from backend.src.algorithms.eq_scoring import EQScoringAlgorithm
from backend.src.models.profile_vector import ProfileVector

# Import generators
from backend.tests.generators import (
    profile_vector_scores,
    likert_value,
)


# ============================================================================
# Helper Functions
# ============================================================================

def create_mock_question(question_id: str, category: str = "EQ", is_active: bool = True):
    """Create a mock question object."""
    question = Mock()
    question.id = question_id
    question.category = category
    question.facet = "Empathy"
    question.question_type = "Likert" if category != "IQ" else "MCQ"
    question.is_active = is_active
    question.reverse_score = False
    question.difficulty_weight = 1.0
    return question


def create_mock_answer(question_id: str, value: int = 3):
    """Create a mock answer object."""
    answer = Mock()
    answer.question_id = question_id
    answer.answer_value = value
    answer.answer_text = None
    return answer


def create_mock_profile_vector(scores: list) -> Mock:
    """Create a mock ProfileVector with given scores."""
    pv = Mock(spec=ProfileVector)
    pv.to_vector.return_value = scores
    return pv


def create_mock_career_rule(
    career_name: str,
    is_active: bool = True
) -> Mock:
    """Create a mock CareerRule with given attributes."""
    facet_keys = [
        'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
        'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
        'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
        'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
    ]
    
    weights = {key: 0.5 for key in facet_keys}
    thresholds = {key: 20.0 for key in facet_keys}
    
    rule = Mock()
    rule.career_name = career_name
    rule.is_active = is_active
    rule.weights = weights
    rule.thresholds = thresholds
    rule.bonus_keys = []
    
    return rule


class TestAnswerValidationCompletenessProperty:
    """
    Property 16: Answer Validation Completeness
    
    *For any* set of required questions, validation SHALL return true only if 
    all required questions have answers.
    
    **Validates: Requirements 9.1, 9.2**
    """
    
    @settings(max_examples=100)
    @given(
        num_questions=st.integers(min_value=1, max_value=20),
        num_answers=st.integers(min_value=0, max_value=20)
    )
    def test_answer_validation_completeness(self, num_questions: int, num_answers: int):
        """
        Feature: backend-test-suite, Property 16: Answer Validation Completeness
        **Validates: Requirements 9.1, 9.2**
        
        For any set of required questions, validation returns true only if
        all required questions have answers.
        """
        # Create questions
        questions = [
            create_mock_question(f"q{i}", category="EQ", is_active=True)
            for i in range(num_questions)
        ]
        
        # Create answers (may be fewer or more than questions)
        answers = [
            create_mock_answer(f"q{i}", value=3)
            for i in range(min(num_answers, num_questions))
        ]
        
        # Validate completeness
        result = AnswerValidator.validate_completeness(answers, questions)
        
        # Property: validation returns true only if all required questions have answers
        if num_answers >= num_questions:
            assert result == True, \
                f"Expected True when answers ({num_answers}) >= questions ({num_questions})"
        else:
            assert result == False, \
                f"Expected False when answers ({num_answers}) < questions ({num_questions})"
    
    @settings(max_examples=100)
    @given(num_questions=st.integers(min_value=1, max_value=10))
    def test_all_questions_answered_returns_true(self, num_questions: int):
        """
        Verify that when all questions are answered, validation returns true.
        """
        # Create questions
        questions = [
            create_mock_question(f"q{i}", category="EQ", is_active=True)
            for i in range(num_questions)
        ]
        
        # Create answers for all questions
        answers = [
            create_mock_answer(f"q{i}", value=3)
            for i in range(num_questions)
        ]
        
        result = AnswerValidator.validate_completeness(answers, questions)
        
        assert result == True, \
            f"Expected True when all {num_questions} questions are answered"
    
    @settings(max_examples=100)
    @given(
        num_questions=st.integers(min_value=2, max_value=10),
        missing_count=st.integers(min_value=1, max_value=5)
    )
    def test_missing_answers_returns_false(self, num_questions: int, missing_count: int):
        """
        Verify that when some questions are not answered, validation returns false.
        """
        # Ensure we don't try to miss more questions than we have
        actual_missing = min(missing_count, num_questions - 1)
        assume(actual_missing > 0)
        
        # Create questions
        questions = [
            create_mock_question(f"q{i}", category="EQ", is_active=True)
            for i in range(num_questions)
        ]
        
        # Create answers for only some questions (missing some)
        num_answers = num_questions - actual_missing
        answers = [
            create_mock_answer(f"q{i}", value=3)
            for i in range(num_answers)
        ]
        
        result = AnswerValidator.validate_completeness(answers, questions)
        
        assert result == False, \
            f"Expected False when {actual_missing} questions are missing answers"
    
    def test_empty_answers_returns_false(self):
        """
        Verify that empty answers list returns false.
        **Validates: Requirements 9.3**
        """
        questions = [
            create_mock_question(f"q{i}", category="EQ", is_active=True)
            for i in range(5)
        ]
        
        result = AnswerValidator.validate_completeness([], questions)
        
        assert result == False, "Expected False for empty answers list"
    
    def test_empty_questions_returns_false(self):
        """
        Verify that empty questions list returns false.
        **Validates: Requirements 9.4**
        """
        answers = [
            create_mock_answer(f"q{i}", value=3)
            for i in range(5)
        ]
        
        result = AnswerValidator.validate_completeness(answers, [])
        
        assert result == False, "Expected False for empty questions list"


class TestAlgorithmDeterminismProperty:
    """
    Property 17: Algorithm Determinism
    
    *For any* valid inputs, multiple calls to scoring, Ikigai, and career mapping 
    algorithms with identical inputs SHALL produce identical outputs.
    
    **Validates: Requirements 10.1, 10.2, 10.3**
    """
    
    @settings(max_examples=100)
    @given(profile_scores=profile_vector_scores())
    def test_ikigai_algorithm_determinism(self, profile_scores: list):
        """
        Feature: backend-test-suite, Property 17: Algorithm Determinism (Ikigai)
        **Validates: Requirements 10.2**
        
        For any valid profile vector, multiple calls to Ikigai algorithm
        with identical inputs produce identical outputs.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Call Ikigai calculation multiple times
        result1 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        result2 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        result3 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        
        # All results should be identical
        assert result1 == result2, \
            f"Ikigai results differ between call 1 and 2: {result1} vs {result2}"
        assert result2 == result3, \
            f"Ikigai results differ between call 2 and 3: {result2} vs {result3}"
    
    @settings(max_examples=100)
    @given(profile_scores=profile_vector_scores())
    def test_career_mapping_algorithm_determinism(self, profile_scores: list):
        """
        Feature: backend-test-suite, Property 17: Algorithm Determinism (Career Mapping)
        **Validates: Requirements 10.3**
        
        For any valid profile vector and career rules, multiple calls to 
        career mapping algorithm with identical inputs produce identical outputs.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create consistent career rules
        rules = [
            create_mock_career_rule(f"Career_{i}", is_active=True)
            for i in range(5)
        ]
        
        # Call career mapping multiple times
        result1 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        result2 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        result3 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # All results should be identical
        assert len(result1) == len(result2) == len(result3), \
            f"Career mapping result lengths differ: {len(result1)}, {len(result2)}, {len(result3)}"
        
        for i in range(len(result1)):
            assert result1[i]['career_name'] == result2[i]['career_name'] == result3[i]['career_name'], \
                f"Career names differ at index {i}"
            assert result1[i]['fit_score'] == result2[i]['fit_score'] == result3[i]['fit_score'], \
                f"Fit scores differ at index {i}: {result1[i]['fit_score']}, {result2[i]['fit_score']}, {result3[i]['fit_score']}"
    
    @settings(max_examples=100)
    @given(answers=st.lists(likert_value, min_size=1, max_size=10))
    def test_scoring_algorithm_determinism(self, answers: list):
        """
        Feature: backend-test-suite, Property 17: Algorithm Determinism (Scoring)
        **Validates: Requirements 10.1**
        
        For any valid answers and questions, multiple calls to scoring algorithm
        with identical inputs produce identical outputs.
        """
        # Create questions for a single facet
        questions = [
            Mock(
                id=f"q_{i}",
                category="EQ",
                facet="empathy",
                reverse_score=False,
                question_type="Likert"
            )
            for i in range(len(answers))
        ]
        
        # Create answer dictionaries
        answer_dicts = [
            {"question_id": f"q_{i}", "answer_value": answer}
            for i, answer in enumerate(answers)
        ]
        
        # Call scoring algorithm multiple times
        result1 = EQScoringAlgorithm.calculate_eq_score(answer_dicts, questions)
        result2 = EQScoringAlgorithm.calculate_eq_score(answer_dicts, questions)
        result3 = EQScoringAlgorithm.calculate_eq_score(answer_dicts, questions)
        
        # All results should be identical
        assert result1 == result2, \
            f"Scoring results differ between call 1 and 2: {result1} vs {result2}"
        assert result2 == result3, \
            f"Scoring results differ between call 2 and 3: {result2} vs {result3}"
    
    @settings(max_examples=100)
    @given(profile_scores=profile_vector_scores())
    def test_combined_algorithm_determinism(self, profile_scores: list):
        """
        Verify that all algorithms together produce deterministic results.
        """
        pv = create_mock_profile_vector(profile_scores)
        rules = [
            create_mock_career_rule(f"Career_{i}", is_active=True)
            for i in range(3)
        ]
        
        # First run
        ikigai1 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        career1 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # Second run
        ikigai2 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        career2 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # Results should be identical
        assert ikigai1 == ikigai2, "Ikigai results not deterministic"
        assert len(career1) == len(career2), "Career result lengths differ"
        
        for i in range(len(career1)):
            assert career1[i]['fit_score'] == career2[i]['fit_score'], \
                f"Career fit scores differ at index {i}"
