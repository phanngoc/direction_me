from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .base import BaseAPI
from database.connection import get_db
from models.user import User
from models.assessment_result import AssessmentResult
from models.career_recommendation import CareerRecommendation
from models.visualization_data import VisualizationData
from assessment.results_service import ResultsService

class ResultsAPI(BaseAPI):
    def __init__(self):
        super().__init__(prefix="/results", tags=["Results"])
        self.results_service = ResultsService()
    
    def setup_routes(self):
        @self.router.get("/{result_id}")
        async def get_results(
            result_id: str,
            db: Session = self.get_db_session()
        ):
            """Get assessment results"""
            try:
                result = self.results_service.get_results(result_id, db)
                
                if not result:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Results not found"
                    )
                
                return self.create_response(result, "Results retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to retrieve results")
        
        @self.router.post("/calculate")
        async def calculate_results(
            session_id: str,
            user_id: str,
            chatbot_session_id: str,
            db: Session = self.get_db_session()
        ):
            """Calculate assessment results"""
            try:
                # Validate required fields
                self.validate_request_data(
                    {"session_id": session_id, "user_id": user_id, "chatbot_session_id": chatbot_session_id},
                    ["session_id", "user_id", "chatbot_session_id"]
                )
                
                result = self.results_service.calculate_complete_results(
                    session_id, user_id, chatbot_session_id, db
                )
                
                return self.create_response(result, "Results calculated successfully")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to calculate results")
        
        @self.router.get("/{result_id}/visualizations")
        async def get_visualization_data(
            result_id: str,
            chart_type: Optional[str] = None,
            db: Session = self.get_db_session()
        ):
            """Get visualization data"""
            try:
                visualizations = self.results_service.get_visualization_data(result_id, chart_type, db)
                
                return self.create_response(visualizations, "Visualization data retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to retrieve visualization data")
        
        @self.router.get("/{result_id}/recommendations")
        async def get_career_recommendations(
            result_id: str,
            db: Session = self.get_db_session()
        ):
            """Get career recommendations"""
            try:
                recommendations = self.results_service.get_career_recommendations(result_id, db)
                
                return self.create_response(recommendations, "Recommendations retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to retrieve recommendations")
        
        @self.router.get("/user/{user_id}")
        async def get_user_results(
            user_id: str,
            db: Session = self.get_db_session()
        ):
            """Get all results for a user"""
            try:
                results = self.results_service.get_user_results(user_id, db)
                
                return self.create_response(results, "User results retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to retrieve user results")
