"""
Learning Recommendations Engine
Generates personalized learning recommendations based on profile and goals
"""

from typing import Dict, List
import json


def generate_learning_recommendations(
    profile_vector: Dict[str, float],
    career_name: str,
    career_requirements: Dict[str, float],
    skill_gaps: List[Dict]
) -> Dict:
    """
    Generate personalized learning recommendations

    Args:
        profile_vector: User's 16-dimensional profile vector
        career_name: Target career name
        career_requirements: Required skill levels for the career
        skill_gaps: List of skill gaps from gap analysis

    Returns:
        Dictionary containing learning recommendations
    """
    # Categorize skills by domain
    iq_skills = []
    eq_skills = []
    dq_skills = []
    aq_skills = []

    for gap in skill_gaps:
        facet = gap['facet']
        if facet.startswith('iq_'):
            iq_skills.append(gap)
        elif facet.startswith('eq_'):
            eq_skills.append(gap)
        elif facet.startswith('dq_'):
            dq_skills.append(gap)
        elif facet.startswith('aq_'):
            aq_skills.append(gap)

    # Generate recommendations for each domain
    recommendations = {
        'iq_recommendations': generate_iq_recommendations(iq_skills),
        'eq_recommendations': generate_eq_recommendations(eq_skills),
        'dq_recommendations': generate_dq_recommendations(dq_skills),
        'aq_recommendations': generate_aq_recommendations(aq_skills)
    }

    # Generate projects based on career
    projects = generate_project_recommendations(career_name, profile_vector, skill_gaps)

    # Generate daily habits
    habits = generate_habit_recommendations(career_name, skill_gaps)

    # Generate timeline
    timeline = generate_learning_timeline(skill_gaps, projects)

    return {
        'career_name': career_name,
        'recommendations': recommendations,
        'projects': projects,
        'habits': habits,
        'timeline': timeline,
        'total_skills': len(skill_gaps),
        'estimated_weeks': timeline['total_weeks']
    }


def generate_iq_recommendations(iq_gaps: List[Dict]) -> List[Dict]:
    """Generate IQ-specific learning recommendations"""
    recommendations = []

    iq_resources = {
        'iq_lr': {
            'name': 'Logical Reasoning',
            'courses': ['Critical Thinking', 'Formal Logic', 'Programming Fundamentals'],
            'practice': ['Logic puzzles', 'Programming challenges', 'Chess'],
            'books': ['Thinking, Fast and Slow', 'The Art of Logic']
        },
        'iq_nr': {
            'name': 'Numerical Reasoning',
            'courses': ['Statistics', 'Data Analysis', 'Quantitative Methods'],
            'practice': ['Math problems', 'Data interpretation', 'Financial analysis'],
            'books': ['How to Lie with Statistics', 'Naked Statistics']
        },
        'iq_vr': {
            'name': 'Verbal Reasoning',
            'courses': ['Reading Comprehension', 'Rhetoric', 'Academic Writing'],
            'practice': ['Reading analysis', 'Debate practice', 'Essay writing'],
            'books': ['Elements of Style', 'On Writing Well']
        },
        'iq_sr': {
            'name': 'Spatial Reasoning',
            'courses': ['3D Modeling', 'Architecture', 'Engineering Drawing'],
            'practice': ['3D puzzles', 'CAD software', 'Map reading'],
            'books': ['Sketching User Experiences', 'Drawing on the Right Side of the Brain']
        }
    }

    for gap in iq_gaps:
        facet = gap['facet']
        if facet in iq_resources:
            resource = iq_resources[facet]
            recommendations.append({
                'skill': resource['name'],
                'priority': gap['priority'],
                'gap': gap['gap'],
                'courses': resource['courses'],
                'practice_activities': resource['practice'],
                'recommended_books': resource['books'],
                'duration_weeks': 8 + (2 if gap['priority'] == 'critical' else 0)
            })

    return recommendations


def generate_eq_recommendations(eq_gaps: List[Dict]) -> List[Dict]:
    """Generate EQ-specific learning recommendations"""
    recommendations = []

    eq_resources = {
        'eq_empathy': {
            'name': 'Empathy',
            'courses': ['Emotional Intelligence', 'Psychology', 'Communication Skills'],
            'practice': ['Active listening', 'Volunteer work', 'Peer counseling'],
            'books': ['Emotional Intelligence', 'Nonviolent Communication']
        },
        'eq_social': {
            'name': 'Social Skills',
            'courses': ['Public Speaking', 'Networking', 'Leadership'],
            'practice': ['Networking events', 'Toastmasters', 'Team sports'],
            'books': ['How to Win Friends and Influence People', 'Never Eat Alone']
        },
        'eq_self_awareness': {
            'name': 'Self-Awareness',
            'courses': ['Mindfulness', 'Self-Reflection', 'Personality Psychology'],
            'practice': ['Meditation', 'Journaling', 'Personality tests'],
            'books': ['Emotional Intelligence 2.0', 'The Power of Now']
        },
        'eq_self_regulation': {
            'name': 'Self-Regulation',
            'courses': ['Stress Management', 'Cognitive Behavioral Therapy', 'Habit Formation'],
            'practice': ['Meditation', 'Exercise', 'Time management'],
            'books': ['Atomic Habits', 'The Willpower Instinct']
        }
    }

    for gap in eq_gaps:
        facet = gap['facet']
        if facet in eq_resources:
            resource = eq_resources[facet]
            recommendations.append({
                'skill': resource['name'],
                'priority': gap['priority'],
                'gap': gap['gap'],
                'courses': resource['courses'],
                'practice_activities': resource['practice'],
                'recommended_books': resource['books'],
                'duration_weeks': 6 + (2 if gap['priority'] == 'critical' else 0)
            })

    return recommendations


def generate_dq_recommendations(dq_gaps: List[Dict]) -> List[Dict]:
    """Generate DQ-specific learning recommendations"""
    recommendations = []

    dq_resources = {
        'dq_info_literacy': {
            'name': 'Information Literacy',
            'courses': ['Research Methods', 'Critical Thinking', 'Fact-Checking'],
            'practice': ['Research projects', 'Fact-checking practice', 'Academic writing'],
            'books': ['The Filter Bubble', 'Factfulness']
        },
        'dq_creativity': {
            'name': 'Digital Creativity',
            'courses': ['Design Thinking', 'Digital Art', 'Content Creation'],
            'practice': ['Creative projects', 'Blogging', 'Video editing'],
            'books': ['Steal Like an Artist', 'The Creative Act']
        },
        'dq_safety': {
            'name': 'Digital Safety',
            'courses': ['Cybersecurity', 'Privacy Protection', 'Ethical Hacking'],
            'practice': ['Security audits', 'Privacy settings review', 'Password management'],
            'books': ['The Art of Invisibility', 'Data and Goliath']
        },
        'dq_collaboration': {
            'name': 'Digital Collaboration',
            'courses': ['Project Management', 'Remote Work', 'Agile Methods'],
            'practice': ['Team projects', 'Tool adoption', 'Virtual meetings'],
            'books': ['Remote', 'The Culture Code']
        }
    }

    for gap in dq_gaps:
        facet = gap['facet']
        if facet in dq_resources:
            resource = dq_resources[facet]
            recommendations.append({
                'skill': resource['name'],
                'priority': gap['priority'],
                'gap': gap['gap'],
                'courses': resource['courses'],
                'practice_activities': resource['practice'],
                'recommended_books': resource['books'],
                'duration_weeks': 6 + (2 if gap['priority'] == 'critical' else 0)
            })

    return recommendations


def generate_aq_recommendations(aq_gaps: List[Dict]) -> List[Dict]:
    """Generate AQ-specific learning recommendations"""
    recommendations = []

    aq_resources = {
        'aq_control': {
            'name': 'Control (AQ)',
            'courses': ['Stress Management', 'Problem Solving', 'Resilience Training'],
            'practice': ['Challenge exercises', 'Problem-solving drills', 'Stress tests'],
            'books': ['Grit', 'Mindset']
        },
        'aq_ownership': {
            'name': 'Ownership (AQ)',
            'courses': ['Leadership', 'Accountability', 'Entrepreneurship'],
            'practice': ['Lead projects', 'Take responsibility', 'Start initiatives'],
            'books': ['Extreme Ownership', 'The 7 Habits of Highly Effective People']
        },
        'aq_reach': {
            'name': 'Reach (AQ)',
            'courses': ['Systems Thinking', 'Strategic Planning', 'Big Picture Analysis'],
            'practice': ['Strategic games', 'Long-term planning', 'Scenario analysis'],
            'books': ['Thinking in Systems', 'The Fifth Discipline']
        },
        'aq_endurance': {
            'name': 'Endurance (AQ)',
            'courses': ['Grit Development', 'Long-term Project Management', 'Persistence Training'],
            'practice': ['Marathon training', 'Long-term commitments', 'Habit tracking'],
            'books': ['Grit', 'The Power of Habit']
        }
    }

    for gap in aq_gaps:
        facet = gap['facet']
        if facet in aq_resources:
            resource = aq_resources[facet]
            recommendations.append({
                'skill': resource['name'],
                'priority': gap['priority'],
                'gap': gap['gap'],
                'courses': resource['courses'],
                'practice_activities': resource['practice'],
                'recommended_books': resource['books'],
                'duration_weeks': 8 + (2 if gap['priority'] == 'critical' else 0)
            })

    return recommendations


def generate_project_recommendations(
    career_name: str,
    profile_vector: Dict[str, float],
    skill_gaps: List[Dict]
) -> List[Dict]:
    """Generate project recommendations based on career and skill gaps"""
    project_templates = {
        'Software Engineer': [
            {
                'name': 'Build a Personal Portfolio Website',
                'description': 'Create a responsive website showcasing your projects',
                'skills_practiced': ['Programming', 'Web Development', 'Design'],
                'duration_weeks': 4
            },
            {
                'name': 'Contribute to Open Source',
                'description': 'Find and contribute to an open-source project on GitHub',
                'skills_practiced': ['Collaboration', 'Version Control', 'Code Review'],
                'duration_weeks': 8
            },
            {
                'name': 'Build a Full-Stack Application',
                'description': 'Create a complete web application with frontend and backend',
                'skills_practiced': ['Full-Stack Development', 'Database Design', 'API Design'],
                'duration_weeks': 12
            }
        ],
        'Data Scientist': [
            {
                'name': 'Kaggle Competition',
                'description': 'Participate in a Kaggle data science competition',
                'skills_practiced': ['Data Analysis', 'Machine Learning', 'Python'],
                'duration_weeks': 6
            },
            {
                'name': 'Data Visualization Dashboard',
                'description': 'Build an interactive dashboard for a dataset',
                'skills_practiced': ['Data Visualization', 'Storytelling', 'Analytics'],
                'duration_weeks': 4
            },
            {
                'name': 'Predictive Model Project',
                'description': 'Build and deploy a machine learning model',
                'skills_practiced': ['ML Engineering', 'Model Deployment', 'Cloud Services'],
                'duration_weeks': 10
            }
        ]
    }

    # Default projects for any career
    default_projects = [
        {
            'name': 'Skill-Building Challenge',
            'description': 'Complete a 30-day challenge focused on your biggest skill gap',
            'skills_practiced': [gap['facet'] for gap in skill_gaps[:3]],
            'duration_weeks': 4
        },
        {
            'name': 'Capstone Project',
            'description': 'Apply all learned skills in a comprehensive project',
            'skills_practiced': [gap['facet'] for gap in skill_gaps],
            'duration_weeks': 8
        }
    ]

    return project_templates.get(career_name, default_projects)


def generate_habit_recommendations(
    career_name: str,
    skill_gaps: List[Dict]
) -> List[Dict]:
    """Generate daily/weekly habit recommendations"""
    habits = [
        {
            'name': 'Daily Learning',
            'description': 'Spend 30 minutes on focused learning every day',
            'frequency': 'daily',
            'duration_minutes': 30
        },
        {
            'name': 'Weekly Practice',
            'description': 'Complete hands-on practice exercises',
            'frequency': 'weekly',
            'duration_minutes': 120
        },
        {
            'name': 'Reflection & Planning',
            'description': 'Review progress and plan next week',
            'frequency': 'weekly',
            'duration_minutes': 30
        }
    ]

    # Add specific habits based on skill gaps
    if any(gap['facet'].startswith('eq_') for gap in skill_gaps):
        habits.append({
            'name': 'Mindfulness Practice',
            'description': 'Meditation or mindfulness exercise',
            'frequency': 'daily',
            'duration_minutes': 15
        })

    if any(gap['facet'].startswith('aq_') for gap in skill_gaps):
        habits.append({
            'name': 'Challenge Exercise',
            'description': 'Face a difficult task or problem',
            'frequency': 'weekly',
            'duration_minutes': 60
        })

    if any(gap['facet'].startswith('dq_') for gap in skill_gaps):
        habits.append({
            'name': 'Digital Creation',
            'description': 'Create and share digital content',
            'frequency': 'weekly',
            'duration_minutes': 90
        })

    return habits


def generate_learning_timeline(
    skill_gaps: List[Dict],
    projects: List[Dict]
) -> Dict:
    """Generate a structured learning timeline"""
    # Calculate total weeks needed
    skill_weeks = sum(gap.get('estimated_duration_weeks', 8) for gap in skill_gaps)
    project_weeks = sum(project.get('duration_weeks', 4) for project in projects)

    # Organize into phases
    phases = []

    # Phase 1: Foundation (first 25% of time)
    foundation_gaps = [g for g in skill_gaps if g['priority'] == 'critical']
    if foundation_gaps:
        phases.append({
            'phase': 'Foundation',
            'weeks': max(4, len(foundation_gaps) * 2),
            'focus': [g['facet'] for g in foundation_gaps]
        })

    # Phase 2: Core Skills (next 40% of time)
    core_gaps = [g for g in skill_gaps if g['priority'] == 'moderate']
    if core_gaps:
        phases.append({
            'phase': 'Core Skills Development',
            'weeks': max(6, len(core_gaps) * 2),
            'focus': [g['facet'] for g in core_gaps]
        })

    # Phase 3: Advanced & Projects (next 35% of time)
    advanced_gaps = [g for g in skill_gaps if g['priority'] == 'minor']
    phases.append({
        'phase': 'Advanced Skills & Projects',
        'weeks': max(8, project_weeks),
        'focus': [g['facet'] for g in advanced_gaps] + ['projects']
    })

    total_weeks = sum(phase['weeks'] for phase in phases)

    return {
        'phases': phases,
        'total_weeks': total_weeks,
        'estimated_months': round(total_weeks / 4, 1),
        'recommended_pace': 'Moderate' if total_weeks < 24 else 'Intensive'
    }


# CLI Interface
if __name__ == '__main__':
    import sys

    # Example usage
    example_profile = {
        'iq_lr': 75.0,
        'iq_nr': 70.0,
        'dq_creativity': 80.0,
        'aq_endurance': 65.0
    }

    example_gaps = [
        {'facet': 'iq_lr', 'priority': 'critical', 'gap': 15.0, 'estimated_duration_weeks': 8},
        {'facet': 'iq_nr', 'priority': 'moderate', 'gap': 10.0, 'estimated_duration_weeks': 6},
        {'facet': 'dq_creativity', 'priority': 'minor', 'gap': 5.0, 'estimated_duration_weeks': 4}
    ]

    example_requirements = {
        'iq_lr': 90.0,
        'iq_nr': 80.0,
        'dq_creativity': 85.0
    }

    result = generate_learning_recommendations(
        example_profile,
        'Software Engineer',
        example_requirements,
        example_gaps
    )

    print(json.dumps(result, indent=2))
