"""
IQ scoring algorithm for MyWay Career Assessment System.
"""
from typing import List, Dict, Any
from ..models.question_bank import QuestionBank


class IQScoringAlgorithm:
    """Algorithm for calculating IQ scores."""
    
    FACETS = ['iq_lr', 'iq_nr', 'iq_vr', 'iq_sr']  # Logical, Numerical, Verbal, Spatial
    
    @staticmethod
    def calculate_iq_score(answers: List[Dict[str, Any]], questions: List[QuestionBank]) -> Dict[str, float]:
        """
        Calculate IQ score using weighted difficulty formula.
        
        Formula: S_IQ = 100 * (Σ(d_i * r_i)) / Σ(d_i)
        Where: d_i = difficulty weight, r_i = correct/incorrect (0/1)
        """
        # Group questions by facet
        facet_questions = {}
        for question in questions:
            if question.category == 'IQ':
                facet = question.facet.lower()
                if facet not in facet_questions:
                    facet_questions[facet] = []
                facet_questions[facet].append(question)
        
        # Calculate score for each facet
        facet_scores = {}
        for facet in IQScoringAlgorithm.FACETS:
            facet_key = facet.replace('iq_', '')
            if facet_key in facet_questions:
                facet_scores[facet] = IQScoringAlgorithm._calculate_facet_score(
                    answers, facet_questions[facet_key]
                )
            else:
                facet_scores[facet] = 0.0
        
        # Calculate overall IQ score
        overall_score = sum(facet_scores.values()) / len(facet_scores)
        
        return {
            'iq_score': overall_score,
            **facet_scores
        }
    
    @staticmethod
    def _calculate_facet_score(answers: List[Dict[str, Any]], questions: List[QuestionBank]) -> float:
        """Calculate score for a specific facet."""
        if not questions:
            return 0.0
        
        # Create answer lookup
        answer_lookup = {ans['question_id']: ans['answer_value'] for ans in answers}
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for question in questions:
            if question.id in answer_lookup:
                answer_value = answer_lookup[question.id]
                difficulty_weight = float(question.difficulty_weight)
                
                # For MCQ questions, check if answer is correct (assuming answer_value is 1 for correct, 0 for incorrect)
                # For now, we'll use a simple scoring based on answer value
                if question.question_type == 'MCQ':
                    # In a real implementation, you'd check against correct answer
                    # For now, we'll use answer_value as correctness (0 or 1)
                    correctness = 1 if answer_value == 1 else 0
                else:
                    # For other question types, normalize to 0-1 scale
                    correctness = min(1.0, max(0.0, answer_value / 5.0))  # Assuming 5-point scale
                
                total_weighted_score += difficulty_weight * correctness
                total_weight += difficulty_weight
        
        if total_weight == 0:
            return 0.0
        
        # Convert to 0-100 scale
        return (total_weighted_score / total_weight) * 100
    
    @staticmethod
    def get_facet_display_names() -> Dict[str, str]:
        """Get display names for IQ facets."""
        return {
            'iq_lr': 'Logical Reasoning',
            'iq_nr': 'Numerical Reasoning',
            'iq_vr': 'Verbal Reasoning',
            'iq_sr': 'Spatial Reasoning'
        }
    
    @staticmethod
    def validate_answers(answers: List[Dict[str, Any]], questions: List[QuestionBank]) -> bool:
        """Validate that all required questions are answered."""
        if not answers or not questions:
            return False
        
        answer_question_ids = {ans['question_id'] for ans in answers}
        required_question_ids = {str(q.id) for q in questions if q.category == 'IQ'}
        
        return answer_question_ids.issuperset(required_question_ids)