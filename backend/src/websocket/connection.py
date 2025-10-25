from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        # Store active connections by session_id
        self.active_connections: Dict[str, WebSocket] = {}
        # Store connection metadata
        self.connection_metadata: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str, user_id: str = None):
        """Accept WebSocket connection and store it"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        self.connection_metadata[session_id] = {
            "user_id": user_id,
            "connected_at": asyncio.get_event_loop().time(),
            "last_activity": asyncio.get_event_loop().time()
        }
        logger.info(f"WebSocket connected for session {session_id}")
    
    def disconnect(self, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in self.connection_metadata:
            del self.connection_metadata[session_id]
        logger.info(f"WebSocket disconnected for session {session_id}")
    
    async def send_personal_message(self, message: dict, session_id: str):
        """Send message to specific session"""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
                # Update last activity
                if session_id in self.connection_metadata:
                    self.connection_metadata[session_id]["last_activity"] = asyncio.get_event_loop().time()
            except Exception as e:
                logger.error(f"Error sending message to session {session_id}: {e}")
                # Remove broken connection
                self.disconnect(session_id)
    
    async def send_chatbot_message(self, session_id: str, content: str, message_type: str = "text"):
        """Send chatbot message via WebSocket"""
        message = {
            "type": "chatbot_message",
            "data": {
                "content": content,
                "message_type": message_type,
                "timestamp": asyncio.get_event_loop().time()
            }
        }
        await self.send_personal_message(message, session_id)
    
    async def send_assessment_redirect(self, session_id: str, assessment_url: str):
        """Send assessment redirect message"""
        message = {
            "type": "assessment_redirect",
            "data": {
                "url": assessment_url,
                "timestamp": asyncio.get_event_loop().time()
            }
        }
        await self.send_personal_message(message, session_id)
    
    async def send_results_ready(self, session_id: str, results_url: str):
        """Send results ready notification"""
        message = {
            "type": "results_ready",
            "data": {
                "url": results_url,
                "timestamp": asyncio.get_event_loop().time()
            }
        }
        await self.send_personal_message(message, session_id)
    
    async def handle_message(self, websocket: WebSocket, session_id: str, data: dict):
        """Handle incoming WebSocket message"""
        try:
            message_type = data.get("type")
            
            if message_type == "chatbot_message":
                # Handle chatbot message
                content = data.get("data", {}).get("content", "")
                await self.process_chatbot_message(session_id, content)
            
            elif message_type == "assessment_complete":
                # Handle assessment completion
                await self.handle_assessment_completion(session_id, data.get("data", {}))
            
            elif message_type == "ping":
                # Handle ping/pong
                await self.send_personal_message({"type": "pong"}, session_id)
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def process_chatbot_message(self, session_id: str, content: str):
        """Process chatbot message (placeholder for Rasa integration)"""
        # TODO: Integrate with Rasa chatbot
        # For now, send a simple response
        response = "Xin chào! Tôi có thể giúp bạn làm gì?"
        await self.send_chatbot_message(session_id, response)
    
    async def handle_assessment_completion(self, session_id: str, data: dict):
        """Handle assessment completion"""
        # TODO: Process assessment results and generate recommendations
        results_url = f"/results/{data.get('session_id', 'unknown')}"
        await self.send_results_ready(session_id, results_url)
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        return list(self.active_connections.keys())
    
    def is_session_active(self, session_id: str) -> bool:
        """Check if session is active"""
        return session_id in self.active_connections
    
    async def broadcast_to_all(self, message: dict):
        """Broadcast message to all active connections"""
        for session_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, session_id)

# Global WebSocket manager instance
websocket_manager = WebSocketManager()
