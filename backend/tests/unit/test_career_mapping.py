"""
Unit tests for career mapping algorithm.
"""
import pytest
from unittest.mock import Mock
from backend.src.algorithms.career_mapping import CareerMappingAlgorithm
from backend.src.models.profile_vector import ProfileVector
from backend.src.models.career_rule import CareerRule


class TestCareerMappingAlgorithm:
    """Test cases for career mapping algorithm."""
    
    def test_calculate_career_fit_scores_basic(self):
        """Test basic career fit score calculation."""
        # Create mock profile vector
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16
        
        # Create mock career rules
        career_rules = [
            Mock(spec=CareerRule),
            Mock(spec=CareerRule)
        ]
        
        # Setup mock rules
        for i, rule in enumerate(career_rules):
            rule.career_name = f"Career{i+1}"
            rule.weights = {f"facet_{j}": 0.8 for j in range(16)}
            rule.thresholds = {f"facet_{j}": 50.0 for j in range(16)}
            rule.bonus_keys = ["facet_0", "facet_1"]
            rule.is_active = True
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, career_rules
        )
        
        assert isinstance(result, list)
        assert len(result) == 2
        
        for career_result in result:
            assert 'career_name' in career_result
            assert 'fit_score' in career_result
            assert 'rank' in career_result
            assert 'explanation' in career_result
            assert 0 <= career_result['fit_score'] <= 100
    
    def test_calculate_career_fit_scores_high_fit(self):
        """Test career fit calculation with high compatibility."""
        profile_vector = Mock(spec=ProfileVector)
        # High scores that exceed thresholds
        profile_vector.to_vector.return_value = [90.0] * 16
        
        career_rule = Mock(spec=CareerRule)
        career_rule.career_name = "HighFitCareer"
        career_rule.weights = {f"facet_{i}": 0.8 for i in range(16)}
        career_rule.thresholds = {f"facet_{i}": 50.0 for i in range(16)}
        career_rule.bonus_keys = ["facet_0", "facet_1"]
        career_rule.is_active = True
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, [career_rule]
        )
        
        assert len(result) == 1
        assert result[0]['fit_score'] > 80  # Should be high fit
        assert result[0]['career_name'] == "HighFitCareer"
    
    def test_calculate_career_fit_scores_low_fit(self):
        """Test career fit calculation with low compatibility."""
        profile_vector = Mock(spec=ProfileVector)
        # Low scores that don't meet thresholds
        profile_vector.to_vector.return_value = [20.0] * 16
        
        career_rule = Mock(spec=CareerRule)
        career_rule.career_name = "LowFitCareer"
        career_rule.weights = {f"facet_{i}": 0.8 for i in range(16)}
        career_rule.thresholds = {f"facet_{i}": 80.0 for i in range(16)}  # High thresholds
        career_rule.bonus_keys = []
        career_rule.is_active = True
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, [career_rule]
        )
        
        assert len(result) == 1
        assert result[0]['fit_score'] < 40  # Should be low fit
        assert result[0]['career_name'] == "LowFitCareer"
    
    def test_calculate_career_fit_scores_with_bonus(self):
        """Test career fit calculation with bonus points."""
        profile_vector = Mock(spec=ProfileVector)
        # High scores in bonus areas
        scores = [95.0, 95.0] + [50.0] * 14  # High in first two facets
        profile_vector.to_vector.return_value = scores
        
        career_rule = Mock(spec=CareerRule)
        career_rule.career_name = "BonusCareer"
        career_rule.weights = {f"facet_{i}": 0.5 for i in range(16)}
        career_rule.thresholds = {f"facet_{i}": 40.0 for i in range(16)}
        career_rule.bonus_keys = ["facet_0", "facet_1"]  # First two facets get bonus
        career_rule.is_active = True
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, [career_rule]
        )
        
        assert len(result) == 1
        # Should have high fit due to bonus points
        assert result[0]['fit_score'] > 70
    
    def test_calculate_career_fit_scores_ranking(self):
        """Test that results are properly ranked."""
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16
        
        # Create rules with different fit levels
        career_rules = []
        for i in range(3):
            rule = Mock(spec=CareerRule)
            rule.career_name = f"Career{i+1}"
            rule.weights = {f"facet_{j}": 0.5 + (i * 0.1) for j in range(16)}
            rule.thresholds = {f"facet_{j}": 50.0 for j in range(16)}
            rule.bonus_keys = []
            rule.is_active = True
            career_rules.append(rule)
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, career_rules
        )
        
        # Should be ranked by fit score (descending)
        for i in range(len(result) - 1):
            assert result[i]['fit_score'] >= result[i + 1]['fit_score']
            assert result[i]['rank'] == i + 1
    
    def test_calculate_career_fit_scores_inactive_rules(self):
        """Test that inactive rules are excluded."""
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16
        
        career_rules = [
            Mock(spec=CareerRule),
            Mock(spec=CareerRule)
        ]
        
        # First rule is active, second is inactive
        career_rules[0].career_name = "ActiveCareer"
        career_rules[0].weights = {f"facet_{i}": 0.8 for i in range(16)}
        career_rules[0].thresholds = {f"facet_{i}": 50.0 for i in range(16)}
        career_rules[0].bonus_keys = []
        career_rules[0].is_active = True
        
        career_rules[1].career_name = "InactiveCareer"
        career_rules[1].weights = {f"facet_{i}": 0.8 for i in range(16)}
        career_rules[1].thresholds = {f"facet_{i}": 50.0 for i in range(16)}
        career_rules[1].bonus_keys = []
        career_rules[1].is_active = False
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, career_rules
        )
        
        # Should only include active rule
        assert len(result) == 1
        assert result[0]['career_name'] == "ActiveCareer"
    
    def test_calculate_career_fit_score_individual(self):
        """Test individual career fit score calculation."""
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [75.0] * 16
        
        career_rule = Mock(spec=CareerRule)
        career_rule.career_name = "TestCareer"
        career_rule.weights = {f"facet_{i}": 0.8 for i in range(16)}
        career_rule.thresholds = {f"facet_{i}": 60.0 for i in range(16)}
        career_rule.bonus_keys = ["facet_0"]
        
        result = CareerMappingAlgorithm._calculate_career_fit_score(
            profile_vector.to_vector(), career_rule
        )
        
        assert isinstance(result, float)
        assert 0 <= result <= 100
    
    def test_generate_explanation(self):
        """Test explanation generation."""
        profile_scores = [80.0, 60.0, 40.0, 20.0] + [50.0] * 12
        career_rule = Mock(spec=CareerRule)
        career_rule.career_name = "TestCareer"
        career_rule.weights = {f"facet_{i}": 0.8 for i in range(16)}
        career_rule.thresholds = {f"facet_{i}": 50.0 for i in range(16)}
        career_rule.bonus_keys = ["facet_0"]
        
        explanation = CareerMappingAlgorithm._generate_explanation(
            profile_scores, career_rule, 75.0
        )
        
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        assert "TestCareer" in explanation
    
    def test_get_career_requirements(self):
        """Test career requirements retrieval."""
        career_name = "Software Engineer"
        
        requirements = CareerMappingAlgorithm.get_career_requirements(career_name)
        
        assert isinstance(requirements, dict)
        assert 'career_name' in requirements
        assert 'description' in requirements
        assert 'key_skills' in requirements
        assert 'education_requirements' in requirements
        assert 'experience_level' in requirements
        assert 'salary_range' in requirements
        assert 'growth_outlook' in requirements
    
    def test_get_career_requirements_unknown_career(self):
        """Test career requirements for unknown career."""
        career_name = "Unknown Career"
        
        requirements = CareerMappingAlgorithm.get_career_requirements(career_name)
        
        # Should return default structure
        assert isinstance(requirements, dict)
        assert requirements['career_name'] == career_name
        assert 'description' in requirements
    
    def test_edge_case_empty_rules(self):
        """Test handling of empty rules list."""
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16
        
        result = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, []
        )
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_edge_case_invalid_profile_vector(self):
        """Test handling of invalid profile vector."""
        career_rule = Mock(spec=CareerRule)
        career_rule.career_name = "TestCareer"
        career_rule.weights = {f"facet_{i}": 0.8 for i in range(16)}
        career_rule.thresholds = {f"facet_{i}": 50.0 for i in range(16)}
        career_rule.bonus_keys = []
        career_rule.is_active = True
        
        # Test with None
        with pytest.raises(TypeError):
            CareerMappingAlgorithm.calculate_career_fit_scores(None, [career_rule])
        
        # Test with invalid vector length
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 10  # Wrong length
        
        with pytest.raises(ValueError):
            CareerMappingAlgorithm.calculate_career_fit_scores(profile_vector, [career_rule])
    
    def test_consistency_across_calls(self):
        """Test that multiple calls with same input produce same output."""
        profile_vector = Mock(spec=ProfileVector)
        profile_vector.to_vector.return_value = [70.0] * 16
        
        career_rule = Mock(spec=CareerRule)
        career_rule.career_name = "TestCareer"
        career_rule.weights = {f"facet_{i}": 0.8 for i in range(16)}
        career_rule.thresholds = {f"facet_{i}": 50.0 for i in range(16)}
        career_rule.bonus_keys = []
        career_rule.is_active = True
        
        result1 = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, [career_rule]
        )
        result2 = CareerMappingAlgorithm.calculate_career_fit_scores(
            profile_vector, [career_rule]
        )
        
        # Results should be identical
        assert len(result1) == len(result2)
        for i in range(len(result1)):
            assert result1[i]['fit_score'] == result2[i]['fit_score']
            assert result1[i]['career_name'] == result2[i]['career_name']