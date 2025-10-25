"""
Progress Tracking API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from src.services.progress_tracking_service import ProgressTrackingService
from src.algorithms.progress_comparison import compare_progress, calculate_growth_rate
from src.middleware.auth import get_current_user


router = APIRouter(prefix="/progress", tags=["progress"])


# Pydantic models
class ProgressRecord(BaseModel):
    """Progress tracking record model"""
    id: str
    user_id: str
    assessment_id: str
    previous_assessment_id: Optional[str]
    improvement_iq: Optional[float]
    improvement_eq: Optional[float]
    improvement_dq: Optional[float]
    improvement_aq: Optional[float]
    tracked_at: datetime


class ProgressComparison(BaseModel):
    """Progress comparison model"""
    assessment_1: dict
    assessment_2: dict
    improvements: dict
    improvement_percentages: dict
    time_between_assessments: int


class ProgressAnalytics(BaseModel):
    """Progress analytics model"""
    total_assessments: int
    trends: dict
    best_improvement: dict
    latest_scores: dict
    first_assessment_date: datetime
    latest_assessment_date: datetime


@router.get("/history", response_model=List[ProgressRecord])
async def get_progress_history(
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    service: ProgressTrackingService = Depends()
):
    """
    Get user's progress history

    Returns list of progress tracking records showing improvements over time
    """
    try:
        history = await service.get_user_progress_history(
            user_id=current_user['id'],
            limit=limit
        )

        return history

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve progress history: {str(e)}"
        )


@router.get("/compare/{assessment_id_1}/{assessment_id_2}", response_model=ProgressComparison)
async def compare_assessments(
    assessment_id_1: str,
    assessment_id_2: str,
    current_user: dict = Depends(get_current_user),
    service: ProgressTrackingService = Depends()
):
    """
    Compare two assessments

    Shows improvements and changes between two assessment results
    """
    try:
        comparison = await service.compare_assessments(
            assessment_id_1=assessment_id_1,
            assessment_id_2=assessment_id_2
        )

        return comparison

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compare assessments: {str(e)}"
        )


@router.get("/analytics", response_model=ProgressAnalytics)
async def get_progress_analytics(
    current_user: dict = Depends(get_current_user),
    service: ProgressTrackingService = Depends()
):
    """
    Get progress analytics

    Provides trends, best improvements, and overall analytics for user's progress
    """
    try:
        analytics = await service.get_progress_analytics(
            user_id=current_user['id']
        )

        if 'message' in analytics:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=analytics['message']
            )

        return analytics

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate analytics: {str(e)}"
        )


@router.post("/track/{assessment_id}")
async def create_progress_tracking(
    assessment_id: str,
    previous_assessment_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    service: ProgressTrackingService = Depends()
):
    """
    Create progress tracking record

    Automatically called after completing an assessment
    """
    try:
        record = await service.create_progress_record(
            user_id=current_user['id'],
            assessment_id=assessment_id,
            previous_assessment_id=previous_assessment_id
        )

        return record

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create progress record: {str(e)}"
        )


@router.get("/growth-rate")
async def get_growth_rate(
    current_user: dict = Depends(get_current_user),
    service: ProgressTrackingService = Depends()
):
    """
    Calculate growth rate over all assessments

    Shows how quickly the user is improving over time
    """
    try:
        history = await service.get_user_progress_history(
            user_id=current_user['id'],
            limit=100
        )

        if len(history) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Need at least 2 assessments to calculate growth rate"
            )

        growth = calculate_growth_rate(history)

        return growth

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate growth rate: {str(e)}"
        )


@router.get("/latest")
async def get_latest_progress(
    current_user: dict = Depends(get_current_user),
    service: ProgressTrackingService = Depends()
):
    """
    Get latest progress record

    Returns the most recent progress tracking record
    """
    try:
        history = await service.get_user_progress_history(
            user_id=current_user['id'],
            limit=1
        )

        if not history:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No progress records found"
            )

        return history[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve latest progress: {str(e)}"
        )
