"""
Question service for MyWay Career Assessment System.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.question_bank import QuestionBank


class QuestionService:
    """Service for question operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_questions(self, category: Optional[str] = None) -> List[QuestionBank]:
        """Get questions, optionally filtered by category."""
        query = select(QuestionBank).where(QuestionBank.is_active == True)
        
        if category:
            query = query.where(QuestionBank.category == category)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_question_by_id(self, question_id: str) -> Optional[QuestionBank]:
        """Get question by ID."""
        result = await self.db.execute(
            select(QuestionBank).where(QuestionBank.id == question_id)
        )
        return result.scalar_one_or_none()
    
    async def create_question(self, **question_data) -> QuestionBank:
        """Create a new question."""
        question = QuestionBank(**question_data)
        self.db.add(question)
        await self.db.commit()
        await self.db.refresh(question)
        return question