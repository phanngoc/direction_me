"""
Career suggestions API endpoints for MyWay Career Assessment System.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..services.career_service import CareerService
from ..schemas import CareerSuggestionResponse, CareerAnalysisResponse

router = APIRouter(prefix="/api/v1/careers", tags=["careers"])


@router.get("/suggestions/{assessment_result_id}", response_model=CareerSuggestionResponse)
async def get_career_suggestions(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get career suggestions for an assessment result."""
    try:
        career_service = CareerService(db)
        
        # Get career suggestions
        suggestions = await career_service.get_career_suggestions(assessment_result_id)
        
        if not suggestions:
            # Generate suggestions if they don't exist
            suggestions = await career_service.generate_career_suggestions(assessment_result_id)
        
        return CareerSuggestionResponse(
            success=True,
            data=[
                {
                    "id": str(suggestion.id),
                    "career_name": suggestion.career_name,
                    "fit_score": suggestion.fit_score,
                    "rank": suggestion.rank,
                    "explanation": suggestion.explanation
                }
                for suggestion in suggestions
            ],
            message="Career suggestions retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get career suggestions: {str(e)}"
        )


@router.post("/suggestions/{assessment_result_id}/generate")
async def generate_career_suggestions(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate new career suggestions for an assessment result."""
    try:
        career_service = CareerService(db)
        
        # Generate career suggestions
        suggestions = await career_service.generate_career_suggestions(assessment_result_id)
        
        return {
            "success": True,
            "data": {
                "suggestions_count": len(suggestions),
                "suggestions": [
                    {
                        "id": str(suggestion.id),
                        "career_name": suggestion.career_name,
                        "fit_score": suggestion.fit_score,
                        "rank": suggestion.rank
                    }
                    for suggestion in suggestions
                ]
            },
            "message": "Career suggestions generated successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate career suggestions: {str(e)}"
        )


@router.get("/suggestion/{suggestion_id}")
async def get_career_suggestion(
    suggestion_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific career suggestion by ID."""
    try:
        career_service = CareerService(db)
        
        suggestion = await career_service.get_career_suggestion_by_id(suggestion_id)
        
        if not suggestion:
            raise HTTPException(
                status_code=404,
                detail="Career suggestion not found"
            )
        
        return {
            "success": True,
            "data": {
                "id": str(suggestion.id),
                "career_name": suggestion.career_name,
                "fit_score": suggestion.fit_score,
                "rank": suggestion.rank,
                "explanation": suggestion.explanation,
                "created_at": suggestion.created_at.isoformat()
            },
            "message": "Career suggestion retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get career suggestion: {str(e)}"
        )


@router.get("/requirements/{career_name}")
async def get_career_requirements(
    career_name: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed requirements for a specific career."""
    try:
        career_service = CareerService(db)
        
        requirements = await career_service.get_career_requirements(career_name)
        
        if not requirements:
            raise HTTPException(
                status_code=404,
                detail="Career not found"
            )
        
        return {
            "success": True,
            "data": requirements,
            "message": "Career requirements retrieved successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get career requirements: {str(e)}"
        )


@router.get("/compare")
async def compare_careers(
    career_names: List[str] = Query(..., description="List of career names to compare"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Compare multiple careers side by side."""
    try:
        if len(career_names) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least 2 careers required for comparison"
            )
        
        if len(career_names) > 5:
            raise HTTPException(
                status_code=400,
                detail="Maximum 5 careers allowed for comparison"
            )
        
        career_service = CareerService(db)
        
        comparison = await career_service.get_career_comparison(career_names)
        
        return {
            "success": True,
            "data": comparison,
            "message": "Career comparison generated successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compare careers: {str(e)}"
        )


@router.get("/search")
async def search_careers(
    query: str = Query(..., description="Search query for career names"),
    limit: int = Query(10, ge=1, le=20, description="Maximum number of results"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search careers by name or description."""
    try:
        career_service = CareerService(db)
        
        results = await career_service.search_careers(query, limit)
        
        return {
            "success": True,
            "data": {
                "query": query,
                "results": results,
                "count": len(results)
            },
            "message": "Career search completed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search careers: {str(e)}"
        )


@router.get("/statistics")
async def get_career_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get career suggestion statistics."""
    try:
        career_service = CareerService(db)
        
        statistics = await career_service.get_career_statistics()
        
        return {
            "success": True,
            "data": statistics,
            "message": "Career statistics retrieved successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get career statistics: {str(e)}"
        )


@router.get("/analysis/{assessment_result_id}", response_model=CareerAnalysisResponse)
async def get_career_analysis(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive career analysis including Ikigai scores."""
    try:
        career_service = CareerService(db)
        
        analysis = await career_service.get_career_analysis(assessment_result_id)
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Assessment result not found or analysis not available"
            )
        
        return CareerAnalysisResponse(
            success=True,
            data=analysis,
            message="Career analysis retrieved successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get career analysis: {str(e)}"
        )