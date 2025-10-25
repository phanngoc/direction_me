from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .base import BaseAPI
from database.connection import get_db
from models.user import User
from models.assessment_session import AssessmentSession
from models.assessment_question import AssessmentQuestion
from models.assessment_response import AssessmentResponse
from assessment.session_service import AssessmentSessionService
from assessment.question_service import AssessmentQuestionService
import uuid
from datetime import datetime

class AssessmentAPI(BaseAPI):
    def __init__(self):
        super().__init__(prefix="/assessments", tags=["Assessments"])
        self.session_service = AssessmentSessionService()
        self.question_service = AssessmentQuestionService()
    
    def setup_routes(self):
        @self.router.post("/start")
        async def start_assessment(
            chatbot_session_id: str,
            user_id: str,
            db: Session = self.get_db_session()
        ):
            """Start assessment from chatbot session"""
            try:
                # Validate required fields
                self.validate_request_data(
                    {"chatbot_session_id": chatbot_session_id, "user_id": user_id},
                    ["chatbot_session_id", "user_id"]
                )
                
                # Create assessment session
                assessment_session = self.session_service.create_session(
                    user_id, chatbot_session_id, db
                )
                
                return self.create_response(assessment_session, "Assessment started")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to start assessment")
        
        @self.router.get("/{session_id}/questions")
        async def get_questions(
            session_id: str,
            module: str,
            limit: Optional[int] = None,
            db: Session = self.get_db_session()
        ):
            """Get assessment questions for a module"""
            try:
                # Validate session exists
                session = self.session_service.get_session(session_id, db)
                if not session:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Assessment session not found"
                    )
                
                # Get questions for module
                if limit:
                    questions = self.question_service.get_random_questions(module, limit, db)
                else:
                    questions = self.question_service.get_questions_by_module(module, db)
                
                return self.create_response(questions, "Questions retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to retrieve questions")
        
        @self.router.get("/{session_id}/sequence")
        async def get_assessment_sequence(
            session_id: str,
            db: Session = self.get_db_session()
        ):
            """Get complete assessment sequence"""
            try:
                # Validate session exists
                session = self.session_service.get_session(session_id, db)
                if not session:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Assessment session not found"
                    )
                
                # Get complete assessment sequence
                sequence = self.question_service.get_assessment_sequence(db)
                
                return self.create_response(sequence, "Assessment sequence retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to retrieve assessment sequence")
        
        @self.router.post("/{session_id}/responses")
        async def submit_response(
            session_id: str,
            question_id: str,
            answer: str,
            answer_value: Optional[int] = None,
            response_time_seconds: Optional[int] = None,
            user_id: str = None,
            db: Session = self.get_db_session()
        ):
            """Submit assessment response"""
            try:
                # Validate session exists
                session = self.session_service.get_session(session_id, db)
                if not session:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Assessment session not found"
                    )
                
                # Get user_id from session if not provided
                if not user_id:
                    user_id = session.user_id
                
                # Validate question exists
                question = self.question_service.get_question_by_id(question_id, db)
                if not question:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Question not found"
                    )
                
                # Validate response
                validation = self.question_service.validate_response(question, answer, answer_value)
                if not validation["is_valid"]:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=validation["feedback"]
                    )
                
                # Add response
                response = self.session_service.add_response(
                    session_id, question_id, user_id, answer, 
                    answer_value, response_time_seconds, db
                )
                
                # Update response with score
                response.score = validation["score"]
                db.commit()
                
                return self.create_response({
                    "response": response,
                    "validation": validation
                }, "Response submitted")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to submit response")
        
        @self.router.post("/{session_id}/complete")
        async def complete_assessment(
            session_id: str,
            db: Session = self.get_db_session()
        ):
            """Complete assessment session"""
            try:
                # Validate session exists
                session = self.session_service.get_session(session_id, db)
                if not session:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Assessment session not found"
                    )
                
                # Complete session
                completed_session = self.session_service.complete_session(session_id, db)
                
                return self.create_response(completed_session, "Assessment completed")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to complete assessment")
        
        @self.router.get("/{session_id}/progress")
        async def get_session_progress(
            session_id: str,
            db: Session = self.get_db_session()
        ):
            """Get assessment session progress"""
            try:
                progress = self.session_service.get_session_progress(session_id, db)
                
                if "error" in progress:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=progress["error"]
                    )
                
                return self.create_response(progress, "Progress retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to get session progress")
        
        @self.router.get("/{session_id}/responses")
        async def get_session_responses(
            session_id: str,
            db: Session = self.get_db_session()
        ):
            """Get all responses for a session"""
            try:
                responses = self.session_service.get_session_responses(session_id, db)
                
                return self.create_response(responses, "Responses retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to get session responses")
