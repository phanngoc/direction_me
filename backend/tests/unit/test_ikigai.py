"""
Unit tests for Ikigai calculation algorithm.
"""
import pytest
from unittest.mock import Mock
from backend.src.algorithms.ikigai_calculation import IkigaiCalculationAlgorithm
from backend.src.models.profile_vector import ProfileVector


class TestIkigaiCalculationAlgorithm:
    """Test cases for Ikigai calculation algorithm."""
    
    def test_calculate_ikigai_scores_basic(self):
        """Test basic Ikigai score calculation."""
        # Create a mock profile vector with balanced scores
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16  # All scores at 70
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        
        # Check that all required scores are present
        assert 'ikigai_love' in result
        assert 'ikigai_good_at' in result
        assert 'ikigai_world_needs' in result
        assert 'ikigai_paid_for' in result
        assert 'ikigai_harmonic' in result
        assert 'ikigai_geometric' in result
        
        # Check that scores are within valid range
        for key, value in result.items():
            assert 0 <= value <= 100, f"{key} should be between 0 and 100, got {value}"
    
    def test_calculate_ikigai_scores_high_iq_low_eq(self):
        """Test Ikigai calculation with high IQ and low EQ."""
        profile_vector = Mock(spec=ProfileVector)
        # High IQ scores, low EQ scores
        scores = [90.0, 90.0, 90.0, 90.0,  # IQ
                 30.0, 30.0, 30.0, 30.0,  # EQ
                 50.0, 50.0, 50.0, 50.0,  # DQ
                 50.0, 50.0, 50.0, 50.0]  # AQ
        profile_vector.to_vector.return_value = scores
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        
        # Good at should be high (IQ contributes heavily)
        assert result['ikigai_good_at'] > 70
        
        # Love should be lower (EQ contributes heavily)
        assert result['ikigai_love'] < 50
    
    def test_calculate_ikigai_scores_high_eq_low_iq(self):
        """Test Ikigai calculation with high EQ and low IQ."""
        profile_vector = Mock(spec=ProfileVector)
        # Low IQ scores, high EQ scores
        scores = [30.0, 30.0, 30.0, 30.0,  # IQ
                 90.0, 90.0, 90.0, 90.0,  # EQ
                 50.0, 50.0, 50.0, 50.0,  # DQ
                 50.0, 50.0, 50.0, 50.0]  # AQ
        profile_vector.to_vector.return_value = scores
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        
        # Love should be high (EQ contributes heavily)
        assert result['ikigai_love'] > 70
        
        # Good at should be lower (IQ contributes heavily)
        assert result['ikigai_good_at'] < 50
    
    def test_calculate_ikigai_scores_extreme_values(self):
        """Test Ikigai calculation with extreme values."""
        profile_vector = Mock(spec=ProfileVector)
        # All scores at 0
        profile_vector.to_vector.return_value = [0.0] * 16
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        
        # All scores should be 0 or very low
        for key, value in result.items():
            assert 0 <= value <= 10, f"{key} should be very low, got {value}"
    
    def test_calculate_ikigai_scores_maximum_values(self):
        """Test Ikigai calculation with maximum values."""
        profile_vector = Mock(spec=ProfileVector)
        # All scores at 100
        profile_vector.to_vector.return_value = [100.0] * 16
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        
        # All scores should be high
        for key, value in result.items():
            assert value > 80, f"{key} should be high, got {value}"
    
    def test_get_ikigai_interpretation(self):
        """Test Ikigai interpretation generation."""
        # Test balanced profile
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        interpretation = IkigaiCalculationAlgorithm.get_ikigai_interpretation(result)
        
        assert 'quadrant' in interpretation
        assert 'description' in interpretation
        assert 'recommendations' in interpretation
        assert isinstance(interpretation['recommendations'], list)
    
    def test_get_ikigai_quadrant(self):
        """Test Ikigai quadrant determination."""
        # Test different quadrant scenarios
        test_cases = [
            # (love, good_at, world_needs, paid_for, expected_quadrant)
            (80, 80, 80, 80, "Perfect Match"),
            (90, 90, 30, 30, "Passion & Mission"),
            (30, 90, 30, 90, "Profession & Vocation"),
            (90, 30, 90, 30, "Mission & Vocation"),
            (30, 30, 90, 90, "Profession & Mission"),
            (50, 50, 50, 50, "Balanced")
        ]
        
        for love, good_at, world_needs, paid_for, expected in test_cases:
            quadrant = IkigaiCalculationAlgorithm.get_ikigai_quadrant(
                love, good_at, world_needs, paid_for
            )
            assert quadrant == expected, f"Expected {expected}, got {quadrant}"
    
    def test_get_development_recommendations(self):
        """Test development recommendations generation."""
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        recommendations = IkigaiCalculationAlgorithm.get_development_recommendations(result)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(rec, str) for rec in recommendations)
    
    def test_harmonic_mean_calculation(self):
        """Test harmonic mean calculation."""
        # Test with known values
        love, good_at, world_needs, paid_for = 80.0, 60.0, 40.0, 20.0
        
        harmonic_mean = IkigaiCalculationAlgorithm._calculate_harmonic_mean(
            love, good_at, world_needs, paid_for
        )
        
        # Harmonic mean should be less than arithmetic mean
        arithmetic_mean = (love + good_at + world_needs + paid_for) / 4
        assert harmonic_mean < arithmetic_mean
        assert 0 <= harmonic_mean <= 100
    
    def test_geometric_mean_calculation(self):
        """Test geometric mean calculation."""
        # Test with known values
        love, good_at, world_needs, paid_for = 80.0, 60.0, 40.0, 20.0
        
        geometric_mean = IkigaiCalculationAlgorithm._calculate_geometric_mean(
            love, good_at, world_needs, paid_for
        )
        
        # Geometric mean should be less than arithmetic mean
        arithmetic_mean = (love + good_at + world_needs + paid_for) / 4
        assert geometric_mean < arithmetic_mean
        assert 0 <= geometric_mean <= 100
    
    def test_axis_calculation_weights(self):
        """Test that axis calculations use correct weights."""
        profile_vector = Mock(spec=ProfileVector)
        # Set specific scores to test weight distribution
        scores = [100.0, 0.0, 0.0, 0.0,  # IQ: only LR high
                 0.0, 100.0, 0.0, 0.0,  # EQ: only empathy high
                 0.0, 0.0, 100.0, 0.0,  # DQ: only info_literacy high
                 0.0, 0.0, 0.0, 100.0]  # AQ: only control high
        profile_vector.to_vector.return_value = scores
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        
        # Each axis should reflect the corresponding high score
        assert result['ikigai_good_at'] > 50  # IQ contributes to good_at
        assert result['ikigai_love'] > 50     # EQ contributes to love
        assert result['ikigai_world_needs'] > 50  # DQ contributes to world_needs
        assert result['ikigai_paid_for'] > 50     # AQ contributes to paid_for
    
    def test_invalid_profile_vector(self):
        """Test handling of invalid profile vector."""
        # Test with None
        with pytest.raises(AttributeError):
            IkigaiCalculationAlgorithm.calculate_ikigai_scores(None)
        
        # Test with invalid vector length
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 10  # Wrong length
        
        with pytest.raises(ValueError):
            IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
    
    def test_edge_case_zero_scores(self):
        """Test handling of zero scores in calculation."""
        profile_vector = Mock(spec=ProfileVector)
        # Mix of zero and non-zero scores
        scores = [0.0, 50.0, 0.0, 50.0,  # IQ
                 0.0, 50.0, 0.0, 50.0,  # EQ
                 0.0, 50.0, 0.0, 50.0,  # DQ
                 0.0, 50.0, 0.0, 50.0]  # AQ
        profile_vector.to_vector.return_value = scores
        
        result = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        
        # Should handle zero scores gracefully
        for key, value in result.items():
            assert 0 <= value <= 100, f"{key} should be between 0 and 100, got {value}"
    
    def test_consistency_across_calls(self):
        """Test that multiple calls with same input produce same output."""
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16
        
        result1 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        result2 = IkigaiCalculationAlgorithm.calculate_ikigai_scores(profile_vector)
        
        # Results should be identical
        for key in result1:
            assert result1[key] == result2[key], f"Results differ for {key}"