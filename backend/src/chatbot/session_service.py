from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models.chatbot_session import ChatbotSession
from models.user import User
from services.session import SessionService
import uuid
from datetime import datetime

class ChatbotSessionService:
    def __init__(self):
        self.session_service = SessionService()
    
    def create_session(self, user_id: str, db: Session) -> ChatbotSession:
        """Create a new chatbot session for user"""
        try:
            # Create session in database
            session_token = str(uuid.uuid4())
            chatbot_session = ChatbotSession(
                user_id=user_id,
                session_token=session_token,
                status="active",
                assessment_ready=False,
                results_viewed=False
            )
            
            db.add(chatbot_session)
            db.commit()
            db.refresh(chatbot_session)
            
            # Store session data in Redis
            session_data = {
                "user_id": user_id,
                "current_intent": "greeting",
                "context": {
                    "conversation_stage": "initial",
                    "assessment_ready": False,
                    "results_viewed": False
                },
                "assessment_ready": False,
                "results_viewed": False
            }
            
            self.session_service.redis_manager.create_session(
                session_token,
                user_id,
                session_data,
                expire_seconds=3600
            )
            
            return chatbot_session
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create chatbot session: {str(e)}")
    
    def get_session(self, session_token: str, db: Session) -> Optional[ChatbotSession]:
        """Get chatbot session by token"""
        return db.query(ChatbotSession).filter(
            ChatbotSession.session_token == session_token
        ).first()
    
    def update_session_status(self, session_token: str, status: str, db: Session) -> bool:
        """Update session status"""
        try:
            session = self.get_session(session_token, db)
            if session:
                session.status = status
                session.last_activity = datetime.utcnow()
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update session status: {str(e)}")
    
    def set_assessment_ready(self, session_token: str, db: Session) -> bool:
        """Mark session as ready for assessment"""
        try:
            session = self.get_session(session_token, db)
            if session:
                session.assessment_ready = True
                db.commit()
                
                # Update Redis
                self.session_service.redis_manager.update_session(
                    session_token,
                    {"assessment_ready": True, "context": {"conversation_stage": "assessment_ready"}}
                )
                return True
            return False
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to set assessment ready: {str(e)}")
    
    def set_results_viewed(self, session_token: str, db: Session) -> bool:
        """Mark that user has viewed results"""
        try:
            session = self.get_session(session_token, db)
            if session:
                session.results_viewed = True
                db.commit()
                
                # Update Redis
                self.session_service.redis_manager.update_session(
                    session_token,
                    {"results_viewed": True, "context": {"conversation_stage": "results_viewed"}}
                )
                return True
            return False
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to set results viewed: {str(e)}")
    
    def get_session_context(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Get session context from Redis"""
        return self.session_service.redis_manager.get_session(session_token)
    
    def update_session_context(self, session_token: str, context: Dict[str, Any]) -> bool:
        """Update session context in Redis"""
        return self.session_service.redis_manager.update_session(session_token, {"context": context})
    
    def is_session_active(self, session_token: str) -> bool:
        """Check if session is active"""
        return self.session_service.redis_manager.is_session_active(session_token)
    
    def extend_session(self, session_token: str, expire_seconds: int = 3600) -> bool:
        """Extend session expiration"""
        return self.session_service.redis_manager.extend_session(session_token, expire_seconds)
    
    def get_user_from_session(self, session_token: str, db: Session) -> Optional[User]:
        """Get user from session token"""
        session = self.get_session(session_token, db)
        if session:
            return db.query(User).filter(User.id == session.user_id).first()
        return None
