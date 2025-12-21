"""
Tests to verify the test infrastructure is working correctly.
"""
import pytest
from hypothesis import given, settings
from tests.generators import (
    likert_value,
    score_value,
    profile_vector_scores,
    mock_question,
    career_rule,
    empty_profile_vector,
    max_profile_vector
)


class TestGenerators:
    """Test that all generators produce valid data."""
    
    @given(value=likert_value)
    @settings(max_examples=50)
    def test_likert_value_range(self, value):
        """Likert values should be between 1 and 5."""
        assert 1 <= value <= 5
        assert isinstance(value, int)
    
    @given(value=score_value)
    @settings(max_examples=50)
    def test_score_value_range(self, value):
        """Score values should be between 0 and 100."""
        assert 0.0 <= value <= 100.0
        assert isinstance(value, float)
    
    @given(scores=profile_vector_scores())
    @settings(max_examples=50)
    def test_profile_vector_scores_structure(self, scores):
        """Profile vector should have 16 elements in valid range."""
        assert len(scores) == 16
        assert all(0.0 <= s <= 100.0 for s in scores)
        assert all(isinstance(s, float) for s in scores)
    
    @given(question=mock_question())
    @settings(max_examples=50)
    def test_mock_question_attributes(self, question):
        """Mock questions should have all required attributes."""
        assert hasattr(question, 'id')
        assert hasattr(question, 'category')
        assert hasattr(question, 'facet')
        assert hasattr(question, 'question_type')
        assert hasattr(question, 'difficulty_weight')
        assert hasattr(question, 'reverse_score')
        assert question.category in ["IQ", "EQ", "DQ", "AQ"]
        assert question.question_type in ["MCQ", "Likert"]
    
    @given(rule=career_rule())
    @settings(max_examples=50)
    def test_career_rule_attributes(self, rule):
        """Career rules should have all required attributes."""
        assert hasattr(rule, 'career_name')
        assert hasattr(rule, 'weights')
        assert hasattr(rule, 'thresholds')
        assert hasattr(rule, 'bonus_keys')
        assert hasattr(rule, 'is_active')
        assert len(rule.weights) == 16
        assert len(rule.thresholds) == 16
        assert isinstance(rule.bonus_keys, list)
    
    @given(scores=empty_profile_vector())
    @settings(max_examples=5)
    def test_empty_profile_vector(self, scores):
        """Empty profile vector should have all zeros."""
        assert len(scores) == 16
        assert all(s == 0.0 for s in scores)
    
    @given(scores=max_profile_vector())
    @settings(max_examples=5)
    def test_max_profile_vector(self, scores):
        """Max profile vector should have all 100s."""
        assert len(scores) == 16
        assert all(s == 100.0 for s in scores)


class TestFixtures:
    """Test that conftest fixtures work correctly."""
    
    def test_mock_profile_vector_fixture(self, mock_profile_vector):
        """Test mock_profile_vector fixture creates valid objects."""
        # Default scores
        pv = mock_profile_vector()
        assert len(pv.to_vector()) == 16
        assert all(s == 50.0 for s in pv.to_vector())
        
        # Custom scores
        custom_scores = [i * 5.0 for i in range(16)]
        pv_custom = mock_profile_vector(custom_scores)
        assert pv_custom.to_vector() == custom_scores
    
    def test_mock_profile_vector_with_nulls_fixture(self, mock_profile_vector_with_nulls):
        """Test mock_profile_vector_with_nulls fixture."""
        null_indices = [0, 4, 8, 12]
        pv = mock_profile_vector_with_nulls(null_indices)
        vector = pv.to_vector()
        
        for i in range(16):
            if i in null_indices:
                assert vector[i] == 0.0
            else:
                assert vector[i] == 50.0
    
    def test_eq_questions_fixture(self, eq_questions):
        """Test eq_questions fixture creates valid questions."""
        assert len(eq_questions) == 4
        assert all(q.category == "EQ" for q in eq_questions)
        facets = [q.facet for q in eq_questions]
        assert "Empathy" in facets
        assert "Social" in facets
    
    def test_iq_questions_fixture(self, iq_questions):
        """Test iq_questions fixture creates valid questions."""
        assert len(iq_questions) == 4
        assert all(q.category == "IQ" for q in iq_questions)
        assert all(q.question_type == "MCQ" for q in iq_questions)
    
    def test_mock_career_rule_fixture(self, mock_career_rule):
        """Test mock_career_rule fixture creates valid rules."""
        rule = mock_career_rule("Software Engineer", is_active=True)
        assert rule.career_name == "Software Engineer"
        assert rule.is_active == True
        assert len(rule.weights) == 16
        assert len(rule.thresholds) == 16
    
    def test_sample_career_rules_fixture(self, sample_career_rules):
        """Test sample_career_rules fixture creates multiple rules."""
        assert len(sample_career_rules) == 5
        active_rules = [r for r in sample_career_rules if r.is_active]
        inactive_rules = [r for r in sample_career_rules if not r.is_active]
        assert len(active_rules) == 4
        assert len(inactive_rules) == 1
    
    def test_create_answers_fixture(self, create_answers, eq_questions):
        """Test create_answers fixture creates valid answers."""
        # With specific value
        answers = create_answers(eq_questions, value=4)
        assert len(answers) == len(eq_questions)
        assert all(a["answer_value"] == 4 for a in answers)
        
        # With random values
        random_answers = create_answers(eq_questions)
        assert len(random_answers) == len(eq_questions)
        assert all(1 <= a["answer_value"] <= 5 for a in random_answers)
    
    def test_mock_db_session_fixture(self, mock_db_session):
        """Test mock_db_session fixture has required methods."""
        assert hasattr(mock_db_session, 'commit')
        assert hasattr(mock_db_session, 'rollback')
        assert hasattr(mock_db_session, 'close')
        assert hasattr(mock_db_session, 'execute')
        assert hasattr(mock_db_session, 'add')
    
    def test_mock_assessment_fixture(self, mock_assessment):
        """Test mock_assessment fixture creates valid assessment."""
        assert mock_assessment.status == "in_progress"
        assert mock_assessment.answered_questions == 0
        assert mock_assessment.completed_at is None
