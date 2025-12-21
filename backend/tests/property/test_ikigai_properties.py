"""
Property-based tests for Ikigai calculation algorithms.

This module contains property tests that validate universal correctness properties
of the Ikigai calculation algorithms using Hypothesis for randomized input generation.

Feature: backend-test-suite
"""
import pytest
import math
from unittest.mock import Mock
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from backend.src.algorithms.ikigai_calculation import IkigaiCalculationAlgorithm
from backend.src.models.profile_vector import ProfileVector

# Import generators
from backend.tests.generators import (
    profile_vector_scores,
    profile_vector_scores_positive,
    score_value,
)


class TestIkigaiAxisFormulasProperty:
    """
    Property 8: Ikigai Axis Formulas
    
    *For any* valid profile vector, the Ikigai axis scores SHALL be calculated 
    using the correct formulas:
    - love = (eq_empathy + eq_social + dq_creativity) / 3
    - good_at = (iq_lr + iq_nr + iq_vr + iq_sr) / 4
    - world_needs = (dq_info_literacy + dq_safety + aq_control + aq_ownership) / 4
    - paid_for = (aq_reach + aq_endurance + eq_self_awareness + eq_self_regulation) / 4
    
    **Validates: Requirements 3.1, 3.2, 3.3, 3.4**
    """
    
    @settings(max_examples=100)
    @given(scores=profile_vector_scores())
    def test_ikigai_axis_formulas(self, scores: list):
        """
        Feature: backend-test-suite, Property 8: Ikigai Axis Formulas
        **Validates: Requirements 3.1, 3.2, 3.3, 3.4**
        
        For any valid profile vector, the Ikigai axis scores are calculated
        using the correct formulas for love, good_at, world_needs, and paid_for.
        """
        # Create mock profile vector with the generated scores
        # Profile vector indices:
        # [0-3]: IQ (lr, nr, vr, sr)
        # [4-7]: EQ (empathy, social, self_awareness, self_regulation)
        # [8-11]: DQ (info_literacy, creativity, safety, collaboration)
        # [12-15]: AQ (control, ownership, reach, endurance)
        pv = Mock(spec=ProfileVector)
        pv.to_vector.return_value = scores
        
        # Calculate Ikigai scores
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        
        # Verify love axis: (eq_empathy + eq_social + dq_creativity) / 3
        # eq_empathy = scores[4], eq_social = scores[5], dq_creativity = scores[9]
        expected_love = (scores[4] + scores[5] + scores[9]) / 3
        assert abs(result['ikigai_love'] - expected_love) < 0.001, \
            f"Love axis: expected {expected_love}, got {result['ikigai_love']}"
        
        # Verify good_at axis: (iq_lr + iq_nr + iq_vr + iq_sr) / 4
        # iq_lr = scores[0], iq_nr = scores[1], iq_vr = scores[2], iq_sr = scores[3]
        expected_good_at = (scores[0] + scores[1] + scores[2] + scores[3]) / 4
        assert abs(result['ikigai_good_at'] - expected_good_at) < 0.001, \
            f"Good at axis: expected {expected_good_at}, got {result['ikigai_good_at']}"
        
        # Verify world_needs axis: (dq_info_literacy + dq_safety + aq_control + aq_ownership) / 4
        # dq_info_literacy = scores[8], dq_safety = scores[10], aq_control = scores[12], aq_ownership = scores[13]
        expected_world_needs = (scores[8] + scores[10] + scores[12] + scores[13]) / 4
        assert abs(result['ikigai_world_needs'] - expected_world_needs) < 0.001, \
            f"World needs axis: expected {expected_world_needs}, got {result['ikigai_world_needs']}"
        
        # Verify paid_for axis: (aq_reach + aq_endurance + eq_self_awareness + eq_self_regulation) / 4
        # aq_reach = scores[14], aq_endurance = scores[15], eq_self_awareness = scores[6], eq_self_regulation = scores[7]
        expected_paid_for = (scores[14] + scores[15] + scores[6] + scores[7]) / 4
        assert abs(result['ikigai_paid_for'] - expected_paid_for) < 0.001, \
            f"Paid for axis: expected {expected_paid_for}, got {result['ikigai_paid_for']}"
    
    @settings(max_examples=100)
    @given(scores=profile_vector_scores())
    def test_ikigai_axis_scores_in_valid_range(self, scores: list):
        """
        Verify that all Ikigai axis scores are within the valid range [0, 100].
        """
        pv = Mock(spec=ProfileVector)
        pv.to_vector.return_value = scores
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        
        # All axis scores should be in [0, 100]
        assert 0 <= result['ikigai_love'] <= 100, \
            f"Love axis {result['ikigai_love']} outside valid range"
        assert 0 <= result['ikigai_good_at'] <= 100, \
            f"Good at axis {result['ikigai_good_at']} outside valid range"
        assert 0 <= result['ikigai_world_needs'] <= 100, \
            f"World needs axis {result['ikigai_world_needs']} outside valid range"
        assert 0 <= result['ikigai_paid_for'] <= 100, \
            f"Paid for axis {result['ikigai_paid_for']} outside valid range"



class TestHarmonicMeanProperty:
    """
    Property 9: Harmonic Mean Formula
    
    *For any* four positive axis scores, the harmonic mean SHALL equal 
    4 / (1/love + 1/good_at + 1/world_needs + 1/paid_for).
    
    **Validates: Requirements 3.5**
    """
    
    @settings(max_examples=100)
    @given(
        love=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        good_at=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        world_needs=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        paid_for=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    def test_harmonic_mean_formula(self, love: float, good_at: float, world_needs: float, paid_for: float):
        """
        Feature: backend-test-suite, Property 9: Harmonic Mean Formula
        **Validates: Requirements 3.5**
        
        For any four positive axis scores, the harmonic mean equals
        4 / (1/love + 1/good_at + 1/world_needs + 1/paid_for).
        """
        # Calculate expected harmonic mean
        expected = 4 / (1/love + 1/good_at + 1/world_needs + 1/paid_for)
        
        # Calculate actual harmonic mean using the algorithm
        actual = IkigaiCalculationAlgorithm._calculate_harmonic_mean(
            love, good_at, world_needs, paid_for
        )
        
        assert abs(actual - expected) < 0.001, \
            f"Harmonic mean: expected {expected}, got {actual}"
    
    @settings(max_examples=100)
    @given(scores=profile_vector_scores_positive())
    def test_harmonic_mean_from_profile_vector(self, scores: list):
        """
        Verify harmonic mean is correctly calculated from profile vector.
        """
        pv = Mock(spec=ProfileVector)
        pv.to_vector.return_value = scores
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        
        # Get the axis scores
        love = result['ikigai_love']
        good_at = result['ikigai_good_at']
        world_needs = result['ikigai_world_needs']
        paid_for = result['ikigai_paid_for']
        
        # Skip if any axis is zero (harmonic mean returns 0 in that case)
        if any(score == 0 for score in [love, good_at, world_needs, paid_for]):
            assert result['ikigai_harmonic'] == 0.0
        else:
            # Calculate expected harmonic mean
            expected = 4 / (1/love + 1/good_at + 1/world_needs + 1/paid_for)
            assert abs(result['ikigai_harmonic'] - expected) < 0.001, \
                f"Harmonic mean: expected {expected}, got {result['ikigai_harmonic']}"
    
    @settings(max_examples=100)
    @given(
        love=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        good_at=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        world_needs=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        paid_for=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    def test_harmonic_mean_less_than_arithmetic_mean(self, love: float, good_at: float, world_needs: float, paid_for: float):
        """
        Verify that harmonic mean is always less than or equal to arithmetic mean.
        This is a mathematical property of harmonic means.
        """
        harmonic = IkigaiCalculationAlgorithm._calculate_harmonic_mean(
            love, good_at, world_needs, paid_for
        )
        arithmetic = (love + good_at + world_needs + paid_for) / 4
        
        # Harmonic mean <= Arithmetic mean (with small tolerance for floating point)
        assert harmonic <= arithmetic + 0.001, \
            f"Harmonic mean {harmonic} should be <= arithmetic mean {arithmetic}"
    
    def test_harmonic_mean_zero_when_any_axis_zero(self):
        """
        Verify that harmonic mean returns 0 when any axis score is zero.
        **Validates: Requirements 3.7**
        """
        # Test with zero love
        result = IkigaiCalculationAlgorithm._calculate_harmonic_mean(0, 50, 50, 50)
        assert result == 0.0, f"Expected 0.0 when love is 0, got {result}"
        
        # Test with zero good_at
        result = IkigaiCalculationAlgorithm._calculate_harmonic_mean(50, 0, 50, 50)
        assert result == 0.0, f"Expected 0.0 when good_at is 0, got {result}"
        
        # Test with zero world_needs
        result = IkigaiCalculationAlgorithm._calculate_harmonic_mean(50, 50, 0, 50)
        assert result == 0.0, f"Expected 0.0 when world_needs is 0, got {result}"
        
        # Test with zero paid_for
        result = IkigaiCalculationAlgorithm._calculate_harmonic_mean(50, 50, 50, 0)
        assert result == 0.0, f"Expected 0.0 when paid_for is 0, got {result}"



class TestGeometricMeanProperty:
    """
    Property 10: Geometric Mean Formula
    
    *For any* four positive axis scores, the geometric mean SHALL equal 
    (love * good_at * world_needs * paid_for)^(1/4).
    
    **Validates: Requirements 3.6**
    """
    
    @settings(max_examples=100)
    @given(
        love=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        good_at=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        world_needs=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        paid_for=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    def test_geometric_mean_formula(self, love: float, good_at: float, world_needs: float, paid_for: float):
        """
        Feature: backend-test-suite, Property 10: Geometric Mean Formula
        **Validates: Requirements 3.6**
        
        For any four positive axis scores, the geometric mean equals
        (love * good_at * world_needs * paid_for)^(1/4).
        """
        # Calculate expected geometric mean
        expected = math.pow(love * good_at * world_needs * paid_for, 0.25)
        
        # Calculate actual geometric mean using the algorithm
        actual = IkigaiCalculationAlgorithm._calculate_geometric_mean(
            love, good_at, world_needs, paid_for
        )
        
        assert abs(actual - expected) < 0.001, \
            f"Geometric mean: expected {expected}, got {actual}"
    
    @settings(max_examples=100)
    @given(scores=profile_vector_scores_positive())
    def test_geometric_mean_from_profile_vector(self, scores: list):
        """
        Verify geometric mean is correctly calculated from profile vector.
        """
        pv = Mock(spec=ProfileVector)
        pv.to_vector.return_value = scores
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(pv)
        
        # Get the axis scores
        love = result['ikigai_love']
        good_at = result['ikigai_good_at']
        world_needs = result['ikigai_world_needs']
        paid_for = result['ikigai_paid_for']
        
        # Skip if any axis is zero or negative (geometric mean returns 0 in that case)
        if any(score <= 0 for score in [love, good_at, world_needs, paid_for]):
            assert result['ikigai_geometric'] == 0.0
        else:
            # Calculate expected geometric mean
            expected = math.pow(love * good_at * world_needs * paid_for, 0.25)
            assert abs(result['ikigai_geometric'] - expected) < 0.001, \
                f"Geometric mean: expected {expected}, got {result['ikigai_geometric']}"
    
    @settings(max_examples=100)
    @given(
        love=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        good_at=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        world_needs=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        paid_for=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    def test_geometric_mean_less_than_arithmetic_mean(self, love: float, good_at: float, world_needs: float, paid_for: float):
        """
        Verify that geometric mean is always less than or equal to arithmetic mean.
        This is a mathematical property of geometric means (AM-GM inequality).
        """
        geometric = IkigaiCalculationAlgorithm._calculate_geometric_mean(
            love, good_at, world_needs, paid_for
        )
        arithmetic = (love + good_at + world_needs + paid_for) / 4
        
        # Geometric mean <= Arithmetic mean (with small tolerance for floating point)
        assert geometric <= arithmetic + 0.001, \
            f"Geometric mean {geometric} should be <= arithmetic mean {arithmetic}"
    
    @settings(max_examples=100)
    @given(
        love=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        good_at=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        world_needs=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        paid_for=st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    def test_geometric_mean_greater_than_harmonic_mean(self, love: float, good_at: float, world_needs: float, paid_for: float):
        """
        Verify that geometric mean is always greater than or equal to harmonic mean.
        This is a mathematical property: HM <= GM <= AM.
        """
        geometric = IkigaiCalculationAlgorithm._calculate_geometric_mean(
            love, good_at, world_needs, paid_for
        )
        harmonic = IkigaiCalculationAlgorithm._calculate_harmonic_mean(
            love, good_at, world_needs, paid_for
        )
        
        # Geometric mean >= Harmonic mean (with small tolerance for floating point)
        assert geometric >= harmonic - 0.001, \
            f"Geometric mean {geometric} should be >= harmonic mean {harmonic}"
    
    def test_geometric_mean_zero_when_any_axis_zero_or_negative(self):
        """
        Verify that geometric mean returns 0 when any axis score is zero or negative.
        **Validates: Requirements 3.8**
        """
        # Test with zero love
        result = IkigaiCalculationAlgorithm._calculate_geometric_mean(0, 50, 50, 50)
        assert result == 0.0, f"Expected 0.0 when love is 0, got {result}"
        
        # Test with zero good_at
        result = IkigaiCalculationAlgorithm._calculate_geometric_mean(50, 0, 50, 50)
        assert result == 0.0, f"Expected 0.0 when good_at is 0, got {result}"
        
        # Test with zero world_needs
        result = IkigaiCalculationAlgorithm._calculate_geometric_mean(50, 50, 0, 50)
        assert result == 0.0, f"Expected 0.0 when world_needs is 0, got {result}"
        
        # Test with zero paid_for
        result = IkigaiCalculationAlgorithm._calculate_geometric_mean(50, 50, 50, 0)
        assert result == 0.0, f"Expected 0.0 when paid_for is 0, got {result}"
        
        # Test with negative value
        result = IkigaiCalculationAlgorithm._calculate_geometric_mean(-10, 50, 50, 50)
        assert result == 0.0, f"Expected 0.0 when love is negative, got {result}"
