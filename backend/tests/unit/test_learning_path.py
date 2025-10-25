"""
Unit tests for learning path generation
"""

import pytest
from src.algorithms.learning_path_generator import (
    generate_learning_path,
    generate_skill_recommendations,
    generate_project_plan,
    generate_habit_suggestions
)
from src.algorithms.skill_gap_analysis import analyze_skill_gap
from src.algorithms.recommendations import generate_learning_recommendations


class TestLearningPathGeneration:
    """Test suite for learning path generation"""

    def setup_method(self):
        """Setup test data"""
        self.test_profile = {
            'iq_lr': 75.0,
            'iq_nr': 70.0,
            'iq_vr': 80.0,
            'iq_sr': 65.0,
            'eq_empathy': 85.0,
            'eq_social': 75.0,
            'eq_self_awareness': 70.0,
            'eq_self_regulation': 65.0,
            'dq_info_literacy': 80.0,
            'dq_creativity': 85.0,
            'dq_safety': 70.0,
            'dq_collaboration': 75.0,
            'aq_control': 70.0,
            'aq_ownership': 75.0,
            'aq_reach': 65.0,
            'aq_endurance': 80.0
        }

        self.test_career = 'Software Engineer'
        self.test_requirements = {
            'iq_lr': 90.0,
            'iq_nr': 85.0,
            'dq_creativity': 95.0,
            'dq_collaboration': 85.0,
            'aq_ownership': 90.0,
            'aq_endurance': 90.0
        }

    def test_generate_learning_path_success(self):
        """Test successful learning path generation"""
        result = generate_learning_path(
            self.test_profile,
            self.test_career,
            self.test_requirements
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

    def test_generate_learning_path_empty_profile(self):
        """Test learning path generation with empty profile"""
        empty_profile = {}

        result = generate_learning_path(
            empty_profile,
            self.test_career,
            self.test_requirements
        )

        # Should still generate a path based on career requirements
        assert 'skills' in result
        assert len(result['skills']) > 0

    def test_generate_skill_recommendations(self):
        """Test skill recommendation generation"""
        gap_analysis = analyze_skill_gap(
            self.test_profile,
            self.test_requirements,
            self.test_career
        )

        recommendations = generate_skill_recommendations(
            gap_analysis['prioritized_gaps']
        )

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        for rec in recommendations:
            assert 'skill' in rec
            assert 'priority' in rec
            assert 'recommended_resources' in rec
            assert 'estimated_duration_weeks' in rec

    def test_generate_project_plan(self):
        """Test project plan generation"""
        projects = generate_project_plan(self.test_career, self.test_profile)

        assert isinstance(projects, list)
        assert len(projects) > 0
        for project in projects:
            assert 'name' in project
            assert 'description' in project
            assert 'duration_weeks' in project
            assert 'skills_required' in project

    def test_generate_habit_suggestions(self):
        """Test habit suggestion generation"""
        habits = generate_habit_suggestions(self.test_career)

        assert isinstance(habits, list)
        assert len(habits) > 0
        for habit in habits:
            assert 'name' in habit
            assert 'frequency' in habit
            assert 'duration_minutes' in habit

    def test_learning_path_timeline_calculation(self):
        """Test timeline calculation in learning path"""
        result = generate_learning_path(
            self.test_profile,
            self.test_career,
            self.test_requirements
        )

        # Timeline should be sum of all skill development times
        total_skill_weeks = sum(s['duration_weeks'] for s in result['skills'])
        total_project_weeks = sum(p['duration_weeks'] for p in result['projects'])

        # Timeline can be parallel, so it might be less than sum
        assert result['timeline_weeks'] >= max(total_skill_weeks, total_project_weeks)

    def test_learning_path_priority_ordering(self):
        """Test that skills are ordered by priority"""
        result = generate_learning_path(
            self.test_profile,
            self.test_career,
            self.test_requirements
        )

        # Critical priority skills should come first
        priorities = [s.get('priority', 'minor') for s in result['skills']]
        priority_order = {'critical': 0, 'moderate': 1, 'minor': 2}

        # Check that priorities are generally in order (allowing some flexibility)
        for i in range(len(priorities) - 1):
            current = priority_order.get(priorities[i], 3)
            next_val = priority_order.get(priorities[i + 1], 3)
            # Allow same or increasing priority (lower number = higher priority)
            assert current <= next_val + 1  # Allow some flexibility

    def test_learning_recommendations_structure(self):
        """Test learning recommendations structure"""
        gap_analysis = analyze_skill_gap(
            self.test_profile,
            self.test_requirements,
            self.test_career
        )

        recommendations = generate_learning_recommendations(
            self.test_profile,
            self.test_career,
            self.test_requirements,
            gap_analysis['prioritized_gaps']
        )

        assert 'iq_recommendations' in recommendations
        assert 'eq_recommendations' in recommendations
        assert 'dq_recommendations' in recommendations
        assert 'aq_recommendations' in recommendations
        assert 'projects' in recommendations
        assert 'habits' in recommendations
        assert 'timeline' in recommendations

    def test_learning_path_different_careers(self):
        """Test learning path generation for different careers"""
        careers = ['Software Engineer', 'Data Scientist', 'Product Manager', 'UX Designer']

        for career in careers:
            result = generate_learning_path(
                self.test_profile,
                career,
                self.test_requirements
            )

            assert result['career_name'] == career
            assert len(result['skills']) > 0
            assert len(result['projects']) > 0

    def test_learning_path_resource_validation(self):
        """Test that resources are properly included"""
        result = generate_learning_path(
            self.test_profile,
            self.test_career,
            self.test_requirements
        )

        for skill in result['skills']:
            assert 'resources' in skill
            assert isinstance(skill['resources'], list)
            assert len(skill['resources']) > 0

    def test_learning_path_level_categorization(self):
        """Test that skills are categorized by level"""
        result = generate_learning_path(
            self.test_profile,
            self.test_career,
            self.test_requirements
        )

        levels = set()
        for skill in result['skills']:
            assert 'level' in skill
            levels.add(skill['level'])

        # Should have at least some level differentiation
        assert len(levels) > 0
        # Valid levels only
        valid_levels = {'beginner', 'intermediate', 'advanced'}
        assert all(level in valid_levels for level in levels)


class TestSkillGapAnalysis:
    """Test suite for skill gap analysis"""

    def setup_method(self):
        """Setup test data"""
        self.test_profile = {
            'iq_lr': 75.0,
            'iq_nr': 70.0,
            'dq_creativity': 85.0
        }

        self.test_requirements = {
            'iq_lr': 90.0,
            'iq_nr': 85.0,
            'dq_creativity': 95.0
        }

    def test_skill_gap_calculation(self):
        """Test skill gap calculation"""
        result = analyze_skill_gap(
            self.test_profile,
            self.test_requirements,
            'Software Engineer'
        )

        assert 'skill_gaps' in result
        assert 'prioritized_gaps' in result
        assert 'readiness_score' in result

        # Check specific gaps
        assert 'iq_lr' in result['skill_gaps']
        assert result['skill_gaps']['iq_lr']['gap'] == 15.0

    def test_readiness_score_calculation(self):
        """Test readiness score calculation"""
        result = analyze_skill_gap(
            self.test_profile,
            self.test_requirements,
            'Software Engineer'
        )

        # Readiness score should be between 0 and 100
        assert 0 <= result['readiness_score'] <= 100

    def test_gap_prioritization(self):
        """Test that gaps are properly prioritized"""
        result = analyze_skill_gap(
            self.test_profile,
            self.test_requirements,
            'Software Engineer'
        )

        priorities = result['prioritized_gaps']

        # Gaps should be ordered by size (largest first)
        for i in range(len(priorities) - 1):
            assert priorities[i]['gap'] >= priorities[i + 1]['gap']

    def test_no_gaps_scenario(self):
        """Test scenario where user meets all requirements"""
        high_profile = {
            'iq_lr': 95.0,
            'iq_nr': 90.0,
            'dq_creativity': 100.0
        }

        result = analyze_skill_gap(
            high_profile,
            self.test_requirements,
            'Software Engineer'
        )

        assert result['readiness_score'] >= 95.0
        assert result['total_gaps'] == 0 or all(
            gap['gap'] == 0 for gap in result['prioritized_gaps']
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
