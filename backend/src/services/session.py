from typing import Optional, Dict, Any
import uuid
import time
from redis.connection import session_manager
from models.chatbot_session import ChatbotSession
from models.user import User
from database.connection import get_db
from sqlalchemy.orm import Session

class SessionService:
    def __init__(self):
        self.redis_manager = session_manager
    
    def create_chatbot_session(self, user_id: str, db: Session) -> ChatbotSession:
        """Create a new chatbot session"""
        session_token = str(uuid.uuid4())
        
        # Create session in database
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
            "current_intent": None,
            "context": {},
            "assessment_ready": False,
            "results_viewed": False
        }
        
        self.redis_manager.create_session(
            session_token, 
            user_id, 
            session_data, 
            expire_seconds=3600
        )
        
        return chatbot_session
    
    def get_chatbot_session(self, session_token: str, db: Session) -> Optional[ChatbotSession]:
        """Get chatbot session by token"""
        return db.query(ChatbotSession).filter(
            ChatbotSession.session_token == session_token
        ).first()
    
    def update_session_context(self, session_token: str, context: Dict[str, Any]) -> bool:
        """Update session context in Redis"""
        return self.redis_manager.update_session(session_token, {"context": context})
    
    def set_assessment_ready(self, session_token: str) -> bool:
        """Mark session as ready for assessment"""
        return self.redis_manager.update_session(session_token, {"assessment_ready": True})
    
    def set_results_viewed(self, session_token: str) -> bool:
        """Mark that user has viewed results"""
        return self.redis_manager.update_session(session_token, {"results_viewed": True})
    
    def get_session_data(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Get session data from Redis"""
        return self.redis_manager.get_session(session_token)
    
    def extend_session(self, session_token: str, expire_seconds: int = 3600) -> bool:
        """Extend session expiration"""
        return self.redis_manager.extend_session(session_token, expire_seconds)
    
    def delete_session(self, session_token: str) -> bool:
        """Delete session from Redis"""
        return self.redis_manager.delete_session(session_token)
    
    def is_session_active(self, session_token: str) -> bool:
        """Check if session is active"""
        session_data = self.get_session_data(session_token)
        return session_data is not None
    
    def get_user_from_session(self, session_token: str, db: Session) -> Optional[User]:
        """Get user from session token"""
        chatbot_session = self.get_chatbot_session(session_token, db)
        if chatbot_session:
            return db.query(User).filter(User.id == chatbot_session.user_id).first()
        return None
