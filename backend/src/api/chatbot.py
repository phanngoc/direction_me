from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .base import BaseAPI
from database.connection import get_db
from models.user import User
from models.chatbot_session import ChatbotSession
from models.chatbot_message import ChatbotMessage
from chatbot.session_service import ChatbotSessionService
from chatbot.message_service import ChatbotMessageService
import uuid
from datetime import datetime

class ChatbotAPI(BaseAPI):
    def __init__(self):
        super().__init__(prefix="/chatbot", tags=["Chatbot"])
        self.session_service = ChatbotSessionService()
        self.message_service = ChatbotMessageService()
    
    def setup_routes(self):
        @self.router.post("/sessions")
        async def start_chatbot_session(
            user_id: str,
            initial_message: Optional[str] = None,
            db: Session = self.get_db_session()
        ):
            """Start new chatbot session"""
            try:
                # Create chatbot session
                chatbot_session = self.session_service.create_session(user_id, db)
                
                # Process initial message if provided
                if initial_message:
                    result = self.message_service.process_message_flow(
                        str(chatbot_session.id), 
                        initial_message, 
                        "text", 
                        db
                    )
                
                return self.create_response(chatbot_session, "Chatbot session started")
            except Exception as e:
                raise self.handle_error(e, "Failed to start chatbot session")
        
        @self.router.post("/sessions/{session_id}/messages")
        async def send_message(
            session_id: str,
            content: str,
            message_type: str = "text",
            db: Session = self.get_db_session()
        ):
            """Send message to chatbot"""
            try:
                # Get session
                session = db.query(ChatbotSession).filter(
                    ChatbotSession.id == session_id
                ).first()
                
                if not session:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Session not found"
                    )
                
                # Process message flow
                result = self.message_service.process_message_flow(
                    session_id, content, message_type, db
                )
                
                return self.create_response({
                    "message": result["bot_message"].content,
                    "message_type": result["bot_message"].message_type,
                    "intent": result["intent"],
                    "entities": result["entities"],
                    "confidence": result["confidence"]
                }, "Message processed")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to process message")
        
        @self.router.get("/sessions/{session_id}/messages")
        async def get_conversation_history(
            session_id: str,
            limit: int = 50,
            offset: int = 0,
            db: Session = self.get_db_session()
        ):
            """Get conversation history"""
            try:
                messages = self.message_service.get_conversation_history(
                    session_id, limit, offset, db
                )
                
                return self.create_response(messages, "Conversation history retrieved")
                
            except Exception as e:
                raise self.handle_error(e, "Failed to retrieve conversation history")
