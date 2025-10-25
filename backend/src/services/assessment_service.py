"""
Assessment service for MyWay Career Assessment System.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..models.assessment import Assessment
from ..models.assessment_result import AssessmentResult
from ..models.user import User


class AssessmentService:
    """Service for assessment operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_assessment(self, user_id: str) -> Assessment:
        """Create a new assessment for user."""
        assessment = Assessment(
            user_id=user_id,
            status='in_progress',
            total_questions=0,
            answered_questions=0
        )
        
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        
        return assessment
    
    async def get_assessment(self, assessment_id: str) -> Optional[Assessment]:
        """Get assessment by ID."""
        result = await self.db.execute(
            select(Assessment)
            .where(Assessment.id == assessment_id)
            .options(selectinload(Assessment.user))
        )
        return result.scalar_one_or_none()
    
    async def get_user_assessments(self, user_id: str) -> List[Assessment]:
        """Get all assessments for a user."""
        result = await self.db.execute(
            select(Assessment)
            .where(Assessment.user_id == user_id)
            .order_by(Assessment.started_at.desc())
        )
        return result.scalars().all()
    
    async def update_assessment_progress(self, assessment_id: str, answered_questions: int) -> Optional[Assessment]:
        """Update assessment progress."""
        assessment = await self.get_assessment(assessment_id)
        if not assessment:
            return None
        
        assessment.answered_questions = answered_questions
        await self.db.commit()
        await self.db.refresh(assessment)
        
        return assessment
    
    async def complete_assessment(self, assessment_id: str) -> Optional[Assessment]:
        """Mark assessment as completed."""
        assessment = await self.get_assessment(assessment_id)
        if not assessment:
            return None
        
        assessment.status = 'completed'
        assessment.completed_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(assessment)
        
        return assessment
    
    async def abandon_assessment(self, assessment_id: str) -> Optional[Assessment]:
        """Mark assessment as abandoned."""
        assessment = await self.get_assessment(assessment_id)
        if not assessment:
            return None
        
        assessment.status = 'abandoned'
        assessment.completed_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(assessment)
        
        return assessment
    
    async def get_assessment_result(self, assessment_id: str) -> Optional[AssessmentResult]:
        """Get assessment result."""
        result = await self.db.execute(
            select(AssessmentResult)
            .where(AssessmentResult.assessment_id == assessment_id)
        )
        return result.scalar_one_or_none()
    
    async def create_assessment_result(self, assessment_id: str, **scores) -> AssessmentResult:
        """Create assessment result with calculated scores."""
        assessment_result = AssessmentResult(
            assessment_id=assessment_id,
            **scores
        )
        
        self.db.add(assessment_result)
        await self.db.commit()
        await self.db.refresh(assessment_result)
        
        return assessment_result