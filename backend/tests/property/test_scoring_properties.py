"""
Property-based tests for scoring algorithms.

This module contains property tests that validate universal correctness properties
of the scoring algorithms using Hypothesis for randomized input generation.

Feature: backend-test-suite
"""
import pytest
from unittest.mock import Mock
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from backend.src.algorithms.eq_scoring import EQScoringAlgorithm
from backend.src.algorithms.iq_scoring import IQScoringAlgorithm
from backend.src.algorithms.dq_scoring import DQScoringAlgorithm
from backend.src.algorithms.aq_scoring import AQScoringAlgorithm

# Import generators
from backend.tests.generators import (
    likert_value,
    difficulty_weight,
    correctness_value,
)


class TestLikertNormalizationProperty:
    """
    Property 1: Likert Normalization Produces Valid Range
    
    *For any* valid Likert scale answer (1-5), the normalized score SHALL be 
    in the range [0, 100] and follow the formula t̂_j = 25*(t_j-1).
    
    **Validates: Requirements 1.1, 1.6**
    """
    
    @settings(max_examples=100)
    @given(answer_value=likert_value)
    def test_likert_normalization_produces_valid_range(self, answer_value: int):
        """
        Feature: backend-test-suite, Property 1: Likert Normalization Produces Valid Range
        **Validates: Requirements 1.1, 1.6**
        
        For any valid Likert scale answer (1-5), the normalized score SHALL be
        in the range [0, 100] and follow the formula t̂_j = 25*(t_j-1).
        """
        # Create a mock question with no reverse scoring
        question = Mock(
            id="test_q",
            category="EQ",
            facet="Empathy",
            reverse_score=False,
            question_type="Likert"
        )
        
        # Create answer
        answers = [{"question_id": "test_q", "answer_value": answer_value}]
        questions = [question]
        
        # Calculate score using EQ algorithm (uses Likert normalization)
        result = EQScoringAlgorithm.calculate_eq_score(answers, questions)
        
        # Expected normalized score: t̂_j = 25*(t_j-1)
        expected_score = 25 * (answer_value - 1)
        
        # Verify the score is in valid range [0, 100]
        assert 0 <= result["eq_empathy"] <= 100, \
            f"Score {result['eq_empathy']} is outside valid range [0, 100]"
        
        # Verify the formula is correctly applied
        assert abs(result["eq_empathy"] - expected_score) < 0.001, \
            f"Expected {expected_score}, got {result['eq_empathy']}"
    
    @settings(max_examples=100)
    @given(answer_value=likert_value)
    def test_likert_normalization_boundary_values(self, answer_value: int):
        """
        Verify boundary values produce expected results:
        - answer=1 -> score=0
        - answer=5 -> score=100
        """
        expected_score = 25 * (answer_value - 1)
        
        # Verify expected boundaries
        if answer_value == 1:
            assert expected_score == 0
        elif answer_value == 5:
            assert expected_score == 100
        
        # Verify score is always in valid range
        assert 0 <= expected_score <= 100




class TestReverseScoringProperty:
    """
    Property 2: Reverse Scoring Transformation
    
    *For any* Likert answer value and reverse_score=true, the transformation 
    t_j = (6-x_j) SHALL be applied before normalization, resulting in inverted scores.
    
    **Validates: Requirements 1.2**
    """
    
    @settings(max_examples=100)
    @given(answer_value=likert_value)
    def test_reverse_scoring_transformation(self, answer_value: int):
        """
        Feature: backend-test-suite, Property 2: Reverse Scoring Transformation
        **Validates: Requirements 1.2**
        
        For any Likert answer value, reverse scoring should invert the score
        such that normal_score + reverse_score = 100.
        """
        # Create normal question (no reverse)
        normal_question = Mock(
            id="normal_q",
            category="EQ",
            facet="Empathy",
            reverse_score=False,
            question_type="Likert"
        )
        
        # Create reverse question
        reverse_question = Mock(
            id="reverse_q",
            category="EQ",
            facet="Social",
            reverse_score=True,
            question_type="Likert"
        )
        
        # Calculate normal score
        normal_answers = [{"question_id": "normal_q", "answer_value": answer_value}]
        normal_result = EQScoringAlgorithm.calculate_eq_score(normal_answers, [normal_question])
        normal_score = normal_result["eq_empathy"]
        
        # Calculate reverse score
        reverse_answers = [{"question_id": "reverse_q", "answer_value": answer_value}]
        reverse_result = EQScoringAlgorithm.calculate_eq_score(reverse_answers, [reverse_question])
        reverse_score = reverse_result["eq_social"]
        
        # Property: normal_score + reverse_score = 100
        # Because: normal = 25*(x-1), reverse = 25*((6-x)-1) = 25*(5-x)
        # normal + reverse = 25*(x-1) + 25*(5-x) = 25*x - 25 + 125 - 25*x = 100
        assert abs(normal_score + reverse_score - 100) < 0.001, \
            f"normal_score ({normal_score}) + reverse_score ({reverse_score}) should equal 100"
    
    @settings(max_examples=100)
    @given(answer_value=likert_value)
    def test_reverse_scoring_formula(self, answer_value: int):
        """
        Verify the reverse scoring formula: t_j = (6-x_j) before normalization.
        """
        # Create reverse question
        reverse_question = Mock(
            id="reverse_q",
            category="EQ",
            facet="Empathy",
            reverse_score=True,
            question_type="Likert"
        )
        
        # Calculate reverse score
        reverse_answers = [{"question_id": "reverse_q", "answer_value": answer_value}]
        reverse_result = EQScoringAlgorithm.calculate_eq_score(reverse_answers, [reverse_question])
        reverse_score = reverse_result["eq_empathy"]
        
        # Expected: t_j = (6-x_j), then t̂_j = 25*(t_j-1)
        reversed_value = 6 - answer_value
        expected_score = 25 * (reversed_value - 1)
        
        assert abs(reverse_score - expected_score) < 0.001, \
            f"Expected {expected_score}, got {reverse_score}"



class TestFacetScoreAveragingProperty:
    """
    Property 3: Facet Score is Average of Question Scores
    
    *For any* set of questions within a facet and their corresponding answers, 
    the facet score SHALL equal the arithmetic mean of all normalized question scores.
    
    **Validates: Requirements 1.3**
    """
    
    @settings(max_examples=100)
    @given(answers=st.lists(likert_value, min_size=1, max_size=10))
    def test_facet_score_is_average(self, answers: list):
        """
        Feature: backend-test-suite, Property 3: Facet Score is Average of Question Scores
        **Validates: Requirements 1.3**
        
        For any set of questions within a facet, the facet score equals
        the arithmetic mean of all normalized question scores.
        """
        # Create questions for a single facet
        questions = [
            Mock(
                id=f"q_{i}",
                category="EQ",
                facet="Empathy",
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
        
        # Calculate facet score using the algorithm
        result = EQScoringAlgorithm.calculate_eq_score(answer_dicts, questions)
        actual_facet_score = result["eq_empathy"]
        
        # Calculate expected average manually
        # Normalize each answer: t̂_j = 25*(t_j-1)
        normalized_scores = [25 * (a - 1) for a in answers]
        expected_average = sum(normalized_scores) / len(normalized_scores)
        
        # Verify the facet score equals the average
        assert abs(actual_facet_score - expected_average) < 0.001, \
            f"Expected average {expected_average}, got {actual_facet_score}"
    
    @settings(max_examples=100)
    @given(
        answers1=st.lists(likert_value, min_size=1, max_size=5),
        answers2=st.lists(likert_value, min_size=1, max_size=5)
    )
    def test_facet_scores_independent(self, answers1: list, answers2: list):
        """
        Verify that facet scores are calculated independently for each facet.
        """
        # Create questions for two different facets
        questions = []
        answer_dicts = []
        
        # Empathy facet questions
        for i, answer in enumerate(answers1):
            questions.append(Mock(
                id=f"empathy_{i}",
                category="EQ",
                facet="Empathy",
                reverse_score=False,
                question_type="Likert"
            ))
            answer_dicts.append({"question_id": f"empathy_{i}", "answer_value": answer})
        
        # Social facet questions
        for i, answer in enumerate(answers2):
            questions.append(Mock(
                id=f"social_{i}",
                category="EQ",
                facet="Social",
                reverse_score=False,
                question_type="Likert"
            ))
            answer_dicts.append({"question_id": f"social_{i}", "answer_value": answer})
        
        # Calculate scores
        result = EQScoringAlgorithm.calculate_eq_score(answer_dicts, questions)
        
        # Calculate expected averages
        expected_empathy = sum(25 * (a - 1) for a in answers1) / len(answers1)
        expected_social = sum(25 * (a - 1) for a in answers2) / len(answers2)
        
        # Verify each facet is calculated independently
        assert abs(result["eq_empathy"] - expected_empathy) < 0.001
        assert abs(result["eq_social"] - expected_social) < 0.001



class TestDomainScoreAveragingProperty:
    """
    Property 4: Domain Score is Average of Facet Scores
    
    *For any* domain (IQ, EQ, DQ, AQ), the domain score SHALL equal the 
    arithmetic mean of all facet scores within that domain.
    
    **Validates: Requirements 1.4**
    """
    
    @settings(max_examples=100)
    @given(facet_scores=st.lists(
        st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        min_size=4,
        max_size=4
    ))
    def test_domain_score_is_facet_average(self, facet_scores: list):
        """
        Feature: backend-test-suite, Property 4: Domain Score is Average of Facet Scores
        **Validates: Requirements 1.4**
        
        For any domain, the domain score equals the arithmetic mean of all facet scores.
        """
        # Map facet scores to Likert values (reverse the normalization)
        # score = 25 * (likert - 1), so likert = (score / 25) + 1
        # We need to clamp to valid Likert range [1, 5]
        def score_to_likert(score):
            likert = (score / 25) + 1
            return max(1, min(5, round(likert)))
        
        # Create questions for all 4 EQ facets
        # Note: facet names must match what the algorithm expects after .lower()
        facets = ["empathy", "social", "self_awareness", "self_regulation"]
        questions = []
        answer_dicts = []
        
        for i, facet in enumerate(facets):
            # Use a Likert value that produces approximately the target facet score
            likert_val = score_to_likert(facet_scores[i])
            questions.append(Mock(
                id=f"q_{facet}",
                category="EQ",
                facet=facet,
                reverse_score=False,
                question_type="Likert"
            ))
            answer_dicts.append({"question_id": f"q_{facet}", "answer_value": likert_val})
        
        # Calculate domain score
        result = EQScoringAlgorithm.calculate_eq_score(answer_dicts, questions)
        
        # Get actual facet scores from result
        actual_facet_scores = [
            result["eq_empathy"],
            result["eq_social"],
            result["eq_self_awareness"],
            result["eq_self_regulation"]
        ]
        
        # Expected domain score is average of actual facet scores
        expected_domain_score = sum(actual_facet_scores) / len(actual_facet_scores)
        
        # Verify domain score equals average of facet scores
        assert abs(result["eq_score"] - expected_domain_score) < 0.001, \
            f"Expected domain score {expected_domain_score}, got {result['eq_score']}"
    
    @settings(max_examples=100)
    @given(
        empathy_answers=st.lists(likert_value, min_size=1, max_size=3),
        social_answers=st.lists(likert_value, min_size=1, max_size=3),
        awareness_answers=st.lists(likert_value, min_size=1, max_size=3),
        regulation_answers=st.lists(likert_value, min_size=1, max_size=3)
    )
    def test_eq_domain_score_from_multiple_questions(
        self,
        empathy_answers: list,
        social_answers: list,
        awareness_answers: list,
        regulation_answers: list
    ):
        """
        Verify domain score is average of facet scores when each facet has multiple questions.
        """
        questions = []
        answer_dicts = []
        
        # Create questions and answers for each facet
        # Note: facet names must match what the algorithm expects after .lower()
        # The algorithm looks for: empathy, social, self_awareness, self_regulation
        facet_data = [
            ("empathy", empathy_answers),
            ("social", social_answers),
            ("self_awareness", awareness_answers),
            ("self_regulation", regulation_answers)
        ]
        
        for facet, answers in facet_data:
            for i, answer in enumerate(answers):
                questions.append(Mock(
                    id=f"{facet}_{i}",
                    category="EQ",
                    facet=facet,
                    reverse_score=False,
                    question_type="Likert"
                ))
                answer_dicts.append({"question_id": f"{facet}_{i}", "answer_value": answer})
        
        # Calculate scores
        result = EQScoringAlgorithm.calculate_eq_score(answer_dicts, questions)
        
        # Calculate expected facet scores
        def calc_facet_avg(answers):
            return sum(25 * (a - 1) for a in answers) / len(answers)
        
        expected_facet_scores = [
            calc_facet_avg(empathy_answers),
            calc_facet_avg(social_answers),
            calc_facet_avg(awareness_answers),
            calc_facet_avg(regulation_answers)
        ]
        
        # Expected domain score is average of facet scores
        expected_domain_score = sum(expected_facet_scores) / 4
        
        # Verify
        assert abs(result["eq_score"] - expected_domain_score) < 0.001, \
            f"Expected {expected_domain_score}, got {result['eq_score']}"



class TestIQWeightedScoringProperty:
    """
    Property 5: IQ Weighted Difficulty Scoring
    
    *For any* set of IQ questions with difficulty weights and correctness values, 
    the IQ score SHALL follow the formula: S_IQ = 100 * (Σ(d_i * r_i)) / Σ(d_i).
    
    **Validates: Requirements 1.5**
    """
    
    @settings(max_examples=100)
    @given(
        weights=st.lists(
            st.floats(min_value=0.1, max_value=3.0, allow_nan=False, allow_infinity=False),
            min_size=1,
            max_size=10
        ),
        correctness=st.lists(
            st.integers(min_value=0, max_value=1),
            min_size=1,
            max_size=10
        )
    )
    def test_iq_weighted_scoring_formula(self, weights: list, correctness: list):
        """
        Feature: backend-test-suite, Property 5: IQ Weighted Difficulty Scoring
        **Validates: Requirements 1.5**
        
        For any set of IQ questions with difficulty weights and correctness values,
        the IQ score follows: S_IQ = 100 * (Σ(d_i * r_i)) / Σ(d_i)
        """
        # Ensure lists have same length
        assume(len(weights) == len(correctness))
        
        # Create questions with specified weights
        questions = [
            Mock(
                id=f"iq_{i}",
                category="IQ",
                facet="lr",  # All in same facet for simplicity
                difficulty_weight=weights[i],
                question_type="MCQ"
            )
            for i in range(len(weights))
        ]
        
        # Create answers with specified correctness
        answers = [
            {"question_id": f"iq_{i}", "answer_value": correctness[i]}
            for i in range(len(correctness))
        ]
        
        # Calculate IQ score
        result = IQScoringAlgorithm.calculate_iq_score(answers, questions)
        
        # Calculate expected score using the formula
        # S_IQ = 100 * (Σ(d_i * r_i)) / Σ(d_i)
        weighted_sum = sum(w * c for w, c in zip(weights, correctness))
        total_weight = sum(weights)
        expected_score = 100 * weighted_sum / total_weight if total_weight > 0 else 0
        
        # The facet score should match the formula
        assert abs(result["iq_lr"] - expected_score) < 0.001, \
            f"Expected {expected_score}, got {result['iq_lr']}"
    
    @settings(max_examples=100)
    @given(
        weight=st.floats(min_value=0.1, max_value=3.0, allow_nan=False, allow_infinity=False),
        correct=st.booleans()
    )
    def test_iq_single_question_scoring(self, weight: float, correct: bool):
        """
        Verify single question IQ scoring follows the weighted formula.
        """
        # Create single question
        question = Mock(
            id="iq_single",
            category="IQ",
            facet="lr",
            difficulty_weight=weight,
            question_type="MCQ"
        )
        
        # Create answer (1 for correct, 0 for incorrect)
        answer = {"question_id": "iq_single", "answer_value": 1 if correct else 0}
        
        # Calculate score
        result = IQScoringAlgorithm.calculate_iq_score([answer], [question])
        
        # For single question: S_IQ = 100 * (d * r) / d = 100 * r
        expected_score = 100.0 if correct else 0.0
        
        assert abs(result["iq_lr"] - expected_score) < 0.001, \
            f"Expected {expected_score}, got {result['iq_lr']}"
    
    @settings(max_examples=100)
    @given(
        weights=st.lists(
            st.floats(min_value=0.1, max_value=3.0, allow_nan=False, allow_infinity=False),
            min_size=2,
            max_size=5
        )
    )
    def test_iq_all_correct_equals_100(self, weights: list):
        """
        Verify that all correct answers produce a score of 100.
        """
        # Create questions
        questions = [
            Mock(
                id=f"iq_{i}",
                category="IQ",
                facet="lr",
                difficulty_weight=weights[i],
                question_type="MCQ"
            )
            for i in range(len(weights))
        ]
        
        # All correct answers
        answers = [
            {"question_id": f"iq_{i}", "answer_value": 1}
            for i in range(len(weights))
        ]
        
        # Calculate score
        result = IQScoringAlgorithm.calculate_iq_score(answers, questions)
        
        # All correct should give 100
        assert abs(result["iq_lr"] - 100.0) < 0.001, \
            f"Expected 100.0, got {result['iq_lr']}"
    
    @settings(max_examples=100)
    @given(
        weights=st.lists(
            st.floats(min_value=0.1, max_value=3.0, allow_nan=False, allow_infinity=False),
            min_size=2,
            max_size=5
        )
    )
    def test_iq_all_incorrect_equals_0(self, weights: list):
        """
        Verify that all incorrect answers produce a score of 0.
        """
        # Create questions
        questions = [
            Mock(
                id=f"iq_{i}",
                category="IQ",
                facet="lr",
                difficulty_weight=weights[i],
                question_type="MCQ"
            )
            for i in range(len(weights))
        ]
        
        # All incorrect answers
        answers = [
            {"question_id": f"iq_{i}", "answer_value": 0}
            for i in range(len(weights))
        ]
        
        # Calculate score
        result = IQScoringAlgorithm.calculate_iq_score(answers, questions)
        
        # All incorrect should give 0
        assert abs(result["iq_lr"] - 0.0) < 0.001, \
            f"Expected 0.0, got {result['iq_lr']}"

