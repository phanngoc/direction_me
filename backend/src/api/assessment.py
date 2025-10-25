"""
Assessment API endpoints for MyWay Career Assessment System.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.assessment_service import AssessmentService
from ..services.question_service import QuestionService
from ..middleware.auth import get_current_user
from ..models.user import User
from ..schemas import (
    Assessment as AssessmentSchema,
    CreateAssessmentRequest,
    Question as QuestionSchema,
    Answer as AnswerSchema,
    SubmitAnswersRequest
)

router = APIRouter()


@router.post("/", response_model=AssessmentSchema)
async def create_assessment(
    assessment_data: CreateAssessmentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new assessment."""
    assessment_service = AssessmentService(db)
    
    assessment = await assessment_service.create_assessment(
        user_id=str(current_user.id)
    )
    
    return AssessmentSchema.from_orm(assessment)


@router.get("/{assessment_id}", response_model=AssessmentSchema)
async def get_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get assessment details."""
    assessment_service = AssessmentService(db)
    
    assessment = await assessment_service.get_assessment(assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Check if user owns this assessment
    if str(assessment.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this assessment"
        )
    
    return AssessmentSchema.from_orm(assessment)


@router.get("/{assessment_id}/questions", response_model=List[QuestionSchema])
async def get_assessment_questions(
    assessment_id: str,
    category: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get questions for assessment."""
    assessment_service = AssessmentService(db)
    question_service = QuestionService(db)
    
    # Verify assessment exists and belongs to user
    assessment = await assessment_service.get_assessment(assessment_id)
    if not assessment or str(assessment.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Get questions
    questions = await question_service.get_questions(category=category)
    
    return [QuestionSchema.from_orm(q) for q in questions]


@router.post("/{assessment_id}/answers")
async def submit_answers(
    assessment_id: str,
    answers_data: SubmitAnswersRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit assessment answers."""
    assessment_service = AssessmentService(db)
    
    # Verify assessment exists and belongs to user
    assessment = await assessment_service.get_assessment(assessment_id)
    if not assessment or str(assessment.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Update assessment progress
    await assessment_service.update_assessment_progress(
        assessment_id=assessment_id,
        answered_questions=len(answers_data.answers)
    )
    
    return {"message": "Answers submitted successfully"}


@router.post("/{assessment_id}/complete")
async def complete_assessment(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Complete assessment and calculate results."""
    assessment_service = AssessmentService(db)
    
    # Verify assessment exists and belongs to user
    assessment = await assessment_service.get_assessment(assessment_id)
    if not assessment or str(assessment.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Complete assessment
    assessment = await assessment_service.complete_assessment(assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to complete assessment"
        )
    
    return {"message": "Assessment completed successfully"}