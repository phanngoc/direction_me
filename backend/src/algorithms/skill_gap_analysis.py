"""
Skill Gap Analysis Algorithm
Analyzes the gap between current profile and target career requirements
"""

from typing import Dict, List, Tuple
import json


def analyze_skill_gap(
    profile_vector: Dict[str, float],
    career_requirements: Dict[str, float],
    career_name: str
) -> Dict:
    """
    Analyze skill gaps between user profile and career requirements

    Args:
        profile_vector: User's 16-dimensional profile vector
        career_requirements: Target career's required skill levels
        career_name: Name of the target career

    Returns:
        Dictionary containing gap analysis results
    """
    gaps = {}
    priorities = []

    # Calculate gaps for each facet
    for facet, required_level in career_requirements.items():
        current_level = profile_vector.get(facet, 0.0)
        gap = max(0, required_level - current_level)

        if gap > 0:
            gaps[facet] = {
                'current': current_level,
                'required': required_level,
                'gap': gap,
                'percentage_gap': (gap / required_level) * 100 if required_level > 0 else 0
            }

    # Prioritize gaps by severity
    for facet, gap_info in sorted(gaps.items(), key=lambda x: x[1]['gap'], reverse=True):
        priority = categorize_gap_priority(gap_info['gap'])
        priorities.append({
            'facet': facet,
            'priority': priority,
            'current': gap_info['current'],
            'required': gap_info['required'],
            'gap': gap_info['gap']
        })

    # Generate recommendations
    recommendations = generate_skill_recommendations(priorities, career_name)

    # Calculate overall readiness score
    readiness_score = calculate_readiness_score(profile_vector, career_requirements)

    return {
        'career_name': career_name,
        'readiness_score': readiness_score,
        'skill_gaps': gaps,
        'prioritized_gaps': priorities,
        'recommendations': recommendations,
        'total_gaps': len(gaps),
        'critical_gaps': sum(1 for p in priorities if p['priority'] == 'critical'),
        'moderate_gaps': sum(1 for p in priorities if p['priority'] == 'moderate'),
        'minor_gaps': sum(1 for p in priorities if p['priority'] == 'minor')
    }


def categorize_gap_priority(gap: float) -> str:
    """Categorize gap severity into priority levels"""
    if gap >= 30:
        return 'critical'
    elif gap >= 15:
        return 'moderate'
    else:
        return 'minor'


def calculate_readiness_score(
    profile_vector: Dict[str, float],
    career_requirements: Dict[str, float]
) -> float:
    """
    Calculate overall readiness score (0-100)
    Based on how well the profile matches career requirements
    """
    if not career_requirements:
        return 0.0

    total_match = 0.0
    total_required = 0.0

    for facet, required_level in career_requirements.items():
        current_level = profile_vector.get(facet, 0.0)
        # Use min to avoid bonus points for exceeding requirements
        match_level = min(current_level, required_level)
        total_match += match_level
        total_required += required_level

    if total_required == 0:
        return 0.0

    readiness = (total_match / total_required) * 100
    return round(readiness, 2)


def generate_skill_recommendations(
    prioritized_gaps: List[Dict],
    career_name: str
) -> List[Dict]:
    """
    Generate actionable recommendations for closing skill gaps
    """
    recommendations = []

    # Skill development resources by facet
    skill_resources = {
        'iq_lr': {
            'name': 'Logical Reasoning',
            'resources': ['Logic puzzles', 'Programming challenges', 'Chess'],
            'duration_weeks': 8
        },
        'iq_nr': {
            'name': 'Numerical Reasoning',
            'resources': ['Math courses', 'Statistical analysis', 'Data analysis projects'],
            'duration_weeks': 10
        },
        'iq_vr': {
            'name': 'Verbal Reasoning',
            'resources': ['Reading comprehension', 'Debate clubs', 'Writing practice'],
            'duration_weeks': 8
        },
        'iq_sr': {
            'name': 'Spatial Reasoning',
            'resources': ['3D modeling', 'Architecture courses', 'Engineering drawing'],
            'duration_weeks': 12
        },
        'eq_empathy': {
            'name': 'Empathy',
            'resources': ['Active listening workshops', 'Volunteer work', 'Psychology courses'],
            'duration_weeks': 6
        },
        'eq_social': {
            'name': 'Social Skills',
            'resources': ['Networking events', 'Public speaking', 'Team sports'],
            'duration_weeks': 8
        },
        'eq_self_awareness': {
            'name': 'Self-Awareness',
            'resources': ['Meditation', 'Journaling', 'Therapy/counseling'],
            'duration_weeks': 12
        },
        'eq_self_regulation': {
            'name': 'Self-Regulation',
            'resources': ['Stress management', 'Mindfulness', 'Cognitive behavioral therapy'],
            'duration_weeks': 10
        },
        'dq_info_literacy': {
            'name': 'Information Literacy',
            'resources': ['Research methods', 'Critical thinking courses', 'Fact-checking practice'],
            'duration_weeks': 6
        },
        'dq_creativity': {
            'name': 'Digital Creativity',
            'resources': ['Design thinking', 'Digital art', 'Content creation'],
            'duration_weeks': 8
        },
        'dq_safety': {
            'name': 'Digital Safety',
            'resources': ['Cybersecurity courses', 'Privacy workshops', 'Security certifications'],
            'duration_weeks': 6
        },
        'dq_collaboration': {
            'name': 'Digital Collaboration',
            'resources': ['Project management tools', 'Remote work training', 'Agile methodologies'],
            'duration_weeks': 4
        },
        'aq_control': {
            'name': 'Control (AQ)',
            'resources': ['Stress management', 'Problem-solving workshops', 'Resilience training'],
            'duration_weeks': 8
        },
        'aq_ownership': {
            'name': 'Ownership (AQ)',
            'resources': ['Leadership courses', 'Accountability training', 'Entrepreneurship'],
            'duration_weeks': 10
        },
        'aq_reach': {
            'name': 'Reach (AQ)',
            'resources': ['Systems thinking', 'Strategic planning', 'Big-picture analysis'],
            'duration_weeks': 8
        },
        'aq_endurance': {
            'name': 'Endurance (AQ)',
            'resources': ['Marathon training', 'Long-term project commitment', 'Grit building'],
            'duration_weeks': 12
        }
    }

    for gap in prioritized_gaps:
        facet = gap['facet']
        if facet in skill_resources:
            resource_info = skill_resources[facet]
            recommendations.append({
                'skill': resource_info['name'],
                'facet': facet,
                'priority': gap['priority'],
                'gap_amount': gap['gap'],
                'current_level': gap['current'],
                'target_level': gap['required'],
                'recommended_resources': resource_info['resources'],
                'estimated_duration_weeks': resource_info['duration_weeks'],
                'learning_approach': get_learning_approach(gap['priority'])
            })

    return recommendations


def get_learning_approach(priority: str) -> str:
    """Get recommended learning approach based on priority"""
    approaches = {
        'critical': 'Intensive study with daily practice (2-3 hours/day)',
        'moderate': 'Regular practice with weekly goals (1 hour/day)',
        'minor': 'Gradual improvement with consistent habits (30 min/day)'
    }
    return approaches.get(priority, 'Regular practice recommended')


def compare_profiles_gap_analysis(
    current_profile: Dict[str, float],
    previous_profile: Dict[str, float],
    career_requirements: Dict[str, float]
) -> Dict:
    """
    Compare skill gap progress between two assessment periods

    Args:
        current_profile: Current profile vector
        previous_profile: Previous profile vector
        career_requirements: Target career requirements

    Returns:
        Dictionary containing gap progress analysis
    """
    current_gaps = {}
    previous_gaps = {}
    improvements = []

    # Calculate current and previous gaps
    for facet, required_level in career_requirements.items():
        current_level = current_profile.get(facet, 0.0)
        previous_level = previous_profile.get(facet, 0.0)

        current_gap = max(0, required_level - current_level)
        previous_gap = max(0, required_level - previous_level)

        if current_gap > 0 or previous_gap > 0:
            gap_reduction = previous_gap - current_gap

            improvements.append({
                'facet': facet,
                'previous_gap': previous_gap,
                'current_gap': current_gap,
                'gap_reduction': gap_reduction,
                'improvement_percentage': (gap_reduction / previous_gap * 100) if previous_gap > 0 else 0,
                'status': 'improved' if gap_reduction > 0 else 'unchanged' if gap_reduction == 0 else 'regressed'
            })

    # Overall progress metrics
    total_previous_gap = sum(i['previous_gap'] for i in improvements)
    total_current_gap = sum(i['current_gap'] for i in improvements)
    total_reduction = total_previous_gap - total_current_gap

    return {
        'improvements': sorted(improvements, key=lambda x: x['gap_reduction'], reverse=True),
        'total_previous_gap': total_previous_gap,
        'total_current_gap': total_current_gap,
        'total_gap_reduction': total_reduction,
        'progress_percentage': (total_reduction / total_previous_gap * 100) if total_previous_gap > 0 else 0,
        'improved_facets': sum(1 for i in improvements if i['status'] == 'improved'),
        'unchanged_facets': sum(1 for i in improvements if i['status'] == 'unchanged'),
        'regressed_facets': sum(1 for i in improvements if i['status'] == 'regressed')
    }


# CLI Interface
if __name__ == '__main__':
    import sys

    # Example usage
    example_profile = {
        'iq_lr': 75.0,
        'iq_nr': 70.0,
        'iq_vr': 80.0,
        'iq_sr': 65.0,
        'eq_empathy': 85.0,
        'eq_social': 75.0,
        'eq_self_awareness': 70.0,
        'eq_self_regulation': 65.0,
        'dq_info_literacy': 80.0,
        'dq_creativity': 85.0,
        'dq_safety': 70.0,
        'dq_collaboration': 75.0,
        'aq_control': 70.0,
        'aq_ownership': 75.0,
        'aq_reach': 65.0,
        'aq_endurance': 80.0
    }

    example_requirements = {
        'iq_lr': 90.0,
        'iq_nr': 85.0,
        'dq_creativity': 95.0,
        'dq_collaboration': 85.0,
        'aq_ownership': 90.0,
        'aq_endurance': 90.0
    }

    result = analyze_skill_gap(example_profile, example_requirements, 'Software Engineer')

    print(json.dumps(result, indent=2))
