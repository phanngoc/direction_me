"""
Career rules management service for MyWay Career Assessment System.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
import json
import os
from datetime import datetime

from ..models.career_rule import CareerRule
from ..database import get_db


class CareerRuleService:
    """Service for managing career mapping rules."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_all_rules(self, active_only: bool = True) -> List[CareerRule]:
        """
        Get all career rules.
        
        Args:
            active_only: Whether to return only active rules
            
        Returns:
            List of career rules
        """
        query = select(CareerRule)
        
        if active_only:
            query = query.where(CareerRule.is_active == True)
        
        query = query.order_by(CareerRule.career_name)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_rule_by_name(self, career_name: str) -> Optional[CareerRule]:
        """
        Get career rule by name.
        
        Args:
            career_name: Name of the career
            
        Returns:
            Career rule if found, None otherwise
        """
        query = select(CareerRule).where(CareerRule.career_name == career_name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_rule(
        self,
        career_name: str,
        weights: Dict[str, float],
        thresholds: Dict[str, float],
        bonus_keys: List[str] = None,
        is_active: bool = True
    ) -> CareerRule:
        """
        Create a new career rule.
        
        Args:
            career_name: Name of the career
            weights: Weights for each facet
            thresholds: Minimum thresholds for each facet
            bonus_keys: Facets that get bonus points
            is_active: Whether the rule is active
            
        Returns:
            Created career rule
        """
        career_rule = CareerRule(
            career_name=career_name,
            weights=weights,
            thresholds=thresholds,
            bonus_keys=bonus_keys or [],
            is_active=is_active
        )
        
        self.db.add(career_rule)
        await self.db.commit()
        await self.db.refresh(career_rule)
        
        return career_rule
    
    async def update_rule(
        self,
        career_name: str,
        weights: Dict[str, float] = None,
        thresholds: Dict[str, float] = None,
        bonus_keys: List[str] = None,
        is_active: bool = None
    ) -> Optional[CareerRule]:
        """
        Update an existing career rule.
        
        Args:
            career_name: Name of the career
            weights: New weights for each facet
            thresholds: New minimum thresholds for each facet
            bonus_keys: New bonus keys
            is_active: New active status
            
        Returns:
            Updated career rule if found, None otherwise
        """
        query = select(CareerRule).where(CareerRule.career_name == career_name)
        result = await self.db.execute(query)
        career_rule = result.scalar_one_or_none()
        
        if not career_rule:
            return None
        
        # Update fields if provided
        if weights is not None:
            career_rule.weights = weights
        if thresholds is not None:
            career_rule.thresholds = thresholds
        if bonus_keys is not None:
            career_rule.bonus_keys = bonus_keys
        if is_active is not None:
            career_rule.is_active = is_active
        
        career_rule.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(career_rule)
        
        return career_rule
    
    async def delete_rule(self, career_name: str) -> bool:
        """
        Delete a career rule.
        
        Args:
            career_name: Name of the career
            
        Returns:
            True if deleted, False if not found
        """
        query = delete(CareerRule).where(CareerRule.career_name == career_name)
        result = await self.db.execute(query)
        
        if result.rowcount > 0:
            await self.db.commit()
            return True
        
        return False
    
    async def toggle_rule_status(self, career_name: str) -> Optional[CareerRule]:
        """
        Toggle active status of a career rule.
        
        Args:
            career_name: Name of the career
            
        Returns:
            Updated career rule if found, None otherwise
        """
        query = select(CareerRule).where(CareerRule.career_name == career_name)
        result = await self.db.execute(query)
        career_rule = result.scalar_one_or_none()
        
        if not career_rule:
            return None
        
        career_rule.is_active = not career_rule.is_active
        career_rule.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(career_rule)
        
        return career_rule
    
    async def load_rules_from_file(self, file_path: str) -> List[CareerRule]:
        """
        Load career rules from JSON file.
        
        Args:
            file_path: Path to JSON file containing rules
            
        Returns:
            List of loaded career rules
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Career rules file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        rules = data.get('career_rules', [])
        loaded_rules = []
        
        for rule_data in rules:
            # Check if rule already exists
            existing_rule = await self.get_rule_by_name(rule_data['career_name'])
            
            if existing_rule:
                # Update existing rule
                updated_rule = await self.update_rule(
                    career_name=rule_data['career_name'],
                    weights=rule_data['weights'],
                    thresholds=rule_data['thresholds'],
                    bonus_keys=rule_data.get('bonus_keys', []),
                    is_active=rule_data.get('is_active', True)
                )
                loaded_rules.append(updated_rule)
            else:
                # Create new rule
                new_rule = await self.create_rule(
                    career_name=rule_data['career_name'],
                    weights=rule_data['weights'],
                    thresholds=rule_data['thresholds'],
                    bonus_keys=rule_data.get('bonus_keys', []),
                    is_active=rule_data.get('is_active', True)
                )
                loaded_rules.append(new_rule)
        
        return loaded_rules
    
    async def export_rules_to_file(self, file_path: str) -> bool:
        """
        Export career rules to JSON file.
        
        Args:
            file_path: Path to save JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            rules = await self.get_all_rules(active_only=False)
            
            export_data = {
                'career_rules': [],
                'metadata': {
                    'exported_at': datetime.utcnow().isoformat(),
                    'total_rules': len(rules),
                    'active_rules': len([r for r in rules if r.is_active])
                }
            }
            
            for rule in rules:
                rule_data = {
                    'career_name': rule.career_name,
                    'weights': rule.weights,
                    'thresholds': rule.thresholds,
                    'bonus_keys': rule.bonus_keys,
                    'is_active': rule.is_active,
                    'created_at': rule.created_at.isoformat(),
                    'updated_at': rule.updated_at.isoformat()
                }
                export_data['career_rules'].append(rule_data)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting rules: {e}")
            return False
    
    async def get_rule_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about career rules.
        
        Returns:
            Dictionary with rule statistics
        """
        all_rules = await self.get_all_rules(active_only=False)
        active_rules = [r for r in all_rules if r.is_active]
        
        # Calculate average weights and thresholds
        if active_rules:
            all_weights = []
            all_thresholds = []
            
            for rule in active_rules:
                all_weights.extend(rule.weights.values())
                all_thresholds.extend(rule.thresholds.values())
            
            avg_weight = sum(all_weights) / len(all_weights)
            avg_threshold = sum(all_thresholds) / len(all_thresholds)
        else:
            avg_weight = 0
            avg_threshold = 0
        
        return {
            'total_rules': len(all_rules),
            'active_rules': len(active_rules),
            'inactive_rules': len(all_rules) - len(active_rules),
            'average_weight': round(avg_weight, 2),
            'average_threshold': round(avg_threshold, 2),
            'career_names': [rule.career_name for rule in active_rules]
        }