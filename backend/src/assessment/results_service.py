from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from models.assessment_result import AssessmentResult
from models.assessment_response import AssessmentResponse
from models.career_recommendation import CareerRecommendation
from models.visualization_data import VisualizationData
from assessment.scoring_service import AssessmentScoringService
from services.career_service import CareerService
import uuid
from datetime import datetime

class ResultsService:
    def __init__(self):
        self.scoring_service = AssessmentScoringService()
        self.career_service = CareerService()
    
    def calculate_complete_results(self, session_id: str, user_id: str, chatbot_session_id: str, db: Session) -> AssessmentResult:
        """Calculate complete assessment results"""
        try:
            # Get all responses for the session
            responses = db.query(AssessmentResponse).filter(
                AssessmentResponse.session_id == session_id
            ).all()
            
            if not responses:
                raise Exception("No responses found for session")
            
            # Calculate scores for each quotient
            iq_score_data = self.scoring_service.calculate_iq_score(responses, db)
            eq_score_data = self.scoring_service.calculate_emotional_quotient_score(responses, db)
            dq_score_data = self.scoring_service.calculate_digital_quotient_score(responses, db)
            aq_score_data = self.scoring_service.calculate_adaptability_quotient_score(responses, db)
            
            # Calculate Ikigai scores
            ikigai_scores = self.scoring_service.calculate_ikigai_scores(responses, db)
            
            # Calculate percentiles
            quotient_scores = {
                "iq": iq_score_data["percentage"],
                "eq": eq_score_data["percentage"],
                "dq": dq_score_data["percentage"],
                "aq": aq_score_data["percentage"]
            }
            percentiles = self.scoring_service.calculate_percentiles(quotient_scores)
            
            # Identify strongest and weakest quotients
            strongest, weakest = self.scoring_service.identify_strongest_weakest(quotient_scores)
            
            # Calculate consistency score
            consistency_score = self._calculate_consistency_score(responses, db)
            
            # Create assessment result
            result = AssessmentResult(
                session_id=session_id,
                user_id=user_id,
                chatbot_session_id=chatbot_session_id,
                iq_score=iq_score_data["percentage"],
                eq_score=eq_score_data["percentage"],
                dq_score=dq_score_data["percentage"],
                aq_score=aq_score_data["percentage"],
                iq_percentile=percentiles.get("iq", 50),
                eq_percentile=percentiles.get("eq", 50),
                dq_percentile=percentiles.get("dq", 50),
                aq_percentile=percentiles.get("aq", 50),
                ikigai_love=ikigai_scores.get("love", 50),
                ikigai_good_at=ikigai_scores.get("good_at", 50),
                ikigai_world_needs=ikigai_scores.get("world_needs", 50),
                ikigai_paid_for=ikigai_scores.get("paid_for", 50),
                strongest_quotient=strongest,
                weakest_quotient=weakest,
                consistency_score=consistency_score,
                quality_flags=self._generate_quality_flags(responses, db)
            )
            
            db.add(result)
            db.commit()
            db.refresh(result)
            
            # Generate career recommendations
            self._generate_career_recommendations(result, db)
            
            # Generate visualization data
            self._generate_visualization_data(result, db)
            
            return result
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to calculate results: {str(e)}")
    
    def get_results(self, result_id: str, db: Session) -> Optional[AssessmentResult]:
        """Get assessment results by ID"""
        return db.query(AssessmentResult).filter(
            AssessmentResult.id == result_id
        ).first()
    
    def get_user_results(self, user_id: str, db: Session) -> List[AssessmentResult]:
        """Get all results for a user"""
        return db.query(AssessmentResult).filter(
            AssessmentResult.user_id == user_id
        ).order_by(AssessmentResult.created_at.desc()).all()
    
    def get_visualization_data(self, result_id: str, chart_type: str = None, db: Session) -> List[VisualizationData]:
        """Get visualization data for results"""
        query = db.query(VisualizationData).filter(
            VisualizationData.result_id == result_id
        )
        
        if chart_type:
            query = query.filter(VisualizationData.chart_type == chart_type)
        
        return query.all()
    
    def get_career_recommendations(self, result_id: str, db: Session) -> List[CareerRecommendation]:
        """Get career recommendations for results"""
        return db.query(CareerRecommendation).filter(
            CareerRecommendation.result_id == result_id
        ).order_by(CareerRecommendation.priority_rank).all()
    
    def _calculate_consistency_score(self, responses: List[AssessmentResponse], db: Session) -> float:
        """Calculate response consistency score"""
        try:
            if len(responses) < 2:
                return 1.0
            
            # Group responses by similar questions (same facet)
            facet_responses = {}
            for response in responses:
                question = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.id == response.question_id
                ).first()
                
                if question and question.facet:
                    if question.facet not in facet_responses:
                        facet_responses[question.facet] = []
                    facet_responses[question.facet].append(response.answer_value or 0)
            
            # Calculate consistency within facets
            consistency_scores = []
            for facet, values in facet_responses.items():
                if len(values) > 1:
                    # Calculate standard deviation (lower = more consistent)
                    mean_val = sum(values) / len(values)
                    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
                    std_dev = variance ** 0.5
                    
                    # Convert to consistency score (0-1, higher = more consistent)
                    consistency = max(0, 1 - (std_dev / 2))  # Normalize by max possible std dev
                    consistency_scores.append(consistency)
            
            # Return average consistency
            return round(sum(consistency_scores) / len(consistency_scores), 2) if consistency_scores else 0.5
            
        except Exception as e:
            return 0.5
    
    def _generate_quality_flags(self, responses: List[AssessmentResponse], db: Session) -> Dict[str, Any]:
        """Generate quality flags for assessment"""
        flags = {
            "rushing_detected": False,
            "inconsistent_responses": False,
            "incomplete_responses": False,
            "response_time_anomalies": False
        }
        
        try:
            # Check for rushing (very fast responses)
            fast_responses = [r for r in responses if r.response_time_seconds and r.response_time_seconds < 5]
            if len(fast_responses) > len(responses) * 0.3:  # More than 30% very fast
                flags["rushing_detected"] = True
            
            # Check for incomplete responses
            incomplete = [r for r in responses if not r.answer or r.answer.strip() == ""]
            if len(incomplete) > 0:
                flags["incomplete_responses"] = True
            
            # Check for response time anomalies
            response_times = [r.response_time_seconds for r in responses if r.response_time_seconds]
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                very_slow = [t for t in response_times if t > avg_time * 3]
                if len(very_slow) > len(response_times) * 0.2:  # More than 20% very slow
                    flags["response_time_anomalies"] = True
            
            return flags
            
        except Exception as e:
            return flags
    
    def _generate_career_recommendations(self, result: AssessmentResult, db: Session):
        """Generate career recommendations for results"""
        try:
            recommendations = self.career_service.generate_recommendations(result, db)
            
            for rec in recommendations:
                db.add(rec)
            
            db.commit()
            
        except Exception as e:
            print(f"Failed to generate career recommendations: {e}")
    
    def _generate_visualization_data(self, result: AssessmentResult, db: Session):
        """Generate visualization data for results"""
        try:
            # Radar chart data
            radar_data = {
                "labels": ["IQ", "EQ", "DQ", "AQ"],
                "datasets": [{
                    "label": "Điểm số của bạn",
                    "data": [result.iq_score, result.eq_score, result.dq_score, result.aq_score],
                    "backgroundColor": "rgba(59, 130, 246, 0.2)",
                    "borderColor": "rgba(59, 130, 246, 1)",
                    "borderWidth": 2
                }]
            }
            
            radar_viz = VisualizationData(
                result_id=result.id,
                user_id=result.user_id,
                chart_type="radar",
                chart_data=radar_data
            )
            db.add(radar_viz)
            
            # Facet bars data (simplified)
            facet_data = {
                "facets": ["Tư duy logic", "Giao tiếp", "Công nghệ", "Thích nghi"],
                "scores": [result.iq_score, result.eq_score, result.dq_score, result.aq_score]
            }
            
            facet_viz = VisualizationData(
                result_id=result.id,
                user_id=result.user_id,
                chart_type="facet_bars",
                chart_data=facet_data
            )
            db.add(facet_viz)
            
            # Ikigai map data
            ikigai_data = {
                "intersections": {
                    "love_good_at": (result.ikigai_love + result.ikigai_good_at) / 2,
                    "love_world_needs": (result.ikigai_love + result.ikigai_world_needs) / 2,
                    "good_at_paid_for": (result.ikigai_good_at + result.ikigai_paid_for) / 2,
                    "world_needs_paid_for": (result.ikigai_world_needs + result.ikigai_paid_for) / 2
                },
                "dimensions": {
                    "love": result.ikigai_love,
                    "good_at": result.ikigai_good_at,
                    "world_needs": result.ikigai_world_needs,
                    "paid_for": result.ikigai_paid_for
                }
            }
            
            ikigai_viz = VisualizationData(
                result_id=result.id,
                user_id=result.user_id,
                chart_type="ikigai_map",
                chart_data=ikigai_data
            )
            db.add(ikigai_viz)
            
            db.commit()
            
        except Exception as e:
            print(f"Failed to generate visualization data: {e}")
    
    def update_results(self, result_id: str, updates: Dict[str, Any], db: Session) -> AssessmentResult:
        """Update assessment results"""
        try:
            result = self.get_results(result_id, db)
            if not result:
                raise Exception("Result not found")
            
            for key, value in updates.items():
                if hasattr(result, key):
                    setattr(result, key, value)
            
            db.commit()
            db.refresh(result)
            
            return result
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update results: {str(e)}")
    
    def delete_results(self, result_id: str, db: Session) -> bool:
        """Delete assessment results"""
        try:
            result = self.get_results(result_id, db)
            if result:
                db.delete(result)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to delete results: {str(e)}")
