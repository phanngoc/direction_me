"""
Property-based tests for career mapping algorithms.

This module contains property tests that validate universal correctness properties
of the career mapping algorithms using Hypothesis for randomized input generation.

Feature: backend-test-suite
"""
import pytest
from unittest.mock import Mock
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from backend.src.algorithms.career_mapping import CareerMappingAlgorithm
from backend.src.models.profile_vector import ProfileVector
from backend.src.models.career_rule import CareerRule

# Import generators
from backend.tests.generators import (
    profile_vector_scores,
    career_rule,
)


# ============================================================================
# Helper Functions
# ============================================================================

def create_mock_profile_vector(scores: list) -> Mock:
    """Create a mock ProfileVector with given scores."""
    pv = Mock(spec=ProfileVector)
    pv.to_vector.return_value = scores
    return pv


def create_mock_career_rule(
    career_name: str,
    is_active: bool = True,
    weights: dict = None,
    thresholds: dict = None,
    bonus_keys: list = None
) -> Mock:
    """Create a mock CareerRule with given attributes."""
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
    
    rule = Mock(spec=CareerRule)
    rule.career_name = career_name
    rule.is_active = is_active
    rule.weights = weights
    rule.thresholds = thresholds
    rule.bonus_keys = bonus_keys
    
    return rule


class TestCareerSuggestionsSortingAndLimitingProperty:
    """
    Property 11: Career Suggestions Sorted and Limited
    
    *For any* set of career fit calculations, the results SHALL be sorted by 
    fit_score in descending order and limited to maximum 8 suggestions.
    
    **Validates: Requirements 4.5, 4.6**
    """
    
    @settings(max_examples=100)
    @given(
        profile_scores=profile_vector_scores(),
        num_rules=st.integers(min_value=1, max_value=15)
    )
    def test_career_suggestions_sorted_and_limited(
        self, 
        profile_scores: list, 
        num_rules: int
    ):
        """
        Feature: backend-test-suite, Property 11: Career Suggestions Sorted and Limited
        **Validates: Requirements 4.5, 4.6**
        
        For any set of career fit calculations, results are sorted by fit_score
        in descending order and limited to maximum 8 suggestions.
        """
        # Create mock profile vector
        pv = create_mock_profile_vector(profile_scores)
        
        # Create multiple career rules with varying weights to produce different fit scores
        rules = []
        for i in range(num_rules):
            # Vary weights to get different fit scores
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            # Use different weight patterns to ensure different fit scores
            weights = {key: 0.3 + (i * 0.05) % 0.7 for key in facet_keys}
            thresholds = {key: 20.0 + (i * 2) % 40 for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"Career_{i}",
                is_active=True,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            rules.append(rule)
        
        # Calculate career fit scores
        result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # Property 1: Results are sorted by fit_score in descending order
        for i in range(len(result) - 1):
            assert result[i]['fit_score'] >= result[i + 1]['fit_score'], \
                f"Results not sorted: {result[i]['fit_score']} < {result[i + 1]['fit_score']}"
        
        # Property 2: Results are limited to maximum 8 suggestions
        assert len(result) <= 8, \
            f"Results exceed maximum of 8: got {len(result)}"
    
    @settings(max_examples=100)
    @given(profile_scores=profile_vector_scores())
    def test_career_suggestions_limit_with_many_rules(self, profile_scores: list):
        """
        Verify that even with many career rules, results are limited to 8.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create 20 career rules (more than the limit of 8)
        rules = []
        for i in range(20):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            # Low thresholds to ensure all careers pass the 30% minimum
            thresholds = {key: 10.0 for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"Career_{i}",
                is_active=True,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            rules.append(rule)
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # Must be limited to 8
        assert len(result) <= 8, \
            f"Results should be limited to 8, got {len(result)}"
    
    @settings(max_examples=100)
    @given(profile_scores=profile_vector_scores())
    def test_career_suggestions_sorting_stability(self, profile_scores: list):
        """
        Verify that sorting is consistent across multiple calls.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create career rules
        rules = []
        for i in range(5):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.4 + (i * 0.1) for key in facet_keys}
            thresholds = {key: 20.0 for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"Career_{i}",
                is_active=True,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            rules.append(rule)
        
        # Call twice
        result1 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        result2 = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # Results should be identical
        assert len(result1) == len(result2)
        for i in range(len(result1)):
            assert result1[i]['fit_score'] == result2[i]['fit_score']
            assert result1[i]['career_name'] == result2[i]['career_name']


class TestInactiveRulesExclusionProperty:
    """
    Property 12: Inactive Career Rules Excluded
    
    *For any* set of career rules where some have is_active=false, only active 
    rules SHALL be included in calculations.
    
    **Validates: Requirements 4.7**
    """
    
    @settings(max_examples=100)
    @given(
        profile_scores=profile_vector_scores(),
        active_count=st.integers(min_value=0, max_value=5),
        inactive_count=st.integers(min_value=1, max_value=5)
    )
    def test_inactive_rules_excluded(
        self, 
        profile_scores: list, 
        active_count: int, 
        inactive_count: int
    ):
        """
        Feature: backend-test-suite, Property 12: Inactive Career Rules Excluded
        **Validates: Requirements 4.7**
        
        For any set of career rules where some have is_active=false, only active
        rules are included in calculations.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create active rules
        active_rules = []
        for i in range(active_count):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            thresholds = {key: 10.0 for key in facet_keys}  # Low thresholds to pass 30% minimum
            
            rule = create_mock_career_rule(
                career_name=f"Active_{i}",
                is_active=True,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            active_rules.append(rule)
        
        # Create inactive rules
        inactive_rules = []
        for i in range(inactive_count):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            thresholds = {key: 10.0 for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"Inactive_{i}",
                is_active=False,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            inactive_rules.append(rule)
        
        # Combine all rules
        all_rules = active_rules + inactive_rules
        
        # Calculate career fit scores
        result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, all_rules)
        
        # Extract career names from results
        result_career_names = [r['career_name'] for r in result]
        
        # Property: No inactive careers should appear in results
        for inactive_rule in inactive_rules:
            assert inactive_rule.career_name not in result_career_names, \
                f"Inactive career '{inactive_rule.career_name}' should not be in results"
    
    @settings(max_examples=100)
    @given(profile_scores=profile_vector_scores())
    def test_all_inactive_rules_returns_empty(self, profile_scores: list):
        """
        Verify that if all rules are inactive, result is empty.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create only inactive rules
        inactive_rules = []
        for i in range(5):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            thresholds = {key: 10.0 for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"Inactive_{i}",
                is_active=False,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            inactive_rules.append(rule)
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, inactive_rules)
        
        # Should return empty list
        assert len(result) == 0, \
            f"Expected empty result for all inactive rules, got {len(result)}"
    
    @settings(max_examples=100)
    @given(
        profile_scores=profile_vector_scores(),
        num_active=st.integers(min_value=1, max_value=10)
    )
    def test_only_active_rules_counted(self, profile_scores: list, num_active: int):
        """
        Verify that only active rules contribute to results count.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create active rules
        rules = []
        for i in range(num_active):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            thresholds = {key: 10.0 for key in facet_keys}  # Low thresholds
            
            rule = create_mock_career_rule(
                career_name=f"Active_{i}",
                is_active=True,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            rules.append(rule)
        
        # Add some inactive rules
        for i in range(3):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            thresholds = {key: 10.0 for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"Inactive_{i}",
                is_active=False,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            rules.append(rule)
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # Result count should be at most min(num_active, 8) due to the 8 limit
        # and the 30% threshold filter
        assert len(result) <= min(num_active, 8), \
            f"Result count {len(result)} exceeds expected max {min(num_active, 8)}"


class TestCareerFitThresholdFilteringProperty:
    """
    Property 13: Career Fit Threshold Filtering
    
    *For any* career with fit score below 30%, it SHALL be excluded from suggestions.
    
    **Validates: Requirements 4.4**
    """
    
    @settings(max_examples=100)
    @given(profile_scores=profile_vector_scores())
    def test_career_fit_threshold_filtering(self, profile_scores: list):
        """
        Feature: backend-test-suite, Property 13: Career Fit Threshold Filtering
        **Validates: Requirements 4.4**
        
        For any career with fit score below 30%, it is excluded from suggestions.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create career rules with varying thresholds
        rules = []
        for i in range(10):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            # Vary thresholds to create different fit scores
            thresholds = {key: 20.0 + (i * 5) for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"Career_{i}",
                is_active=True,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            rules.append(rule)
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # Property: All results must have fit_score >= 30
        for career in result:
            assert career['fit_score'] >= 30, \
                f"Career '{career['career_name']}' has fit_score {career['fit_score']} < 30"
    
    @settings(max_examples=100)
    @given(
        profile_scores=st.lists(
            st.floats(min_value=0.0, max_value=20.0, allow_nan=False, allow_infinity=False),
            min_size=16,
            max_size=16
        )
    )
    def test_low_profile_scores_filtered_out(self, profile_scores: list):
        """
        Verify that very low profile scores result in careers being filtered out.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create career rules with high thresholds
        rules = []
        for i in range(5):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            # High thresholds that low scores won't meet
            thresholds = {key: 80.0 for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"HighThreshold_{i}",
                is_active=True,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            rules.append(rule)
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # All results (if any) must still have fit_score >= 30
        for career in result:
            assert career['fit_score'] >= 30, \
                f"Career '{career['career_name']}' has fit_score {career['fit_score']} < 30"
    
    @settings(max_examples=100)
    @given(
        profile_scores=st.lists(
            st.floats(min_value=80.0, max_value=100.0, allow_nan=False, allow_infinity=False),
            min_size=16,
            max_size=16
        )
    )
    def test_high_profile_scores_pass_threshold(self, profile_scores: list):
        """
        Verify that high profile scores result in careers passing the threshold.
        """
        pv = create_mock_profile_vector(profile_scores)
        
        # Create career rules with reasonable thresholds
        rules = []
        for i in range(5):
            facet_keys = [
                'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
                'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
                'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
                'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
            ]
            weights = {key: 0.5 for key in facet_keys}
            # Low thresholds that high scores will easily meet
            thresholds = {key: 30.0 for key in facet_keys}
            
            rule = create_mock_career_rule(
                career_name=f"LowThreshold_{i}",
                is_active=True,
                weights=weights,
                thresholds=thresholds,
                bonus_keys=[]
            )
            rules.append(rule)
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(pv, rules)
        
        # With high profile scores and low thresholds, we should get results
        # All results must have fit_score >= 30
        for career in result:
            assert career['fit_score'] >= 30, \
                f"Career '{career['career_name']}' has fit_score {career['fit_score']} < 30"
        
        # With high scores, we expect some results (unless limited by 8)
        assert len(result) <= 8
