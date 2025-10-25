from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from models.chatbot_message import ChatbotMessage
from models.chatbot_session import ChatbotSession
from services.session import SessionService
import requests
import json
import os
from datetime import datetime

class ChatbotMessageService:
    def __init__(self):
        self.session_service = SessionService()
        self.rasa_server_url = os.getenv("RASA_SERVER_URL", "http://localhost:5005")
    
    def process_user_message(self, session_id: str, content: str, message_type: str, db: Session) -> ChatbotMessage:
        """Process user message and create message record"""
        try:
            # Create user message
            user_message = ChatbotMessage(
                session_id=session_id,
                sender="user",
                message_type=message_type,
                content=content,
                intent=None,  # Will be filled by Rasa
                entities=None,
                confidence=None
            )
            
            db.add(user_message)
            db.commit()
            db.refresh(user_message)
            
            return user_message
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to process user message: {str(e)}")
    
    def get_rasa_response(self, message: str, session_id: str) -> Dict[str, Any]:
        """Get response from Rasa server"""
        try:
            url = f"{self.rasa_server_url}/webhooks/rest/webhook"
            payload = {
                "sender": session_id,
                "message": message
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return data[0]  # Return first response
            else:
                return {
                    "text": "Xin lỗi, tôi không hiểu. Bạn có thể nói rõ hơn không?",
                    "intent": "fallback"
                }
                
        except requests.exceptions.RequestException as e:
            # Fallback response if Rasa is unavailable
            return {
                "text": "Xin chào! Tôi có thể giúp bạn làm gì?",
                "intent": "greeting"
            }
        except Exception as e:
            return {
                "text": "Xin lỗi, có lỗi xảy ra. Vui lòng thử lại.",
                "intent": "error"
            }
    
    def create_bot_response(self, session_id: str, rasa_response: Dict[str, Any], db: Session) -> ChatbotMessage:
        """Create bot response message"""
        try:
            bot_message = ChatbotMessage(
                session_id=session_id,
                sender="bot",
                message_type="text",
                content=rasa_response.get("text", "Xin chào!"),
                intent=rasa_response.get("intent"),
                entities=rasa_response.get("entities"),
                confidence=rasa_response.get("confidence")
            )
            
            db.add(bot_message)
            db.commit()
            db.refresh(bot_message)
            
            return bot_message
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create bot response: {str(e)}")
    
    def handle_assessment_redirect(self, session_id: str, db: Session) -> ChatbotMessage:
        """Handle assessment redirect message"""
        try:
            redirect_message = ChatbotMessage(
                session_id=session_id,
                sender="bot",
                message_type="assessment_redirect",
                content="Tuyệt vời! Tôi sẽ chuyển bạn đến trang đánh giá. Hãy làm bài đánh giá một cách cẩn thận để có kết quả chính xác nhất.",
                intent="assessment_redirect"
            )
            
            db.add(redirect_message)
            db.commit()
            db.refresh(redirect_message)
            
            return redirect_message
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create assessment redirect message: {str(e)}")
    
    def handle_results_ready(self, session_id: str, db: Session) -> ChatbotMessage:
        """Handle results ready message"""
        try:
            results_message = ChatbotMessage(
                session_id=session_id,
                sender="bot",
                message_type="results",
                content="Kết quả đánh giá của bạn đã sẵn sàng! Tôi sẽ hiển thị kết quả chi tiết với các biểu đồ và gợi ý nghề nghiệp phù hợp.",
                intent="results_ready"
            )
            
            db.add(results_message)
            db.commit()
            db.refresh(results_message)
            
            return results_message
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create results ready message: {str(e)}")
    
    def get_conversation_history(self, session_id: str, limit: int = 50, offset: int = 0, db: Session) -> List[ChatbotMessage]:
        """Get conversation history for session"""
        try:
            messages = db.query(ChatbotMessage).filter(
                ChatbotMessage.session_id == session_id
            ).order_by(ChatbotMessage.created_at.desc()).offset(offset).limit(limit).all()
            
            return list(reversed(messages))  # Return in chronological order
            
        except Exception as e:
            raise Exception(f"Failed to get conversation history: {str(e)}")
    
    def process_message_flow(self, session_id: str, content: str, message_type: str, db: Session) -> Dict[str, Any]:
        """Complete message processing flow"""
        try:
            # Process user message
            user_message = self.process_user_message(session_id, content, message_type, db)
            
            # Get Rasa response
            rasa_response = self.get_rasa_response(content, session_id)
            
            # Create bot response
            bot_message = self.create_bot_response(session_id, rasa_response, db)
            
            # Update session context based on intent
            intent = rasa_response.get("intent")
            if intent == "start_assessment":
                # Mark session as ready for assessment
                session = db.query(ChatbotSession).filter(ChatbotSession.id == session_id).first()
                if session:
                    session.assessment_ready = True
                    db.commit()
            
            return {
                "user_message": user_message,
                "bot_message": bot_message,
                "intent": intent,
                "entities": rasa_response.get("entities"),
                "confidence": rasa_response.get("confidence")
            }
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to process message flow: {str(e)}")
