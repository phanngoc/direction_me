"""
Learning path generation algorithm for MyWay Career Assessment System.
"""
from typing import Dict, List, Any, Tuple
import json
import os
import random
from ..models.profile_vector import ProfileVector


class LearningPathGenerator:
    """Generates personalized learning paths based on profile vector and career goals."""
    
    def __init__(self):
        self.roadmap_library = self._load_roadmap_library()
    
    def generate_learning_path(
        self,
        profile_vector: ProfileVector,
        career_name: str
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning path for a specific career.
        
        Args:
            profile_vector: 16-dimensional profile vector
            career_name: Target career name
            
        Returns:
            Dictionary containing learning path data
        """
        if career_name not in self.roadmap_library['careers']:
            return self._generate_default_learning_path(career_name)
        
        career_data = self.roadmap_library['careers'][career_name]
        profile_scores = profile_vector.to_vector()
        
        # Analyze skill gaps
        skill_gaps = self._analyze_skill_gaps(profile_scores)
        
        # Generate personalized skills based on gaps and career requirements
        skills = self._generate_personalized_skills(career_data, skill_gaps, profile_scores)
        
        # Generate projects based on skills and difficulty level
        projects = self._generate_personalized_projects(career_data, skills, profile_scores)
        
        # Generate habits based on career requirements and profile
        habits = self._generate_personalized_habits(career_data, profile_scores)
        
        # Calculate timeline based on skill gaps and learning pace
        timeline_weeks = self._calculate_timeline(career_data, skill_gaps, profile_scores)
        
        # Determine priority based on fit and urgency
        priority = self._determine_priority(career_name, profile_scores)
        
        return {
            'skills': skills,
            'projects': projects,
            'habits': habits,
            'timeline_weeks': timeline_weeks,
            'priority': priority,
            'career_name': career_name,
            'skill_gaps': skill_gaps,
            'difficulty_level': self._assess_difficulty_level(profile_scores),
            'learning_style': self._determine_learning_style(profile_scores)
        }
    
    def generate_recommendations(
        self,
        profile_vector: ProfileVector,
        skill_gaps: List[str]
    ) -> Dict[str, Any]:
        """
        Generate learning recommendations based on skill gaps.
        
        Args:
            profile_vector: 16-dimensional profile vector
            skill_gaps: List of identified skill gaps
            
        Returns:
            Dictionary with learning recommendations
        """
        profile_scores = profile_vector.to_vector()
        
        # Categorize skill gaps
        technical_gaps = [gap for gap in skill_gaps if self._is_technical_skill(gap)]
        soft_skill_gaps = [gap for gap in skill_gaps if not self._is_technical_skill(gap)]
        
        # Generate recommendations for each category
        technical_recommendations = self._generate_technical_recommendations(technical_gaps)
        soft_skill_recommendations = self._generate_soft_skill_recommendations(soft_skill_gaps)
        
        # Generate learning resources
        learning_resources = self._generate_learning_resources(profile_scores, skill_gaps)
        
        # Generate practice exercises
        practice_exercises = self._generate_practice_exercises(skill_gaps)
        
        return {
            'technical_recommendations': technical_recommendations,
            'soft_skill_recommendations': soft_skill_recommendations,
            'learning_resources': learning_resources,
            'practice_exercises': practice_exercises,
            'priority_skills': skill_gaps[:5],
            'estimated_improvement_time': self._estimate_improvement_time(skill_gaps)
        }
    
    def _load_roadmap_library(self) -> Dict[str, Any]:
        """Load roadmap library from JSON file."""
        try:
            file_path = os.path.join(
                os.path.dirname(__file__),
                '..', '..', '..', 'data', 'roadmap_library.json'
            )
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)['roadmap_library']
        except FileNotFoundError:
            return self._get_default_roadmap_library()
    
    def _get_default_roadmap_library(self) -> Dict[str, Any]:
        """Get default roadmap library if file not found."""
        return {
            'careers': {
                'Software Engineer': {
                    'skills': {
                        'foundational': [
                            {'name': 'Programming Fundamentals', 'weeks': 4},
                            {'name': 'Version Control', 'weeks': 2}
                        ],
                        'frontend': [
                            {'name': 'HTML/CSS/JavaScript', 'weeks': 6},
                            {'name': 'React Framework', 'weeks': 8}
                        ],
                        'backend': [
                            {'name': 'Node.js/Express', 'weeks': 6},
                            {'name': 'Database Management', 'weeks': 4}
                        ]
                    },
                    'habits': [
                        {'name': 'Daily Coding Practice', 'frequency': 'daily', 'duration_weeks': 24}
                    ]
                }
            }
        }
    
    def _analyze_skill_gaps(self, profile_scores: List[float]) -> List[str]:
        """Analyze skill gaps based on profile scores."""
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
        
        skill_gaps = []
        for i, score in enumerate(profile_scores):
            if i < len(ProfileVector.FACET_NAMES):
                facet_name = ProfileVector.FACET_NAMES[i]
                if score < 60 and facet_name in skill_mapping:
                    skill_gaps.append(skill_mapping[facet_name])
        
        return skill_gaps
    
    def _generate_personalized_skills(
        self,
        career_data: Dict[str, Any],
        skill_gaps: List[str],
        profile_scores: List[float]
    ) -> List[Dict[str, Any]]:
        """Generate personalized skills based on career requirements and gaps."""
        skills = []
        
        # Get career skill requirements
        career_skills = career_data.get('skills', {})
        
        # Add foundational skills first
        foundational_skills = career_skills.get('foundational', [])
        for skill in foundational_skills:
            skills.append({
                'name': skill['name'],
                'description': skill.get('description', ''),
                'weeks': skill['weeks'],
                'priority': 'high',
                'category': 'foundational',
                'resources': skill.get('resources', []),
                'projects': skill.get('projects', [])
            })
        
        # Add specialized skills based on profile strengths
        for category, category_skills in career_skills.items():
            if category == 'foundational':
                continue
            
            for skill in category_skills:
                # Determine priority based on profile scores
                priority = self._determine_skill_priority(skill, profile_scores)
                
                skills.append({
                    'name': skill['name'],
                    'description': skill.get('description', ''),
                    'weeks': skill['weeks'],
                    'priority': priority,
                    'category': category,
                    'resources': skill.get('resources', []),
                    'projects': skill.get('projects', [])
                })
        
        # Sort by priority and weeks
        skills.sort(key=lambda x: (x['priority'] == 'high', -x['weeks']))
        
        return skills
    
    def _generate_personalized_projects(
        self,
        career_data: Dict[str, Any],
        skills: List[Dict[str, Any]],
        profile_scores: List[float]
    ) -> List[Dict[str, Any]]:
        """Generate personalized projects based on skills and profile."""
        projects = []
        
        # Get project templates
        project_templates = self.roadmap_library.get('project_templates', {})
        
        # Select projects based on difficulty level
        difficulty_level = self._assess_difficulty_level(profile_scores)
        template_category = self._get_difficulty_category(difficulty_level)
        
        if template_category in project_templates:
            for template in project_templates[template_category]:
                projects.append({
                    'name': template['name'],
                    'description': template['description'],
                    'skills_required': template['skills'],
                    'duration_weeks': template['duration_weeks'],
                    'difficulty': template_category,
                    'priority': 'medium'
                })
        
        # Add skill-specific projects
        for skill in skills[:5]:  # Top 5 skills
            if skill.get('projects'):
                for project_name in skill['projects']:
                    projects.append({
                        'name': project_name,
                        'description': f"Practice project for {skill['name']}",
                        'skills_required': [skill['name']],
                        'duration_weeks': max(1, skill['weeks'] // 2),
                        'difficulty': skill['category'],
                        'priority': 'high'
                    })
        
        return projects[:8]  # Limit to 8 projects
    
    def _generate_personalized_habits(
        self,
        career_data: Dict[str, Any],
        profile_scores: List[float]
    ) -> List[Dict[str, Any]]:
        """Generate personalized habits based on career requirements and profile."""
        habits = []
        
        # Get career-specific habits
        career_habits = career_data.get('habits', [])
        for habit in career_habits:
            habits.append({
                'name': habit['name'],
                'description': habit['description'],
                'frequency': habit['frequency'],
                'duration_weeks': habit['duration_weeks'],
                'priority': 'high'
            })
        
        # Add profile-based habits
        profile_habits = self._generate_profile_based_habits(profile_scores)
        habits.extend(profile_habits)
        
        return habits[:6]  # Limit to 6 habits
    
    def _generate_profile_based_habits(self, profile_scores: List[float]) -> List[Dict[str, Any]]:
        """Generate habits based on profile strengths and weaknesses."""
        habits = []
        
        # Check for low scores that need improvement
        if profile_scores[0] < 60:  # IQ Logical Reasoning
            habits.append({
                'name': 'Daily Problem Solving',
                'description': 'Solve one coding problem or puzzle daily',
                'frequency': 'daily',
                'duration_weeks': 12,
                'priority': 'high'
            })
        
        if profile_scores[4] < 60:  # EQ Empathy
            habits.append({
                'name': 'Active Listening Practice',
                'description': 'Practice active listening in conversations',
                'frequency': 'daily',
                'duration_weeks': 8,
                'priority': 'medium'
            })
        
        if profile_scores[8] < 60:  # DQ Information Literacy
            habits.append({
                'name': 'Information Verification',
                'description': 'Verify information from multiple sources before sharing',
                'frequency': 'daily',
                'duration_weeks': 6,
                'priority': 'medium'
            })
        
        if profile_scores[12] < 60:  # AQ Control
            habits.append({
                'name': 'Leadership Opportunities',
                'description': 'Take on leadership roles in group projects',
                'frequency': 'weekly',
                'duration_weeks': 10,
                'priority': 'high'
            })
        
        return habits
    
    def _calculate_timeline(
        self,
        career_data: Dict[str, Any],
        skill_gaps: List[str],
        profile_scores: List[float]
    ) -> int:
        """Calculate learning timeline based on career requirements and profile."""
        base_timeline = career_data.get('timeline_weeks', 20)
        
        # Adjust based on skill gaps
        gap_adjustment = len(skill_gaps) * 2
        
        # Adjust based on learning pace (AQ Endurance)
        learning_pace = profile_scores[15] if len(profile_scores) > 15 else 50
        pace_adjustment = int((100 - learning_pace) / 10)
        
        # Adjust based on overall profile strength
        avg_score = sum(profile_scores) / len(profile_scores)
        strength_adjustment = int((100 - avg_score) / 20)
        
        total_timeline = base_timeline + gap_adjustment + pace_adjustment + strength_adjustment
        
        return max(8, min(52, total_timeline))  # Between 8 and 52 weeks
    
    def _determine_priority(self, career_name: str, profile_scores: List[float]) -> str:
        """Determine learning path priority based on profile and career."""
        avg_score = sum(profile_scores) / len(profile_scores)
        
        if avg_score >= 80:
            return 'high'
        elif avg_score >= 60:
            return 'medium'
        else:
            return 'low'
    
    def _assess_difficulty_level(self, profile_scores: List[float]) -> str:
        """Assess overall difficulty level based on profile scores."""
        avg_score = sum(profile_scores) / len(profile_scores)
        
        if avg_score >= 75:
            return 'advanced'
        elif avg_score >= 50:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _determine_learning_style(self, profile_scores: List[float]) -> str:
        """Determine learning style based on profile scores."""
        # Analyze different aspects
        visual_score = (profile_scores[2] + profile_scores[3]) / 2  # Verbal + Spatial
        analytical_score = (profile_scores[0] + profile_scores[1]) / 2  # Logical + Numerical
        social_score = (profile_scores[4] + profile_scores[5]) / 2  # Empathy + Social
        
        if visual_score > analytical_score and visual_score > social_score:
            return 'visual'
        elif analytical_score > social_score:
            return 'analytical'
        else:
            return 'social'
    
    def _determine_skill_priority(self, skill: Dict[str, Any], profile_scores: List[float]) -> str:
        """Determine priority for a specific skill based on profile."""
        # This is a simplified version - in practice, you'd have more sophisticated logic
        skill_name = skill['name'].lower()
        
        if any(keyword in skill_name for keyword in ['fundamental', 'basic', 'core']):
            return 'high'
        elif any(keyword in skill_name for keyword in ['advanced', 'expert', 'senior']):
            return 'low'
        else:
            return 'medium'
    
    def _get_difficulty_category(self, difficulty_level: str) -> str:
        """Get project template category based on difficulty level."""
        if difficulty_level == 'advanced':
            return 'advanced'
        elif difficulty_level == 'intermediate':
            return 'intermediate'
        else:
            return 'beginner'
    
    def _is_technical_skill(self, skill: str) -> bool:
        """Check if a skill is technical."""
        technical_keywords = [
            'programming', 'coding', 'development', 'technical',
            'software', 'database', 'algorithm', 'data',
            'machine learning', 'cloud', 'security'
        ]
        return any(keyword in skill.lower() for keyword in technical_keywords)
    
    def _generate_technical_recommendations(self, technical_gaps: List[str]) -> List[Dict[str, Any]]:
        """Generate technical skill recommendations."""
        recommendations = []
        
        for gap in technical_gaps:
            recommendations.append({
                'skill': gap,
                'recommendation': f"Focus on developing {gap} through hands-on practice",
                'resources': self._get_skill_resources(gap),
                'timeline_weeks': 4
            })
        
        return recommendations
    
    def _generate_soft_skill_recommendations(self, soft_skill_gaps: List[str]) -> List[Dict[str, Any]]:
        """Generate soft skill recommendations."""
        recommendations = []
        
        for gap in soft_skill_gaps:
            recommendations.append({
                'skill': gap,
                'recommendation': f"Practice {gap} in real-world situations",
                'resources': self._get_soft_skill_resources(gap),
                'timeline_weeks': 6
            })
        
        return recommendations
    
    def _generate_learning_resources(self, profile_scores: List[float], skill_gaps: List[str]) -> List[Dict[str, Any]]:
        """Generate learning resources based on profile and gaps."""
        resources = []
        
        # Get resources from roadmap library
        platform_resources = self.roadmap_library.get('learning_resources', {}).get('platforms', [])
        
        for platform in platform_resources[:3]:  # Top 3 platforms
            resources.append({
                'name': platform['name'],
                'description': platform['description'],
                'focus': platform['focus'],
                'cost': platform['cost'],
                'recommended_for': skill_gaps[:2]  # Top 2 skill gaps
            })
        
        return resources
    
    def _generate_practice_exercises(self, skill_gaps: List[str]) -> List[Dict[str, Any]]:
        """Generate practice exercises for skill gaps."""
        exercises = []
        
        for gap in skill_gaps[:5]:  # Top 5 gaps
            exercises.append({
                'skill': gap,
                'exercise': f"Daily practice exercise for {gap}",
                'frequency': 'daily',
                'duration_minutes': 30
            })
        
        return exercises
    
    def _estimate_improvement_time(self, skill_gaps: List[str]) -> Dict[str, Any]:
        """Estimate time needed to improve skill gaps."""
        base_weeks_per_skill = 4
        total_weeks = len(skill_gaps) * base_weeks_per_skill
        
        return {
            'total_weeks': total_weeks,
            'estimated_months': round(total_weeks / 4, 1),
            'intensive_weeks': max(1, total_weeks // 2),
            'casual_weeks': total_weeks
        }
    
    def _get_skill_resources(self, skill: str) -> List[str]:
        """Get resources for a specific technical skill."""
        resource_mapping = {
            'programming': ['Codecademy', 'freeCodeCamp', 'LeetCode'],
            'data analysis': ['Kaggle', 'Coursera Data Science', 'Python for Data Science'],
            'web development': ['MDN Web Docs', 'React Documentation', 'Node.js Guide'],
            'machine learning': ['Fast.ai', 'Andrew Ng Course', 'Scikit-learn Tutorials']
        }
        
        skill_lower = skill.lower()
        for key, resources in resource_mapping.items():
            if key in skill_lower:
                return resources
        
        return ['General online courses', 'Documentation', 'Practice projects']
    
    def _get_soft_skill_resources(self, skill: str) -> List[str]:
        """Get resources for a specific soft skill."""
        return [
            'Books on leadership and communication',
            'Online courses on emotional intelligence',
            'Practice with mentors or coaches',
            'Join professional groups and communities'
        ]
    
    def _generate_default_learning_path(self, career_name: str) -> Dict[str, Any]:
        """Generate a default learning path for unknown careers."""
        return {
            'skills': [
                {
                    'name': 'Industry Research',
                    'description': f'Research {career_name} industry requirements',
                    'weeks': 2,
                    'priority': 'high',
                    'category': 'foundational',
                    'resources': ['Industry reports', 'Job postings', 'Professional networks'],
                    'projects': ['Industry analysis report']
                }
            ],
            'projects': [
                {
                    'name': f'{career_name} Portfolio Project',
                    'description': f'Create a portfolio project related to {career_name}',
                    'skills_required': ['Industry Research'],
                    'duration_weeks': 4,
                    'difficulty': 'intermediate',
                    'priority': 'high'
                }
            ],
            'habits': [
                {
                    'name': 'Industry Learning',
                    'description': f'Learn about {career_name} daily',
                    'frequency': 'daily',
                    'duration_weeks': 12,
                    'priority': 'high'
                }
            ],
            'timeline_weeks': 12,
            'priority': 'medium',
            'career_name': career_name,
            'skill_gaps': ['Industry Knowledge'],
            'difficulty_level': 'intermediate',
            'learning_style': 'analytical'
        }