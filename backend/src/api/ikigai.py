"""
Ikigai API endpoints for MyWay Career Assessment System.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..models.assessment_result import AssessmentResult
from ..services.career_service import CareerService
from ..algorithms.ikigai_calculation import IkigaiCalculationAlgorithm
from ..schemas import IkigaiResponse, CareerAnalysisResponse

router = APIRouter(prefix="/api/v1/ikigai", tags=["ikigai"])


@router.get("/analysis/{assessment_result_id}", response_model=CareerAnalysisResponse)
async def get_ikigai_analysis(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive Ikigai analysis for an assessment result."""
    try:
        career_service = CareerService(db)
        
        # Get career analysis including Ikigai scores
        analysis = await career_service.get_career_analysis(assessment_result_id)
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Assessment result not found or analysis not available"
            )
        
        return CareerAnalysisResponse(
            success=True,
            data=analysis,
            message="Ikigai analysis retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get Ikigai analysis: {str(e)}"
        )


@router.get("/scores/{assessment_result_id}", response_model=IkigaiResponse)
async def get_ikigai_scores(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get Ikigai scores for an assessment result."""
    try:
        # Get assessment result with profile vector
        result = await db.execute(
            select(AssessmentResult)
            .where(AssessmentResult.id == assessment_result_id)
            .options(selectinload(AssessmentResult.profile_vector))
        )
        assessment_result = result.scalar_one_or_none()
        
        if not assessment_result or not assessment_result.profile_vector:
            raise HTTPException(
                status_code=404,
                detail="Assessment result not found or profile vector not available"
            )
        
        # Calculate Ikigai scores
        ikigai_scores = IkigaiCalculationAlgorithm.calculate_ikigai_scores(
            assessment_result.profile_vector
        )
        
        # Get interpretation
        interpretation = IkigaiCalculationAlgorithm.get_ikigai_interpretation(ikigai_scores)
        
        # Get development recommendations
        recommendations = IkigaiCalculationAlgorithm.get_development_recommendations(ikigai_scores)
        
        # Determine quadrant
        quadrant = IkigaiCalculationAlgorithm.get_ikigai_quadrant(
            ikigai_scores['ikigai_love'],
            ikigai_scores['ikigai_good_at'],
            ikigai_scores['ikigai_world_needs'],
            ikigai_scores['ikigai_paid_for']
        )
        
        return IkigaiResponse(
            success=True,
            data={
                "scores": ikigai_scores,
                "interpretation": interpretation,
                "quadrant": quadrant,
                "recommendations": recommendations
            },
            message="Ikigai scores calculated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate Ikigai scores: {str(e)}"
        )


@router.get("/quadrant/{assessment_result_id}")
async def get_ikigai_quadrant(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get Ikigai quadrant for an assessment result."""
    try:
        # Get assessment result with profile vector
        result = await db.execute(
            select(AssessmentResult)
            .where(AssessmentResult.id == assessment_result_id)
            .options(selectinload(AssessmentResult.profile_vector))
        )
        assessment_result = result.scalar_one_or_none()
        
        if not assessment_result or not assessment_result.profile_vector:
            raise HTTPException(
                status_code=404,
                detail="Assessment result not found or profile vector not available"
            )
        
        # Calculate Ikigai scores
        ikigai_scores = IkigaiCalculationAlgorithm.calculate_ikigai_scores(
            assessment_result.profile_vector
        )
        
        # Determine quadrant
        quadrant = IkigaiCalculationAlgorithm.get_ikigai_quadrant(
            ikigai_scores['ikigai_love'],
            ikigai_scores['ikigai_good_at'],
            ikigai_scores['ikigai_world_needs'],
            ikigai_scores['ikigai_paid_for']
        )
        
        return {
            "success": True,
            "data": {
                "quadrant": quadrant,
                "scores": {
                    "love": ikigai_scores['ikigai_love'],
                    "good_at": ikigai_scores['ikigai_good_at'],
                    "world_needs": ikigai_scores['ikigai_world_needs'],
                    "paid_for": ikigai_scores['ikigai_paid_for']
                }
            },
            "message": "Ikigai quadrant determined successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to determine Ikigai quadrant: {str(e)}"
        )


@router.get("/recommendations/{assessment_result_id}")
async def get_development_recommendations(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get development recommendations based on Ikigai analysis."""
    try:
        # Get assessment result with profile vector
        result = await db.execute(
            select(AssessmentResult)
            .where(AssessmentResult.id == assessment_result_id)
            .options(selectinload(AssessmentResult.profile_vector))
        )
        assessment_result = result.scalar_one_or_none()
        
        if not assessment_result or not assessment_result.profile_vector:
            raise HTTPException(
                status_code=404,
                detail="Assessment result not found or profile vector not available"
            )
        
        # Calculate Ikigai scores
        ikigai_scores = IkigaiCalculationAlgorithm.calculate_ikigai_scores(
            assessment_result.profile_vector
        )
        
        # Get development recommendations
        recommendations = IkigaiCalculationAlgorithm.get_development_recommendations(ikigai_scores)
        
        return {
            "success": True,
            "data": {
                "recommendations": recommendations,
                "scores": ikigai_scores
            },
            "message": "Development recommendations generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get("/interpretation/{assessment_result_id}")
async def get_ikigai_interpretation(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed Ikigai interpretation for an assessment result."""
    try:
        # Get assessment result with profile vector
        result = await db.execute(
            select(AssessmentResult)
            .where(AssessmentResult.id == assessment_result_id)
            .options(selectinload(AssessmentResult.profile_vector))
        )
        assessment_result = result.scalar_one_or_none()
        
        if not assessment_result or not assessment_result.profile_vector:
            raise HTTPException(
                status_code=404,
                detail="Assessment result not found or profile vector not available"
            )
        
        # Calculate Ikigai scores
        ikigai_scores = IkigaiCalculationAlgorithm.calculate_ikigai_scores(
            assessment_result.profile_vector
        )
        
        # Get interpretation
        interpretation = IkigaiCalculationAlgorithm.get_ikigai_interpretation(ikigai_scores)
        
        return {
            "success": True,
            "data": {
                "interpretation": interpretation,
                "scores": ikigai_scores
            },
            "message": "Ikigai interpretation generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate interpretation: {str(e)}"
        )