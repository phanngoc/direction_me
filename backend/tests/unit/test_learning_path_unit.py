"""
Unit tests for learning path generation
"""

import pytest
from unittest.mock import Mock, patch
from src.algorithms.learning_path_generator import LearningPathGenerator
from src.models.profile_vector import ProfileVector


class TestLearningPathGeneration:
    """Test suite for learning path generation"""

    def setup_method(self):
        """Setup test data"""
        self.generator = LearningPathGenerator()
        
        # Create a mock profile vector
        self.mock_profile = Mock(spec=ProfileVector)
        self.mock_profile.to_vector.return_value = [
            75.0, 70.0, 80.0, 65.0,  # IQ: LR, NR, VR, SR
            85.0, 75.0, 70.0, 65.0,  # EQ: Empathy, Social, SelfAwareness, SelfRegulation
            80.0, 85.0, 70.0, 75.0,  # DQ: InfoLiteracy, Creativity, Safety, Collaboration
            70.0, 75.0, 65.0, 80.0   # AQ: Control, Ownership, Reach, Endurance
        ]

        self.test_career = 'Software Engineer'

    def test_generate_learning_path_success(self):
        """Test successful learning path generation"""
        result = self.generator.generate_learning_path(
            self.mock_profile,
            self.test_career
        )

        assert 'skills' in result
        assert 'projects' in result
        assert 'habits' in result
        assert 'timeline_weeks' in result
        assert result['career_name'] == self.test_career
        assert isinstance(result['skills'], list)
        assert isinstance(result['projects'], list)
        assert isinstance(result['habits'], list)
        assert result['timeline_weeks'] > 0

    def test_generate_learning_path_unknown_career(self):
        """Test learning path generation for unknown career"""
        result = self.generator.generate_learning_path(
            self.mock_profile,
            'Unknown Career XYZ'
        )

        # Should still generate a default path
        assert 'skills' in result
        assert 'projects' in result
        assert 'habits' in result
        assert result['career_name'] == 'Unknown Career XYZ'

    def test_generate_recommendations(self):
        """Test recommendation generation"""
        skill_gaps = ['Logical Thinking', 'Mathematical Skills', 'Digital Literacy']
        
        recommendations = self.generator.generate_recommendations(
            self.mock_profile,
            skill_gaps
        )

        assert 'technical_recommendations' in recommendations
        assert 'soft_skill_recommendations' in recommendations
        assert 'learning_resources' in recommendations
        assert 'practice_exercises' in recommendations
        assert 'priority_skills' in recommendations

    def test_learning_path_timeline_calculation(self):
        """Test timeline calculation in learning path"""
        result = self.generator.generate_learning_path(
            self.mock_profile,
            self.test_career
        )

        # Timeline should be between 8 and 52 weeks
        assert 8 <= result['timeline_weeks'] <= 52

    def test_learning_path_priority_determination(self):
        """Test that priority is properly determined"""
        result = self.generator.generate_learning_path(
            self.mock_profile,
            self.test_career
        )

        assert result['priority'] in ['high', 'medium', 'low']

    def test_learning_path_difficulty_level(self):
        """Test difficulty level assessment"""
        result = self.generator.generate_learning_path(
            self.mock_profile,
            self.test_career
        )

        assert result['difficulty_level'] in ['beginner', 'intermediate', 'advanced']

    def test_learning_path_learning_style(self):
        """Test learning style determination"""
        result = self.generator.generate_learning_path(
            self.mock_profile,
            self.test_career
        )

        assert result['learning_style'] in ['visual', 'analytical', 'social']

    def test_learning_path_different_careers(self):
        """Test learning path generation for different careers"""
        careers = ['Software Engineer', 'Data Scientist', 'Product Manager', 'UX Designer']

        for career in careers:
            result = self.generator.generate_learning_path(
                self.mock_profile,
                career
            )

            assert result['career_name'] == career
            assert 'skills' in result
            assert 'projects' in result

    def test_low_profile_scores_generate_more_gaps(self):
        """Test that low profile scores generate more skill gaps"""
        low_profile = Mock(spec=ProfileVector)
        low_profile.to_vector.return_value = [30.0] * 16  # All low scores
        
        result = self.generator.generate_learning_path(
            low_profile,
            self.test_career
        )

        # Should have skill gaps identified
        assert 'skill_gaps' in result
        assert len(result['skill_gaps']) > 0

    def test_high_profile_scores_generate_fewer_gaps(self):
        """Test that high profile scores generate fewer skill gaps"""
        high_profile = Mock(spec=ProfileVector)
        high_profile.to_vector.return_value = [90.0] * 16  # All high scores
        
        result = self.generator.generate_learning_path(
            high_profile,
            self.test_career
        )

        # Should have fewer or no skill gaps
        assert 'skill_gaps' in result


class TestSkillGapAnalysis:
    """Test suite for skill gap analysis within learning path generator"""

    def setup_method(self):
        """Setup test data"""
        self.generator = LearningPathGenerator()

    def test_analyze_skill_gaps_low_scores(self):
        """Test skill gap analysis with low scores"""
        low_scores = [40.0] * 16  # All below 60
        
        gaps = self.generator._analyze_skill_gaps(low_scores)
        
        assert isinstance(gaps, list)
        assert len(gaps) > 0  # Should identify gaps

    def test_analyze_skill_gaps_high_scores(self):
        """Test skill gap analysis with high scores"""
        high_scores = [80.0] * 16  # All above 60
        
        gaps = self.generator._analyze_skill_gaps(high_scores)
        
        assert isinstance(gaps, list)
        assert len(gaps) == 0  # Should not identify gaps

    def test_analyze_skill_gaps_mixed_scores(self):
        """Test skill gap analysis with mixed scores"""
        mixed_scores = [40.0, 80.0, 50.0, 90.0] * 4  # Mix of low and high
        
        gaps = self.generator._analyze_skill_gaps(mixed_scores)
        
        assert isinstance(gaps, list)
        # Should identify some gaps but not all


class TestDifficultyAssessment:
    """Test suite for difficulty level assessment"""

    def setup_method(self):
        """Setup test data"""
        self.generator = LearningPathGenerator()

    def test_assess_difficulty_level_beginner(self):
        """Test beginner difficulty assessment"""
        low_scores = [30.0] * 16
        
        level = self.generator._assess_difficulty_level(low_scores)
        
        assert level == 'beginner'

    def test_assess_difficulty_level_intermediate(self):
        """Test intermediate difficulty assessment"""
        mid_scores = [60.0] * 16
        
        level = self.generator._assess_difficulty_level(mid_scores)
        
        assert level == 'intermediate'

    def test_assess_difficulty_level_advanced(self):
        """Test advanced difficulty assessment"""
        high_scores = [85.0] * 16
        
        level = self.generator._assess_difficulty_level(high_scores)
        
        assert level == 'advanced'


class TestLearningStyleDetermination:
    """Test suite for learning style determination"""

    def setup_method(self):
        """Setup test data"""
        self.generator = LearningPathGenerator()

    def test_determine_learning_style_visual(self):
        """Test visual learning style determination"""
        # High verbal (index 2) and spatial (index 3) scores
        scores = [50.0] * 16
        scores[2] = 90.0  # Verbal
        scores[3] = 90.0  # Spatial
        
        style = self.generator._determine_learning_style(scores)
        
        assert style == 'visual'

    def test_determine_learning_style_analytical(self):
        """Test analytical learning style determination"""
        # High logical (index 0) and numerical (index 1) scores
        scores = [50.0] * 16
        scores[0] = 90.0  # Logical
        scores[1] = 90.0  # Numerical
        
        style = self.generator._determine_learning_style(scores)
        
        assert style == 'analytical'

    def test_determine_learning_style_social(self):
        """Test social learning style determination"""
        # High empathy (index 4) and social (index 5) scores
        scores = [50.0] * 16
        scores[4] = 90.0  # Empathy
        scores[5] = 90.0  # Social
        
        style = self.generator._determine_learning_style(scores)
        
        assert style == 'social'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
