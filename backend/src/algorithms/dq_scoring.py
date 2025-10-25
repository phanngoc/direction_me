"""
DQ scoring algorithm for MyWay Career Assessment System.
"""
from typing import List, Dict, Any
from ..models.question_bank import QuestionBank


class DQScoringAlgorithm:
    """Algorithm for calculating DQ scores."""
    
    FACETS = ['dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration']
    
    @staticmethod
    def calculate_dq_score(answers: List[Dict[str, Any]], questions: List[QuestionBank]) -> Dict[str, float]:
        """
        Calculate DQ score using Likert scale normalization.
        
        Normalization: t_j = (6-x_j) if reverse else x_j, then t̂_j = 25*(t_j-1)
        Domain score: S_D = (1/|G_D|) * Σ(S_D,facet)
        """
        # Group questions by facet
        facet_questions = {}
        for question in questions:
            if question.category == 'DQ':
                facet = question.facet.lower()
                if facet not in facet_questions:
                    facet_questions[facet] = []
                facet_questions[facet].append(question)
        
        # Calculate score for each facet
        facet_scores = {}
        for facet in DQScoringAlgorithm.FACETS:
            facet_key = facet.replace('dq_', '')
            if facet_key in facet_questions:
                facet_scores[facet] = DQScoringAlgorithm._calculate_facet_score(
                    answers, facet_questions[facet_key]
                )
            else:
                facet_scores[facet] = 0.0
        
        # Calculate overall DQ score
        overall_score = sum(facet_scores.values()) / len(facet_scores)
        
        return {
            'dq_score': overall_score,
            **facet_scores
        }
    
    @staticmethod
    def _calculate_facet_score(answers: List[Dict[str, Any]], questions: List[QuestionBank]) -> float:
        """Calculate score for a specific facet."""
        if not questions:
            return 0.0
        
        # Create answer lookup
        answer_lookup = {ans['question_id']: ans['answer_value'] for ans in answers}
        
        total_score = 0.0
        valid_questions = 0
        
        for question in questions:
            if question.id in answer_lookup:
                answer_value = answer_lookup[question.id]
                
                # Normalize Likert scale (1-5) to 0-100
                # t_j = (6-x_j) if reverse else x_j
                if question.reverse_score:
                    normalized_value = 6 - answer_value
                else:
                    normalized_value = answer_value
                
                # t̂_j = 25*(t_j-1) to get 0-100 scale
                facet_score = 25 * (normalized_value - 1)
                total_score += facet_score
                valid_questions += 1
        
        if valid_questions == 0:
            return 0.0
        
        return total_score / valid_questions
    
    @staticmethod
    def get_facet_display_names() -> Dict[str, str]:
        """Get display names for DQ facets."""
        return {
            'dq_info_literacy': 'Information Literacy',
            'dq_creativity': 'Creativity',
            'dq_safety': 'Safety',
            'dq_collaboration': 'Collaboration'
        }
    
    @staticmethod
    def validate_answers(answers: List[Dict[str, Any]], questions: List[QuestionBank]) -> bool:
        """Validate that all required questions are answered."""
        if not answers or not questions:
            return False
        
        answer_question_ids = {ans['question_id'] for ans in answers}
        required_question_ids = {str(q.id) for q in questions if q.category == 'DQ'}
        
        return answer_question_ids.issuperset(required_question_ids)