from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.connection import get_db
from middleware.auth import auth_middleware, get_current_user
from models.user import User
from typing import Optional, Any, Dict
import logging

logger = logging.getLogger(__name__)

class BaseAPI:
    def __init__(self, prefix: str, tags: list = None):
        self.router = APIRouter(prefix=prefix, tags=tags or [])
        self.setup_routes()
    
    def setup_routes(self):
        """Override in subclasses to setup specific routes"""
        pass
    
    def get_db_session(self) -> Session:
        """Get database session"""
        return Depends(get_db)
    
    def get_current_user_dependency(self) -> User:
        """Get current authenticated user"""
        return Depends(get_current_user)
    
    def get_optional_user_dependency(self) -> Optional[User]:
        """Get current user (optional)"""
        return Depends(auth_middleware.get_current_user_optional)
    
    def handle_error(self, error: Exception, message: str = "An error occurred") -> HTTPException:
        """Handle and log errors"""
        logger.error(f"API Error: {str(error)}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
    
    def validate_request_data(self, data: Dict[str, Any], required_fields: list) -> bool:
        """Validate request data has required fields"""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        return True
    
    def create_response(self, data: Any, message: str = "Success") -> Dict[str, Any]:
        """Create standardized API response"""
        return {
            "data": data,
            "message": message,
            "status": "success"
        }
