"""
Learning path service for MyWay Career Assessment System.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
import json
import os
from datetime import datetime, timedelta

from ..models.learning_path import LearningPath
from ..models.assessment_result import AssessmentResult
from ..models.career_suggestion import CareerSuggestion
from ..models.profile_vector import ProfileVector
from ..algorithms.learning_path_generator import LearningPathGenerator


class LearningPathService:
    """Service for managing personalized learning paths."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.generator = LearningPathGenerator()
    
    async def generate_learning_paths(
        self,
        assessment_result_id: str,
        target_careers: List[str] = None
    ) -> List[LearningPath]:
        """
        Generate personalized learning paths for target careers.
        
        Args:
            assessment_result_id: ID of the assessment result
            target_careers: List of target career names (if None, uses top career suggestions)
            
        Returns:
            List of generated learning paths
        """
        # Get assessment result with profile vector
        assessment_result = await self._get_assessment_result_with_profile(assessment_result_id)
        if not assessment_result:
            raise ValueError(f"Assessment result {assessment_result_id} not found")
        
        # Get target careers
        if not target_careers:
            target_careers = await self._get_top_career_suggestions(assessment_result_id)
        
        # Generate learning paths
        learning_paths = []
        for career_name in target_careers:
            learning_path = await self._generate_single_learning_path(
                assessment_result, career_name
            )
            if learning_path:
                learning_paths.append(learning_path)
        
        return learning_paths
    
    async def get_learning_paths(
        self,
        assessment_result_id: str,
        career_name: str = None
    ) -> List[LearningPath]:
        """
        Get existing learning paths for an assessment result.
        
        Args:
            assessment_result_id: ID of the assessment result
            career_name: Optional career name filter
            
        Returns:
            List of learning paths
        """
        query = select(LearningPath).where(
            LearningPath.assessment_result_id == assessment_result_id
        )
        
        if career_name:
            query = query.where(LearningPath.career_name == career_name)
        
        query = query.order_by(LearningPath.priority.desc(), LearningPath.created_at.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_learning_path_by_id(self, path_id: str) -> Optional[LearningPath]:
        """
        Get a specific learning path by ID.
        
        Args:
            path_id: ID of the learning path
            
        Returns:
            Learning path if found, None otherwise
        """
        query = select(LearningPath).where(LearningPath.id == path_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_learning_path_progress(
        self,
        path_id: str,
        completed_skills: List[str] = None,
        completed_projects: List[str] = None,
        completed_habits: List[str] = None
    ) -> Optional[LearningPath]:
        """
        Update progress on a learning path.
        
        Args:
            path_id: ID of the learning path
            completed_skills: List of completed skills
            completed_projects: List of completed projects
            completed_habits: List of completed habits
            
        Returns:
            Updated learning path if found, None otherwise
        """
        learning_path = await self.get_learning_path_by_id(path_id)
        if not learning_path:
            return None
        
        # Update progress (this would typically involve updating a progress tracking table)
        # For now, we'll just return the learning path
        return learning_path
    
    async def get_learning_recommendations(
        self,
        assessment_result_id: str,
        skill_gaps: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get personalized learning recommendations.
        
        Args:
            assessment_result_id: ID of the assessment result
            skill_gaps: Optional list of specific skill gaps to address
            
        Returns:
            Dictionary with learning recommendations
        """
        assessment_result = await self._get_assessment_result_with_profile(assessment_result_id)
        if not assessment_result:
            raise ValueError(f"Assessment result {assessment_result_id} not found")
        
        # Get skill gaps if not provided
        if not skill_gaps:
            skill_gaps = await self._analyze_skill_gaps(assessment_result)
        
        # Generate recommendations
        recommendations = self.generator.generate_recommendations(
            assessment_result.profile_vector, skill_gaps
        )
        
        return {
            'skill_gaps': skill_gaps,
            'recommendations': recommendations,
            'priority_skills': skill_gaps[:5],  # Top 5 priority skills
            'estimated_timeline': self._estimate_learning_timeline(skill_gaps)
        }
    
    async def _get_assessment_result_with_profile(self, assessment_result_id: str) -> Optional[AssessmentResult]:
        """Get assessment result with profile vector."""
        query = select(AssessmentResult).options(
            selectinload(AssessmentResult.profile_vector)
        ).where(AssessmentResult.id == assessment_result_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def _get_top_career_suggestions(self, assessment_result_id: str) -> List[str]:
        """Get top career suggestions for an assessment result."""
        query = select(CareerSuggestion).where(
            and_(
                CareerSuggestion.assessment_result_id == assessment_result_id,
                CareerSuggestion.rank <= 3  # Top 3 careers
            )
        ).order_by(CareerSuggestion.rank)
        
        result = await self.db.execute(query)
        suggestions = result.scalars().all()
        
        return [suggestion.career_name for suggestion in suggestions]
    
    async def _generate_single_learning_path(
        self,
        assessment_result: AssessmentResult,
        career_name: str
    ) -> Optional[LearningPath]:
        """Generate a single learning path for a career."""
        try:
            # Generate learning path using the generator
            path_data = self.generator.generate_learning_path(
                assessment_result.profile_vector,
                career_name
            )
            
            # Create learning path record
            learning_path = LearningPath(
                assessment_result_id=assessment_result.id,
                career_name=career_name,
                skills=path_data['skills'],
                projects=path_data['projects'],
                habits=path_data['habits'],
                timeline_weeks=path_data['timeline_weeks'],
                priority=path_data['priority']
            )
            
            self.db.add(learning_path)
            await self.db.commit()
            await self.db.refresh(learning_path)
            
            return learning_path
            
        except Exception as e:
            print(f"Error generating learning path for {career_name}: {e}")
            return None
    
    async def _analyze_skill_gaps(self, assessment_result: AssessmentResult) -> List[str]:
        """Analyze skill gaps based on profile vector."""
        profile_scores = assessment_result.profile_vector.to_vector()
        skill_gaps = []
        
        # Define skill mapping based on profile facets
        skill_mapping = {
            'iq_lr': 'Logical Thinking',
            'iq_nr': 'Mathematical Skills',
            'iq_vr': 'Communication Skills',
            'iq_sr': 'Spatial Reasoning',
            'eq_empathy': 'Emotional Intelligence',
            'eq_social': 'Social Skills',
            'eq_self_awareness': 'Self-Awareness',
            'eq_self_regulation': 'Self-Management',
            'dq_info_literacy': 'Digital Literacy',
            'dq_creativity': 'Creative Thinking',
            'dq_safety': 'Cybersecurity Awareness',
            'dq_collaboration': 'Collaboration Skills',
            'aq_control': 'Leadership Skills',
            'aq_ownership': 'Responsibility',
            'aq_reach': 'Influence',
            'aq_endurance': 'Persistence'
        }
        
        # Identify skills that need improvement (score < 60)
        for i, score in enumerate(profile_scores):
            if i < len(ProfileVector.FACET_NAMES):
                facet_name = ProfileVector.FACET_NAMES[i]
                if score < 60 and facet_name in skill_mapping:
                    skill_gaps.append(skill_mapping[facet_name])
        
        return skill_gaps
    
    def _estimate_learning_timeline(self, skill_gaps: List[str]) -> Dict[str, Any]:
        """Estimate learning timeline based on skill gaps."""
        base_weeks_per_skill = 4
        total_weeks = len(skill_gaps) * base_weeks_per_skill
        
        return {
            'total_weeks': total_weeks,
            'estimated_months': round(total_weeks / 4, 1),
            'intensive_weeks': max(1, total_weeks // 2),
            'casual_weeks': total_weeks
        }
    
    async def get_learning_path_statistics(self, assessment_result_id: str) -> Dict[str, Any]:
        """Get statistics about learning paths for an assessment result."""
        learning_paths = await self.get_learning_paths(assessment_result_id)
        
        if not learning_paths:
            return {
                'total_paths': 0,
                'average_timeline': 0,
                'priority_distribution': {},
                'skill_coverage': []
            }
        
        # Calculate statistics
        total_paths = len(learning_paths)
        average_timeline = sum(path.timeline_weeks for path in learning_paths) / total_paths
        
        priority_distribution = {}
        for path in learning_paths:
            priority = path.priority
            priority_distribution[priority] = priority_distribution.get(priority, 0) + 1
        
        # Get unique skills across all paths
        all_skills = set()
        for path in learning_paths:
            all_skills.update(path.skills)
        
        return {
            'total_paths': total_paths,
            'average_timeline': round(average_timeline, 1),
            'priority_distribution': priority_distribution,
            'skill_coverage': list(all_skills),
            'career_names': [path.career_name for path in learning_paths]
        }