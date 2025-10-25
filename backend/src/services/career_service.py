"""
Career service for MyWay Career Assessment System.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..models.career_suggestion import CareerSuggestion
from ..models.career_rule import CareerRule
from ..models.assessment_result import AssessmentResult
from ..models.profile_vector import ProfileVector
from ..algorithms.career_mapping import CareerMappingAlgorithm
from ..algorithms.ikigai_calculation import IkigaiCalculationAlgorithm


class CareerService:
    """Service for career-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def generate_career_suggestions(self, assessment_result_id: str) -> List[CareerSuggestion]:
        """Generate career suggestions for an assessment result."""
        # Get assessment result with profile vector
        result = await self.db.execute(
            select(AssessmentResult)
            .where(AssessmentResult.id == assessment_result_id)
            .options(selectinload(AssessmentResult.profile_vector))
        )
        assessment_result = result.scalar_one_or_none()
        
        if not assessment_result or not assessment_result.profile_vector:
            return []
        
        # Get active career rules
        career_rules = await self.get_active_career_rules()
        
        # Calculate career fit scores
        career_suggestions_data = CareerMappingAlgorithm.calculate_career_fit_scores(
            assessment_result.profile_vector, career_rules
        )
        
        # Create CareerSuggestion records
        career_suggestions = []
        for rank, suggestion_data in enumerate(career_suggestions_data, 1):
            career_suggestion = CareerSuggestion(
                assessment_result_id=assessment_result_id,
                career_name=suggestion_data['career_name'],
                fit_score=suggestion_data['fit_score'],
                rank=rank,
                explanation=suggestion_data['explanation']
            )
            career_suggestions.append(career_suggestion)
        
        # Save to database
        for suggestion in career_suggestions:
            self.db.add(suggestion)
        
        await self.db.commit()
        
        # Refresh to get IDs
        for suggestion in career_suggestions:
            await self.db.refresh(suggestion)
        
        return career_suggestions
    
    async def get_career_suggestions(self, assessment_result_id: str) -> List[CareerSuggestion]:
        """Get career suggestions for an assessment result."""
        result = await self.db.execute(
            select(CareerSuggestion)
            .where(CareerSuggestion.assessment_result_id == assessment_result_id)
            .order_by(CareerSuggestion.rank)
        )
        return result.scalars().all()
    
    async def get_career_suggestion_by_id(self, suggestion_id: str) -> Optional[CareerSuggestion]:
        """Get a specific career suggestion by ID."""
        result = await self.db.execute(
            select(CareerSuggestion).where(CareerSuggestion.id == suggestion_id)
        )
        return result.scalar_one_or_none()
    
    async def get_active_career_rules(self) -> List[CareerRule]:
        """Get all active career rules."""
        result = await self.db.execute(
            select(CareerRule).where(CareerRule.is_active == True)
        )
        return result.scalars().all()
    
    async def get_career_rule_by_name(self, career_name: str) -> Optional[CareerRule]:
        """Get career rule by career name."""
        result = await self.db.execute(
            select(CareerRule).where(CareerRule.career_name == career_name)
        )
        return result.scalar_one_or_none()
    
    async def create_career_rule(self, career_name: str, weights: Dict[str, float], 
                                thresholds: Dict[str, float], bonus_keys: List[str] = None) -> CareerRule:
        """Create a new career rule."""
        career_rule = CareerRule(
            career_name=career_name,
            weights=weights,
            thresholds=thresholds,
            bonus_keys=bonus_keys or [],
            is_active=True
        )
        
        self.db.add(career_rule)
        await self.db.commit()
        await self.db.refresh(career_rule)
        
        return career_rule
    
    async def update_career_rule(self, career_name: str, **updates) -> Optional[CareerRule]:
        """Update an existing career rule."""
        career_rule = await self.get_career_rule_by_name(career_name)
        if not career_rule:
            return None
        
        # Update allowed fields
        allowed_fields = ['weights', 'thresholds', 'bonus_keys', 'is_active']
        for field, value in updates.items():
            if field in allowed_fields and hasattr(career_rule, field):
                setattr(career_rule, field, value)
        
        await self.db.commit()
        await self.db.refresh(career_rule)
        
        return career_rule
    
    async def delete_career_rule(self, career_name: str) -> bool:
        """Delete a career rule."""
        career_rule = await self.get_career_rule_by_name(career_name)
        if not career_rule:
            return False
        
        await self.db.delete(career_rule)
        await self.db.commit()
        
        return True
    
    async def get_career_requirements(self, career_name: str) -> Dict[str, Any]:
        """Get detailed requirements for a career."""
        return CareerMappingAlgorithm.get_career_requirements(career_name)
    
    async def get_career_analysis(self, assessment_result_id: str) -> Dict[str, Any]:
        """Get comprehensive career analysis including Ikigai scores."""
        # Get assessment result with profile vector
        result = await self.db.execute(
            select(AssessmentResult)
            .where(AssessmentResult.id == assessment_result_id)
            .options(selectinload(AssessmentResult.profile_vector))
        )
        assessment_result = result.scalar_one_or_none()
        
        if not assessment_result or not assessment_result.profile_vector:
            return {}
        
        # Calculate Ikigai scores
        ikigai_scores = IkigaiCalculationAlgorithm.calculate_ikigai_scores(
            assessment_result.profile_vector
        )
        
        # Get career suggestions
        career_suggestions = await self.get_career_suggestions(assessment_result_id)
        
        # Get Ikigai interpretation
        ikigai_interpretation = IkigaiCalculationAlgorithm.get_ikigai_interpretation(ikigai_scores)
        
        # Get development recommendations
        development_recommendations = IkigaiCalculationAlgorithm.get_development_recommendations(ikigai_scores)
        
        # Determine Ikigai quadrant
        ikigai_quadrant = IkigaiCalculationAlgorithm.get_ikigai_quadrant(
            ikigai_scores['ikigai_love'],
            ikigai_scores['ikigai_good_at'],
            ikigai_scores['ikigai_world_needs'],
            ikigai_scores['ikigai_paid_for']
        )
        
        return {
            'ikigai_scores': ikigai_scores,
            'ikigai_interpretation': ikigai_interpretation,
            'ikigai_quadrant': ikigai_quadrant,
            'development_recommendations': development_recommendations,
            'career_suggestions': [
                {
                    'id': suggestion.id,
                    'career_name': suggestion.career_name,
                    'fit_score': suggestion.fit_score,
                    'rank': suggestion.rank,
                    'explanation': suggestion.explanation
                }
                for suggestion in career_suggestions
            ]
        }
    
    async def get_career_comparison(self, career_names: List[str]) -> Dict[str, Any]:
        """Compare multiple careers."""
        comparison = {}
        
        for career_name in career_names:
            requirements = await self.get_career_requirements(career_name)
            comparison[career_name] = requirements
        
        return comparison
    
    async def search_careers(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search careers by name or description."""
        # Get all active career rules
        career_rules = await self.get_active_career_rules()
        
        # Filter by query
        matching_careers = []
        query_lower = query.lower()
        
        for rule in career_rules:
            if query_lower in rule.career_name.lower():
                requirements = await self.get_career_requirements(rule.career_name)
                matching_careers.append(requirements)
        
        return matching_careers[:limit]
    
    async def get_career_statistics(self) -> Dict[str, Any]:
        """Get career suggestion statistics."""
        # Count total suggestions
        result = await self.db.execute(
            select(CareerSuggestion)
        )
        all_suggestions = result.scalars().all()
        
        # Count by career name
        career_counts = {}
        total_suggestions = len(all_suggestions)
        
        for suggestion in all_suggestions:
            career_name = suggestion.career_name
            if career_name not in career_counts:
                career_counts[career_name] = 0
            career_counts[career_name] += 1
        
        # Calculate percentages
        career_percentages = {
            career: (count / total_suggestions * 100) if total_suggestions > 0 else 0
            for career, count in career_counts.items()
        }
        
        return {
            'total_suggestions': total_suggestions,
            'career_counts': career_counts,
            'career_percentages': career_percentages,
            'most_popular_career': max(career_counts.items(), key=lambda x: x[1])[0] if career_counts else None
        }