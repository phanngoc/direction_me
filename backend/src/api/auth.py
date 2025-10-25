"""
Authentication API endpoints for MyWay Career Assessment System.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.user_service import UserService
from ..middleware.auth import create_access_token, get_current_user
from ..models.user import User
from ..schemas import CreateUserRequest, LoginRequest, AuthResponse, User as UserSchema

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register(
    user_data: CreateUserRequest,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    print(f"Register request: {user_data}")
    user_service = UserService(db)
    
    try:
        print("Creating user...")
        user = await user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            age=user_data.age
        )
        print(f"User created: {user.id}")
        
        # Create access token
        print("Creating access token...")
        access_token = create_access_token(data={"sub": str(user.id)})
        print("Access token created")
        
        print("Creating response...")
        response = AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserSchema.model_validate(user)
        )
        print("Response created successfully")
        return response
    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login user."""
    user_service = UserService(db)
    
    user = await user_service.authenticate_user(
        email=login_data.email,
        password=login_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserSchema.model_validate(user)
    )


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return UserSchema.model_validate(current_user)