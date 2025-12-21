"""
Authentication middleware for MyWay Career Assessment System.
"""
import os
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models.user import User
from ..utils.bcrypt_compat import (
    BCRYPT_MAX_BYTES,
    validate_password_length,
    get_password_hash,
    verify_password,
)

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

# HTTP Bearer token
security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user


class AuthMiddleware:
    """Authentication middleware class."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Skip OPTIONS requests (CORS preflight)
            method = scope.get("method", "")
            if method == "OPTIONS":
                await self.app(scope, receive, send)
                return
            
            # Skip auth for certain paths
            path = scope["path"]
            if path in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
                await self.app(scope, receive, send)
                return
            
            # Check for authorization header
            headers = dict(scope["headers"])
            auth_header = headers.get(b"authorization")
            
            if not auth_header:
                # Let FastAPI handle the authentication
                await self.app(scope, receive, send)
                return
        
        await self.app(scope, receive, send)