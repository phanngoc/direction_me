"""
Unit tests for scoring algorithms.
"""
import pytest
from unittest.mock import Mock
from backend.src.algorithms.iq_scoring import IQScoringAlgorithm
from backend.src.algorithms.eq_scoring import EQScoringAlgorithm
from backend.src.algorithms.dq_scoring import DQScoringAlgorithm
from backend.src.algorithms.aq_scoring import AQScoringAlgorithm


class TestIQScoringAlgorithm:
    """Test IQ scoring algorithm."""
    
    def test_calculate_iq_score_basic(self):
        """Test basic IQ score calculation."""
        # Mock questions
        questions = [
            Mock(id="q1", category="IQ", facet="LR", difficulty_weight=1.0, question_type="MCQ"),
            Mock(id="q2", category="IQ", facet="NR", difficulty_weight=1.2, question_type="MCQ"),
        ]
        
        # Mock answers (all correct)
        answers = [
            {"question_id": "q1", "answer_value": 1},
            {"question_id": "q2", "answer_value": 1},
        ]
        
        result = IQScoringAlgorithm.calculate_iq_score(answers, questions)
        
        assert "iq_score" in result
        assert result["iq_score"] == 100.0  # All correct answers
        assert "iq_lr" in result
        assert "iq_nr" in result
        assert "iq_vr" in result
        assert "iq_sr" in result
    
    def test_calculate_iq_score_partial(self):
        """Test IQ score calculation with partial answers."""
        questions = [
            Mock(id="q1", category="IQ", facet="LR", difficulty_weight=1.0, question_type="MCQ"),
            Mock(id="q2", category="IQ", facet="NR", difficulty_weight=1.0, question_type="MCQ"),
        ]
        
        # Only one correct answer
        answers = [
            {"question_id": "q1", "answer_value": 1},
            {"question_id": "q2", "answer_value": 0},
        ]
        
        result = IQScoringAlgorithm.calculate_iq_score(answers, questions)
        
        assert result["iq_score"] == 50.0  # Half correct
        assert result["iq_lr"] == 100.0
        assert result["iq_nr"] == 0.0
    
    def test_validate_answers(self):
        """Test answer validation."""
        questions = [
            Mock(id="q1", category="IQ", facet="LR", is_active=True),
            Mock(id="q2", category="IQ", facet="NR", is_active=True),
        ]
        
        # Valid answers
        valid_answers = [
            {"question_id": "q1", "answer_value": 1},
            {"question_id": "q2", "answer_value": 1},
        ]
        
        assert IQScoringAlgorithm.validate_answers(valid_answers, questions) == True
        
        # Invalid answers (missing one)
        invalid_answers = [
            {"question_id": "q1", "answer_value": 1},
        ]
        
        assert IQScoringAlgorithm.validate_answers(invalid_answers, questions) == False


class TestEQScoringAlgorithm:
    """Test EQ scoring algorithm."""
    
    def test_calculate_eq_score_basic(self):
        """Test basic EQ score calculation."""
        questions = [
            Mock(id="q1", category="EQ", facet="Empathy", reverse_score=False, question_type="Likert"),
            Mock(id="q2", category="EQ", facet="Social", reverse_score=False, question_type="Likert"),
        ]
        
        # High scores (5 on Likert scale)
        answers = [
            {"question_id": "q1", "answer_value": 5},
            {"question_id": "q2", "answer_value": 5},
        ]
        
        result = EQScoringAlgorithm.calculate_eq_score(answers, questions)
        
        assert "eq_score" in result
        assert result["eq_score"] == 100.0  # Maximum score
        assert "eq_empathy" in result
        assert "eq_social" in result
    
    def test_calculate_eq_score_reverse(self):
        """Test EQ score calculation with reverse scoring."""
        questions = [
            Mock(id="q1", category="EQ", facet="Empathy", reverse_score=True, question_type="Likert"),
        ]
        
        # Low score (1) should become high score (5) after reverse
        answers = [
            {"question_id": "q1", "answer_value": 1},
        ]
        
        result = EQScoringAlgorithm.calculate_eq_score(answers, questions)
        
        assert result["eq_empathy"] == 100.0  # Reversed from 1 to 5
    
    def test_calculate_eq_score_mixed(self):
        """Test EQ score calculation with mixed scores."""
        questions = [
            Mock(id="q1", category="EQ", facet="Empathy", reverse_score=False, question_type="Likert"),
            Mock(id="q2", category="EQ", facet="Social", reverse_score=False, question_type="Likert"),
        ]
        
        # Mixed scores
        answers = [
            {"question_id": "q1", "answer_value": 3},  # Middle score
            {"question_id": "q2", "answer_value": 4},  # High score
        ]
        
        result = EQScoringAlgorithm.calculate_eq_score(answers, questions)
        
        assert 50.0 <= result["eq_score"] <= 75.0  # Between middle and high


class TestDQScoringAlgorithm:
    """Test DQ scoring algorithm."""
    
    def test_calculate_dq_score_basic(self):
        """Test basic DQ score calculation."""
        questions = [
            Mock(id="q1", category="DQ", facet="InfoLiteracy", reverse_score=False, question_type="Likert"),
            Mock(id="q2", category="DQ", facet="Creativity", reverse_score=False, question_type="Likert"),
        ]
        
        # High scores
        answers = [
            {"question_id": "q1", "answer_value": 5},
            {"question_id": "q2", "answer_value": 5},
        ]
        
        result = DQScoringAlgorithm.calculate_dq_score(answers, questions)
        
        assert "dq_score" in result
        assert result["dq_score"] == 100.0
        assert "dq_info_literacy" in result
        assert "dq_creativity" in result


class TestAQScoringAlgorithm:
    """Test AQ scoring algorithm."""
    
    def test_calculate_aq_score_basic(self):
        """Test basic AQ score calculation."""
        questions = [
            Mock(id="q1", category="AQ", facet="Control", reverse_score=False, question_type="Likert"),
            Mock(id="q2", category="AQ", facet="Ownership", reverse_score=False, question_type="Likert"),
        ]
        
        # High scores
        answers = [
            {"question_id": "q1", "answer_value": 5},
            {"question_id": "q2", "answer_value": 5},
        ]
        
        result = AQScoringAlgorithm.calculate_aq_score(answers, questions)
        
        assert "aq_score" in result
        assert result["aq_score"] == 100.0
        assert "aq_control" in result
        assert "aq_ownership" in result
    
    def test_calculate_aq_score_reverse(self):
        """Test AQ score calculation with reverse scoring."""
        questions = [
            Mock(id="q1", category="AQ", facet="Control", reverse_score=True, question_type="Likert"),
        ]
        
        # Low score should become high score after reverse
        answers = [
            {"question_id": "q1", "answer_value": 1},
        ]
        
        result = AQScoringAlgorithm.calculate_aq_score(answers, questions)
        
        assert result["aq_control"] == 100.0


class TestScoringIntegration:
    """Integration tests for all scoring algorithms."""
    
    def test_all_algorithms_with_complete_data(self):
        """Test all algorithms with complete assessment data."""
        # Create comprehensive test data
        questions = []
        answers = []
        
        # IQ questions
        for i, facet in enumerate(["LR", "NR", "VR", "SR"]):
            questions.append(Mock(
                id=f"iq_{i+1}",
                category="IQ",
                facet=facet,
                difficulty_weight=1.0,
                question_type="MCQ"
            ))
            answers.append({"question_id": f"iq_{i+1}", "answer_value": 1})
        
        # EQ questions
        for i, facet in enumerate(["Empathy", "Social", "SelfAwareness", "SelfRegulation"]):
            questions.append(Mock(
                id=f"eq_{i+1}",
                category="EQ",
                facet=facet,
                reverse_score=False,
                question_type="Likert"
            ))
            answers.append({"question_id": f"eq_{i+1}", "answer_value": 4})
        
        # DQ questions
        for i, facet in enumerate(["InfoLiteracy", "Creativity", "Safety", "Collaboration"]):
            questions.append(Mock(
                id=f"dq_{i+1}",
                category="DQ",
                facet=facet,
                reverse_score=False,
                question_type="Likert"
            ))
            answers.append({"question_id": f"dq_{i+1}", "answer_value": 4})
        
        # AQ questions
        for i, facet in enumerate(["Control", "Ownership", "Reach", "Endurance"]):
            questions.append(Mock(
                id=f"aq_{i+1}",
                category="AQ",
                facet=facet,
                reverse_score=False,
                question_type="Likert"
            ))
            answers.append({"question_id": f"aq_{i+1}", "answer_value": 4})
        
        # Test all algorithms
        iq_result = IQScoringAlgorithm.calculate_iq_score(answers, questions)
        eq_result = EQScoringAlgorithm.calculate_eq_score(answers, questions)
        dq_result = DQScoringAlgorithm.calculate_dq_score(answers, questions)
        aq_result = AQScoringAlgorithm.calculate_aq_score(answers, questions)
        
        # Verify all results have expected structure
        assert all(key in iq_result for key in ["iq_score", "iq_lr", "iq_nr", "iq_vr", "iq_sr"])
        assert all(key in eq_result for key in ["eq_score", "eq_empathy", "eq_social", "eq_self_awareness", "eq_self_regulation"])
        assert all(key in dq_result for key in ["dq_score", "dq_info_literacy", "dq_creativity", "dq_safety", "dq_collaboration"])
        assert all(key in aq_result for key in ["aq_score", "aq_control", "aq_ownership", "aq_reach", "aq_endurance"])
        
        # Verify scores are in valid range
        assert 0 <= iq_result["iq_score"] <= 100
        assert 0 <= eq_result["eq_score"] <= 100
        assert 0 <= dq_result["dq_score"] <= 100
        assert 0 <= aq_result["aq_score"] <= 100