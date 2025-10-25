from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from models.assessment_response import AssessmentResponse
from models.assessment_question import AssessmentQuestion
from models.assessment_result import AssessmentResult
import statistics
from datetime import datetime

class AssessmentScoringService:
    def __init__(self):
        pass
    
    def calculate_iq_score(self, responses: List[AssessmentResponse], db: Session) -> Dict[str, Any]:
        """Calculate IQ score from responses"""
        try:
            iq_responses = [r for r in responses if self._is_iq_question(r.question_id, db)]
            
            if not iq_responses:
                return {"score": 0, "max_score": 0, "percentage": 0, "details": {}}
            
            total_score = 0
            max_score = 0
            correct_answers = 0
            total_questions = len(iq_responses)
            
            for response in iq_responses:
                question = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.id == response.question_id
                ).first()
                
                if question and question.correct_answer:
                    if response.answer.strip().lower() == question.correct_answer.lower():
                        correct_answers += 1
                        total_score += 1
                    max_score += 1
                else:
                    # Partial credit for questions without correct answer
                    total_score += 0.5
                    max_score += 1
            
            percentage = (total_score / max_score) * 100 if max_score > 0 else 0
            
            return {
                "score": round(total_score, 2),
                "max_score": max_score,
                "percentage": round(percentage, 2),
                "correct_answers": correct_answers,
                "total_questions": total_questions,
                "details": {
                    "accuracy": round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0
                }
            }
            
        except Exception as e:
            raise Exception(f"Failed to calculate IQ score: {str(e)}")
    
    def calculate_emotional_quotient_score(self, responses: List[AssessmentResponse], db: Session) -> Dict[str, Any]:
        """Calculate EQ score from Likert scale responses"""
        try:
            eq_responses = [r for r in responses if self._is_eq_question(r.question_id, db)]
            
            if not eq_responses:
                return {"score": 0, "max_score": 0, "percentage": 0, "details": {}}
            
            # Group by facets
            facet_scores = {}
            total_score = 0
            max_score = 0
            
            for response in eq_responses:
                question = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.id == response.question_id
                ).first()
                
                if question and response.answer_value is not None:
                    facet = question.facet or "general"
                    
                    # Apply reverse scoring if needed
                    if question.reverse_scored:
                        score = 6 - response.answer_value
                    else:
                        score = response.answer_value
                    
                    if facet not in facet_scores:
                        facet_scores[facet] = []
                    facet_scores[facet].append(score)
                    
                    total_score += score
                    max_score += 5  # Max value for Likert scale
            
            # Calculate average scores per facet
            facet_averages = {}
            for facet, scores in facet_scores.items():
                facet_averages[facet] = {
                    "average": round(statistics.mean(scores), 2),
                    "count": len(scores)
                }
            
            percentage = (total_score / max_score) * 100 if max_score > 0 else 0
            
            return {
                "score": round(total_score, 2),
                "max_score": max_score,
                "percentage": round(percentage, 2),
                "facet_scores": facet_averages,
                "details": {
                    "total_responses": len(eq_responses),
                    "facets_covered": len(facet_scores)
                }
            }
            
        except Exception as e:
            raise Exception(f"Failed to calculate EQ score: {str(e)}")
    
    def calculate_digital_quotient_score(self, responses: List[AssessmentResponse], db: Session) -> Dict[str, Any]:
        """Calculate DQ score from Likert scale responses"""
        try:
            dq_responses = [r for r in responses if self._is_dq_question(r.question_id, db)]
            
            if not dq_responses:
                return {"score": 0, "max_score": 0, "percentage": 0, "details": {}}
            
            # Similar to EQ calculation
            facet_scores = {}
            total_score = 0
            max_score = 0
            
            for response in dq_responses:
                question = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.id == response.question_id
                ).first()
                
                if question and response.answer_value is not None:
                    facet = question.facet or "general"
                    
                    if question.reverse_scored:
                        score = 6 - response.answer_value
                    else:
                        score = response.answer_value
                    
                    if facet not in facet_scores:
                        facet_scores[facet] = []
                    facet_scores[facet].append(score)
                    
                    total_score += score
                    max_score += 5
            
            facet_averages = {}
            for facet, scores in facet_scores.items():
                facet_averages[facet] = {
                    "average": round(statistics.mean(scores), 2),
                    "count": len(scores)
                }
            
            percentage = (total_score / max_score) * 100 if max_score > 0 else 0
            
            return {
                "score": round(total_score, 2),
                "max_score": max_score,
                "percentage": round(percentage, 2),
                "facet_scores": facet_averages,
                "details": {
                    "total_responses": len(dq_responses),
                    "facets_covered": len(facet_scores)
                }
            }
            
        except Exception as e:
            raise Exception(f"Failed to calculate DQ score: {str(e)}")
    
    def calculate_adaptability_quotient_score(self, responses: List[AssessmentResponse], db: Session) -> Dict[str, Any]:
        """Calculate AQ score from Likert scale responses"""
        try:
            aq_responses = [r for r in responses if self._is_aq_question(r.question_id, db)]
            
            if not aq_responses:
                return {"score": 0, "max_score": 0, "percentage": 0, "details": {}}
            
            # Similar calculation to EQ and DQ
            facet_scores = {}
            total_score = 0
            max_score = 0
            
            for response in aq_responses:
                question = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.id == response.question_id
                ).first()
                
                if question and response.answer_value is not None:
                    facet = question.facet or "general"
                    
                    if question.reverse_scored:
                        score = 6 - response.answer_value
                    else:
                        score = response.answer_value
                    
                    if facet not in facet_scores:
                        facet_scores[facet] = []
                    facet_scores[facet].append(score)
                    
                    total_score += score
                    max_score += 5
            
            facet_averages = {}
            for facet, scores in facet_scores.items():
                facet_averages[facet] = {
                    "average": round(statistics.mean(scores), 2),
                    "count": len(scores)
                }
            
            percentage = (total_score / max_score) * 100 if max_score > 0 else 0
            
            return {
                "score": round(total_score, 2),
                "max_score": max_score,
                "percentage": round(percentage, 2),
                "facet_scores": facet_averages,
                "details": {
                    "total_responses": len(aq_responses),
                    "facets_covered": len(facet_scores)
                }
            }
            
        except Exception as e:
            raise Exception(f"Failed to calculate AQ score: {str(e)}")
    
    def calculate_ikigai_scores(self, responses: List[AssessmentResponse], db: Session) -> Dict[str, float]:
        """Calculate Ikigai intersection scores"""
        try:
            # Map responses to Ikigai dimensions
            ikigai_scores = {
                "love": 0,      # What you love
                "good_at": 0,   # What you're good at
                "world_needs": 0,  # What the world needs
                "paid_for": 0   # What you can be paid for
            }
            
            # This is a simplified mapping - in practice, you'd have specific questions for each dimension
            for response in responses:
                question = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.id == response.question_id
                ).first()
                
                if question and response.answer_value is not None:
                    # Map question facets to Ikigai dimensions
                    facet = question.facet or ""
                    
                    if "love" in facet.lower() or "passion" in facet.lower():
                        ikigai_scores["love"] += response.answer_value
                    elif "skill" in facet.lower() or "ability" in facet.lower():
                        ikigai_scores["good_at"] += response.answer_value
                    elif "need" in facet.lower() or "impact" in facet.lower():
                        ikigai_scores["world_needs"] += response.answer_value
                    elif "career" in facet.lower() or "job" in facet.lower():
                        ikigai_scores["paid_for"] += response.answer_value
            
            # Normalize scores to 0-100 range
            for key in ikigai_scores:
                ikigai_scores[key] = min(100, max(0, ikigai_scores[key] * 20))  # Scale to 100
            
            return ikigai_scores
            
        except Exception as e:
            raise Exception(f"Failed to calculate Ikigai scores: {str(e)}")
    
    def calculate_percentiles(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate percentile rankings for scores"""
        try:
            # This would typically use a database of population scores
            # For now, use simplified percentile calculation
            percentiles = {}
            
            for quotient, score in scores.items():
                # Simplified percentile calculation
                if score >= 90:
                    percentiles[quotient] = 95
                elif score >= 80:
                    percentiles[quotient] = 85
                elif score >= 70:
                    percentiles[quotient] = 75
                elif score >= 60:
                    percentiles[quotient] = 65
                elif score >= 50:
                    percentiles[quotient] = 55
                else:
                    percentiles[quotient] = 45
            
            return percentiles
            
        except Exception as e:
            raise Exception(f"Failed to calculate percentiles: {str(e)}")
    
    def identify_strongest_weakest(self, scores: Dict[str, float]) -> Tuple[str, str]:
        """Identify strongest and weakest quotients"""
        try:
            if not scores:
                return "IQ", "IQ"
            
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            strongest = sorted_scores[0][0]
            weakest = sorted_scores[-1][0]
            
            return strongest, weakest
            
        except Exception as e:
            return "IQ", "IQ"
    
    def _is_iq_question(self, question_id: str, db: Session) -> bool:
        """Check if question is IQ type"""
        question = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.id == question_id
        ).first()
        return question and question.module == "IQ"
    
    def _is_eq_question(self, question_id: str, db: Session) -> bool:
        """Check if question is EQ type"""
        question = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.id == question_id
        ).first()
        return question and question.module == "EQ"
    
    def _is_dq_question(self, question_id: str, db: Session) -> bool:
        """Check if question is DQ type"""
        question = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.id == question_id
        ).first()
        return question and question.module == "DQ"
    
    def _is_aq_question(self, question_id: str, db: Session) -> bool:
        """Check if question is AQ type"""
        question = db.query(AssessmentQuestion).filter(
            AssessmentQuestion.id == question_id
        ).first()
        return question and question.module == "AQ"
