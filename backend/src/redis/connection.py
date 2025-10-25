import redis
import json
import time
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Create Redis connection
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class SessionManager:
    def __init__(self):
        self.redis = redis_client
    
    def create_session(self, session_id: str, user_id: str, data: Dict[str, Any], expire_seconds: int = 3600) -> bool:
        """Create a new session with data"""
        try:
            session_data = {
                "session_id": session_id,
                "user_id": user_id,
                "data": data,
                "created_at": str(int(time.time()))
            }
            self.redis.setex(f"session:{session_id}", expire_seconds, json.dumps(session_data))
            return True
        except Exception as e:
            print(f"Error creating session: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data by session ID"""
        try:
            session_data = self.redis.get(f"session:{session_id}")
            if session_data:
                return json.loads(session_data)
            return None
        except Exception as e:
            print(f"Error getting session: {e}")
            return None
    
    def update_session(self, session_id: str, data: Dict[str, Any], expire_seconds: int = 3600) -> bool:
        """Update session data"""
        try:
            existing_session = self.get_session(session_id)
            if existing_session:
                existing_session["data"].update(data)
                self.redis.setex(f"session:{session_id}", expire_seconds, json.dumps(existing_session))
                return True
            return False
        except Exception as e:
            print(f"Error updating session: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session"""
        try:
            self.redis.delete(f"session:{session_id}")
            return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def extend_session(self, session_id: str, expire_seconds: int = 3600) -> bool:
        """Extend session expiration time"""
        try:
            return self.redis.expire(f"session:{session_id}", expire_seconds)
        except Exception as e:
            print(f"Error extending session: {e}")
            return False

# Global session manager instance
session_manager = SessionManager()
