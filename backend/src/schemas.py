"""
Pydantic schemas for MyWay Career Assessment System.
"""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Annotated
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, BeforeValidator


# Helper to convert UUID to string
def uuid_to_str(v):
    if isinstance(v, UUID):
        return str(v)
    return v


# Type alias for UUID fields that auto-convert to string
UUIDStr = Annotated[str, BeforeValidator(uuid_to_str)]


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    age: int = Field(..., ge=16, le=25)


class UserCreate(UserBase):
    # Password validation based on CHARACTER count (8-50 chars)
    # bcrypt's 72-byte limit is handled internally by truncation
    password: str = Field(..., min_length=8, max_length=50)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Request/Response schemas for API
class CreateUserRequest(UserCreate):
    pass


class LoginRequest(UserLogin):
    pass


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: "User"


class User(UserBase):
    id: UUIDStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Assessment schemas
class AssessmentBase(BaseModel):
    user_id: UUIDStr


class AssessmentCreate(AssessmentBase):
    pass


class Assessment(AssessmentBase):
    id: UUIDStr
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    total_questions: int
    answered_questions: int

    class Config:
        from_attributes = True


# Question schemas
class QuestionBase(BaseModel):
    category: str
    facet: str
    question_text: str
    question_type: str
    difficulty_weight: Optional[float]
    reverse_score: bool


class Question(QuestionBase):
    id: UUIDStr
    options: Optional[List[str]]

    class Config:
        from_attributes = True


# Answer schemas
class Answer(BaseModel):
    question_id: UUIDStr
    answer_value: int
    answer_text: Optional[str]


class SubmitAnswersRequest(BaseModel):
    answers: List[Answer]


# Assessment Result schemas
class AssessmentResultBase(BaseModel):
    iq_score: Optional[float] = Field(None, ge=0, le=100)
    eq_score: Optional[float] = Field(None, ge=0, le=100)
    dq_score: Optional[float] = Field(None, ge=0, le=100)
    aq_score: Optional[float] = Field(None, ge=0, le=100)
    ikigai_love: Optional[float] = Field(None, ge=0, le=100)
    ikigai_good_at: Optional[float] = Field(None, ge=0, le=100)
    ikigai_world_needs: Optional[float] = Field(None, ge=0, le=100)
    ikigai_paid_for: Optional[float] = Field(None, ge=0, le=100)
    ikigai_harmonic: Optional[float] = Field(None, ge=0, le=100)
    ikigai_geometric: Optional[float] = Field(None, ge=0, le=100)


class AssessmentResult(AssessmentResultBase):
    id: UUIDStr
    assessment_id: UUIDStr
    calculated_at: datetime

    class Config:
        from_attributes = True


# Career schemas
class CareerSuggestionBase(BaseModel):
    career_name: str
    fit_score: float = Field(..., ge=0, le=100)
    rank: int = Field(..., ge=1, le=8)
    explanation: Optional[str]


class CareerSuggestion(CareerSuggestionBase):
    id: UUIDStr
    created_at: datetime

    class Config:
        from_attributes = True


# Learning Path schemas
class LearningPathBase(BaseModel):
    career_name: str
    skills: List[str]
    projects: List[str]
    habits: List[str]
    timeline_weeks: int = Field(..., gt=0)
    priority: str = Field(..., pattern="^(high|medium|low)$")


class LearningPath(LearningPathBase):
    id: UUIDStr
    created_at: datetime

    class Config:
        from_attributes = True


# Progress Tracking schemas
class ProgressTrackingBase(BaseModel):
    user_id: UUIDStr
    assessment_id: UUIDStr
    previous_assessment_id: Optional[UUIDStr] = None
    improvement_iq: Optional[float]
    improvement_eq: Optional[float]
    improvement_dq: Optional[float]
    improvement_aq: Optional[float]


class ProgressTracking(ProgressTrackingBase):
    id: UUIDStr
    tracked_at: datetime

    class Config:
        from_attributes = True


# Ikigai schemas
class IkigaiResponse(BaseModel):
    success: bool
    message: str
    data: dict


class CareerSuggestionResponse(BaseModel):
    success: bool
    message: str
    data: List[dict]


class CareerAnalysisResponse(BaseModel):
    success: bool
    message: str
    data: dict


# Learning Path schemas
class LearningPathResponse(BaseModel):
    success: bool
    message: str
    data: dict


class LearningPathListResponse(BaseModel):
    success: bool
    message: str
    data: List[dict]


class LearningRecommendationsResponse(BaseModel):
    success: bool
    message: str
    data: dict


# API Response schemas
class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[str] = None


# Assessment schemas
class CreateAssessmentRequest(BaseModel):
    user_id: UUIDStr
    assessment_type: str = Field(..., pattern="^(full|iq|eq|dq|aq)$")


class SubmitAnswersRequest(BaseModel):
    assessment_id: UUIDStr
    answers: List[Answer]


class Assessment(BaseModel):
    id: UUIDStr
    user_id: UUIDStr
    assessment_type: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Rebuild models to resolve forward references
AuthResponse.model_rebuild()