"""
Learning path API endpoints for MyWay Career Assessment System.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..middleware.auth import get_current_user
from ..models.user import User
from ..models.learning_path import LearningPath
from ..models.assessment_result import AssessmentResult
from ..services.learning_path_service import LearningPathService
from ..schemas import LearningPathResponse, LearningPathListResponse, LearningRecommendationsResponse

router = APIRouter(prefix="/api/v1/learning-paths", tags=["learning-paths"])


@router.get("/{assessment_result_id}", response_model=LearningPathListResponse)
async def get_learning_paths(
    assessment_result_id: str,
    career_name: Optional[str] = Query(None, description="Filter by career name"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get learning paths for an assessment result."""
    try:
        service = LearningPathService(db)
        learning_paths = await service.get_learning_paths(assessment_result_id, career_name)
        
        if not learning_paths:
            return LearningPathListResponse(
                success=True,
                message="No learning paths found",
                data=[]
            )
        
        # Convert to response format
        paths_data = []
        for path in learning_paths:
            path_data = {
                "id": str(path.id),
                "career_name": path.career_name,
                "skills": path.skills,
                "projects": path.projects,
                "habits": path.habits,
                "timeline_weeks": path.timeline_weeks,
                "priority": path.priority,
                "created_at": path.created_at.isoformat()
            }
            paths_data.append(path_data)
        
        return LearningPathListResponse(
            success=True,
            message="Learning paths retrieved successfully",
            data=paths_data
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving learning paths: {str(e)}"
        )


@router.post("/{assessment_result_id}/generate", response_model=LearningPathListResponse)
async def generate_learning_paths(
    assessment_result_id: str,
    target_careers: Optional[List[str]] = Query(None, description="Target career names"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate new learning paths for an assessment result."""
    try:
        service = LearningPathService(db)
        learning_paths = await service.generate_learning_paths(assessment_result_id, target_careers)
        
        if not learning_paths:
            return LearningPathListResponse(
                success=True,
                message="No learning paths could be generated",
                data=[]
            )
        
        # Convert to response format
        paths_data = []
        for path in learning_paths:
            path_data = {
                "id": str(path.id),
                "career_name": path.career_name,
                "skills": path.skills,
                "projects": path.projects,
                "habits": path.habits,
                "timeline_weeks": path.timeline_weeks,
                "priority": path.priority,
                "created_at": path.created_at.isoformat()
            }
            paths_data.append(path_data)
        
        return LearningPathListResponse(
            success=True,
            message=f"Generated {len(learning_paths)} learning paths successfully",
            data=paths_data
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating learning paths: {str(e)}"
        )


@router.get("/path/{path_id}", response_model=LearningPathResponse)
async def get_learning_path_by_id(
    path_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific learning path by ID."""
    try:
        service = LearningPathService(db)
        learning_path = await service.get_learning_path_by_id(path_id)
        
        if not learning_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Learning path not found"
            )
        
        path_data = {
            "id": str(learning_path.id),
            "career_name": learning_path.career_name,
            "skills": learning_path.skills,
            "projects": learning_path.projects,
            "habits": learning_path.habits,
            "timeline_weeks": learning_path.timeline_weeks,
            "priority": learning_path.priority,
            "created_at": learning_path.created_at.isoformat()
        }
        
        return LearningPathResponse(
            success=True,
            message="Learning path retrieved successfully",
            data=path_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving learning path: {str(e)}"
        )


@router.put("/path/{path_id}/progress", response_model=LearningPathResponse)
async def update_learning_path_progress(
    path_id: str,
    completed_skills: Optional[List[str]] = None,
    completed_projects: Optional[List[str]] = None,
    completed_habits: Optional[List[str]] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update progress on a learning path."""
    try:
        service = LearningPathService(db)
        learning_path = await service.update_learning_path_progress(
            path_id, completed_skills, completed_projects, completed_habits
        )
        
        if not learning_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Learning path not found"
            )
        
        path_data = {
            "id": str(learning_path.id),
            "career_name": learning_path.career_name,
            "skills": learning_path.skills,
            "projects": learning_path.projects,
            "habits": learning_path.habits,
            "timeline_weeks": learning_path.timeline_weeks,
            "priority": learning_path.priority,
            "created_at": learning_path.created_at.isoformat()
        }
        
        return LearningPathResponse(
            success=True,
            message="Learning path progress updated successfully",
            data=path_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating learning path progress: {str(e)}"
        )


@router.get("/{assessment_result_id}/recommendations", response_model=LearningRecommendationsResponse)
async def get_learning_recommendations(
    assessment_result_id: str,
    skill_gaps: Optional[List[str]] = Query(None, description="Specific skill gaps to address"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized learning recommendations."""
    try:
        service = LearningPathService(db)
        recommendations = await service.get_learning_recommendations(assessment_result_id, skill_gaps)
        
        return LearningRecommendationsResponse(
            success=True,
            message="Learning recommendations retrieved successfully",
            data=recommendations
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving learning recommendations: {str(e)}"
        )


@router.get("/{assessment_result_id}/statistics", response_model=Dict[str, Any])
async def get_learning_path_statistics(
    assessment_result_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get statistics about learning paths for an assessment result."""
    try:
        service = LearningPathService(db)
        statistics = await service.get_learning_path_statistics(assessment_result_id)
        
        return {
            "success": True,
            "message": "Learning path statistics retrieved successfully",
            "data": statistics
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving learning path statistics: {str(e)}"
        )


@router.get("/careers/available", response_model=Dict[str, Any])
async def get_available_careers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of available careers for learning path generation."""
    try:
        # This would typically come from the career rules or a separate careers table
        # For now, return a static list
        available_careers = [
            "Software Engineer",
            "Data Scientist",
            "UX Designer",
            "Marketing Manager",
            "Financial Analyst",
            "Project Manager",
            "Content Creator",
            "Entrepreneur"
        ]
        
        return {
            "success": True,
            "message": "Available careers retrieved successfully",
            "data": {
                "careers": available_careers,
                "total_count": len(available_careers)
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving available careers: {str(e)}"
        )


@router.delete("/path/{path_id}", response_model=Dict[str, Any])
async def delete_learning_path(
    path_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a learning path."""
    try:
        service = LearningPathService(db)
        learning_path = await service.get_learning_path_by_id(path_id)
        
        if not learning_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Learning path not found"
            )
        
        # Delete the learning path
        await db.delete(learning_path)
        await db.commit()
        
        return {
            "success": True,
            "message": "Learning path deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting learning path: {str(e)}"
        )