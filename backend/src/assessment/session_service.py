from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from models.assessment_session import AssessmentSession
from models.assessment_response import AssessmentResponse
from models.assessment_result import AssessmentResult
from models.user import User
import uuid
from datetime import datetime, timedelta

class AssessmentSessionService:
    def __init__(self):
        pass
    
    def create_session(self, user_id: str, chatbot_session_id: str, db: Session) -> AssessmentSession:
        """Create a new assessment session"""
        try:
            assessment_session = AssessmentSession(
                user_id=user_id,
                chatbot_session_id=chatbot_session_id,
                status="in_progress",
                rushing_detected=False
            )
            
            db.add(assessment_session)
            db.commit()
            db.refresh(assessment_session)
            
            return assessment_session
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create assessment session: {str(e)}")
    
    def get_session(self, session_id: str, db: Session) -> Optional[AssessmentSession]:
        """Get assessment session by ID"""
        return db.query(AssessmentSession).filter(
            AssessmentSession.id == session_id
        ).first()
    
    def get_user_sessions(self, user_id: str, db: Session) -> List[AssessmentSession]:
        """Get all assessment sessions for a user"""
        return db.query(AssessmentSession).filter(
            AssessmentSession.user_id == user_id
        ).order_by(AssessmentSession.started_at.desc()).all()
    
    def update_session_status(self, session_id: str, status: str, db: Session) -> bool:
        """Update session status"""
        try:
            session = self.get_session(session_id, db)
            if session:
                session.status = status
                if status == "completed":
                    session.completed_at = datetime.utcnow()
                    # Calculate total time
                    if session.started_at:
                        total_time = session.completed_at - session.started_at
                        session.total_time_minutes = int(total_time.total_seconds() / 60)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update session status: {str(e)}")
    
    def add_response(self, session_id: str, question_id: str, user_id: str, 
                    answer: str, answer_value: int = None, response_time_seconds: int = None, 
                    db: Session) -> AssessmentResponse:
        """Add assessment response"""
        try:
            response = AssessmentResponse(
                session_id=session_id,
                question_id=question_id,
                user_id=user_id,
                answer=answer,
                answer_value=answer_value,
                response_time_seconds=response_time_seconds
            )
            
            db.add(response)
            db.commit()
            db.refresh(response)
            
            return response
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to add response: {str(e)}")
    
    def get_session_responses(self, session_id: str, db: Session) -> List[AssessmentResponse]:
        """Get all responses for a session"""
        return db.query(AssessmentResponse).filter(
            AssessmentResponse.session_id == session_id
        ).all()
    
    def get_session_progress(self, session_id: str, db: Session) -> Dict[str, Any]:
        """Get session progress information"""
        try:
            session = self.get_session(session_id, db)
            if not session:
                return {"error": "Session not found"}
            
            responses = self.get_session_responses(session_id, db)
            
            # Group responses by module
            module_responses = {}
            for response in responses:
                # This would need to be joined with questions to get module info
                # For now, return basic progress
                pass
            
            progress = {
                "session_id": session_id,
                "status": session.status,
                "total_responses": len(responses),
                "started_at": session.started_at.isoformat() if session.started_at else None,
                "completed_at": session.completed_at.isoformat() if session.completed_at else None,
                "total_time_minutes": session.total_time_minutes,
                "rushing_detected": session.rushing_detected,
                "consistency_score": session.consistency_score
            }
            
            return progress
            
        except Exception as e:
            return {"error": f"Failed to get session progress: {str(e)}"}
    
    def check_rushing_behavior(self, session_id: str, db: Session) -> bool:
        """Check if user is rushing through questions"""
        try:
            responses = self.get_session_responses(session_id, db)
            
            if len(responses) < 3:
                return False
            
            # Calculate average response time
            response_times = [r.response_time_seconds for r in responses if r.response_time_seconds]
            if not response_times:
                return False
            
            avg_response_time = sum(response_times) / len(response_times)
            
            # Consider rushing if average response time is less than 10 seconds
            is_rushing = avg_response_time < 10
            
            if is_rushing:
                session = self.get_session(session_id, db)
                if session:
                    session.rushing_detected = True
                    db.commit()
            
            return is_rushing
            
        except Exception as e:
            print(f"Error checking rushing behavior: {e}")
            return False
    
    def calculate_consistency_score(self, session_id: str, db: Session) -> float:
        """Calculate response consistency score"""
        try:
            responses = self.get_session_responses(session_id, db)
            
            if len(responses) < 2:
                return 1.0
            
            # Simple consistency check - compare similar questions
            # This is a placeholder implementation
            consistency_score = 0.85  # Default score
            
            session = self.get_session(session_id, db)
            if session:
                session.consistency_score = consistency_score
                db.commit()
            
            return consistency_score
            
        except Exception as e:
            print(f"Error calculating consistency score: {e}")
            return 0.5
    
    def complete_session(self, session_id: str, db: Session) -> AssessmentSession:
        """Complete assessment session"""
        try:
            session = self.get_session(session_id, db)
            if not session:
                raise Exception("Session not found")
            
            # Update status
            session.status = "completed"
            session.completed_at = datetime.utcnow()
            
            # Calculate total time
            if session.started_at:
                total_time = session.completed_at - session.started_at
                session.total_time_minutes = int(total_time.total_seconds() / 60)
            
            # Check for rushing behavior
            self.check_rushing_behavior(session_id, db)
            
            # Calculate consistency score
            self.calculate_consistency_score(session_id, db)
            
            db.commit()
            db.refresh(session)
            
            return session
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to complete session: {str(e)}")
    
    def get_session_result(self, session_id: str, db: Session) -> Optional[AssessmentResult]:
        """Get assessment result for completed session"""
        return db.query(AssessmentResult).filter(
            AssessmentResult.session_id == session_id
        ).first()
