"""
Progress Comparison Algorithm
Analyzes progress between two assessments
"""

from typing import Dict, List
import json
from datetime import datetime, timedelta


def compare_progress(
    current_assessment: Dict,
    previous_assessment: Dict
) -> Dict:
    """
    Compare two assessment results and analyze progress

    Args:
        current_assessment: Current assessment results
        previous_assessment: Previous assessment results

    Returns:
        Dictionary containing detailed progress comparison
    """
    # Calculate score changes
    score_changes = {
        'iq': current_assessment['iq_score'] - previous_assessment['iq_score'],
        'eq': current_assessment['eq_score'] - previous_assessment['eq_score'],
        'dq': current_assessment['dq_score'] - previous_assessment['dq_score'],
        'aq': current_assessment['aq_score'] - previous_assessment['aq_score']
    }

    # Calculate percentage changes
    percentage_changes = {}
    for category, change in score_changes.items():
        prev_score = previous_assessment[f'{category}_score']
        if prev_score > 0:
            percentage_changes[category] = (change / prev_score) * 100
        else:
            percentage_changes[category] = 0

    # Analyze facet-level changes
    facet_changes = analyze_facet_changes(
        current_assessment.get('profile_vector', {}),
        previous_assessment.get('profile_vector', {})
    )

    # Determine overall progress status
    overall_status = determine_progress_status(score_changes)

    # Generate insights
    insights = generate_progress_insights(
        score_changes,
        percentage_changes,
        facet_changes
    )

    # Calculate momentum
    momentum = calculate_progress_momentum(score_changes, percentage_changes)

    return {
        'score_changes': score_changes,
        'percentage_changes': percentage_changes,
        'facet_changes': facet_changes,
        'overall_status': overall_status,
        'momentum': momentum,
        'insights': insights,
        'time_between_assessments': (
            current_assessment.get('calculated_at', datetime.now()) -
            previous_assessment.get('calculated_at', datetime.now())
        ).days if isinstance(current_assessment.get('calculated_at'), datetime) else None
    }


def analyze_facet_changes(
    current_vector: Dict[str, float],
    previous_vector: Dict[str, float]
) -> Dict:
    """Analyze changes at facet level"""
    facet_changes = {}

    all_facets = set(list(current_vector.keys()) + list(previous_vector.keys()))

    for facet in all_facets:
        current_value = current_vector.get(facet, 0)
        previous_value = previous_vector.get(facet, 0)
        change = current_value - previous_value

        facet_changes[facet] = {
            'current': current_value,
            'previous': previous_value,
            'change': change,
            'change_percentage': (change / previous_value * 100) if previous_value > 0 else 0
        }

    # Sort by absolute change
    sorted_changes = sorted(
        facet_changes.items(),
        key=lambda x: abs(x[1]['change']),
        reverse=True
    )

    return {
        'all_facets': facet_changes,
        'top_improvements': [
            {'facet': f, 'data': d}
            for f, d in sorted_changes
            if d['change'] > 0
        ][:5],
        'top_declines': [
            {'facet': f, 'data': d}
            for f, d in sorted_changes
            if d['change'] < 0
        ][:5]
    }


def determine_progress_status(score_changes: Dict[str, float]) -> str:
    """Determine overall progress status"""
    positive_changes = sum(1 for change in score_changes.values() if change > 0)
    negative_changes = sum(1 for change in score_changes.values() if change < 0)
    total_change = sum(score_changes.values())

    if positive_changes >= 3 and total_change > 10:
        return 'excellent_progress'
    elif positive_changes >= 2 and total_change > 5:
        return 'good_progress'
    elif positive_changes == negative_changes:
        return 'mixed_progress'
    elif negative_changes >= 3:
        return 'needs_attention'
    else:
        return 'stable'


def calculate_progress_momentum(
    score_changes: Dict[str, float],
    percentage_changes: Dict[str, float]
) -> Dict:
    """Calculate progress momentum"""
    avg_change = sum(score_changes.values()) / len(score_changes)
    avg_percentage = sum(percentage_changes.values()) / len(percentage_changes)

    # Momentum score (0-100)
    momentum_score = min(100, max(0, (avg_percentage + 50)))

    return {
        'momentum_score': round(momentum_score, 2),
        'average_change': round(avg_change, 2),
        'average_percentage': round(avg_percentage, 2),
        'direction': 'upward' if avg_change > 0 else 'downward' if avg_change < 0 else 'neutral'
    }


def generate_progress_insights(
    score_changes: Dict[str, float],
    percentage_changes: Dict[str, float],
    facet_changes: Dict
) -> List[str]:
    """Generate human-readable insights about progress"""
    insights = []

    # Overall progress insight
    total_improvement = sum(score_changes.values())
    if total_improvement > 15:
        insights.append("Outstanding overall improvement across all dimensions!")
    elif total_improvement > 5:
        insights.append("Good progress - you're moving in the right direction.")
    elif total_improvement < -5:
        insights.append("Some scores have declined - consider revisiting your learning strategies.")

    # Category-specific insights
    for category, change in score_changes.items():
        if change > 10:
            insights.append(f"Excellent {category.upper()} improvement (+{change:.1f} points)")
        elif change < -10:
            insights.append(f"{category.upper()} needs attention ({change:.1f} points)")

    # Facet-specific insights
    if facet_changes['top_improvements']:
        top_facet = facet_changes['top_improvements'][0]
        insights.append(
            f"Strongest improvement in {top_facet['facet']} "
            f"(+{top_facet['data']['change']:.1f} points)"
        )

    if facet_changes['top_declines']:
        top_decline = facet_changes['top_declines'][0]
        insights.append(
            f"Focus needed on {top_decline['facet']} "
            f"({top_decline['data']['change']:.1f} points)"
        )

    # Consistency insight
    positive_count = sum(1 for c in score_changes.values() if c > 0)
    if positive_count == len(score_changes):
        insights.append("Consistent improvement across all areas - keep it up!")

    return insights


def calculate_growth_rate(
    assessment_history: List[Dict]
) -> Dict:
    """Calculate growth rate over multiple assessments"""
    if len(assessment_history) < 2:
        return {
            'error': 'Need at least 2 assessments to calculate growth rate'
        }

    # Sort by date
    sorted_history = sorted(
        assessment_history,
        key=lambda x: x.get('calculated_at', datetime.min)
    )

    # Calculate growth rates for each category
    growth_rates = {}

    for category in ['iq', 'eq', 'dq', 'aq']:
        scores = [a[f'{category}_score'] for a in sorted_history]

        # Simple linear growth rate
        first_score = scores[0]
        last_score = scores[-1]

        if first_score > 0:
            total_growth = ((last_score - first_score) / first_score) * 100
            num_periods = len(scores) - 1
            avg_growth_per_period = total_growth / num_periods if num_periods > 0 else 0

            growth_rates[category] = {
                'total_growth_percentage': round(total_growth, 2),
                'average_growth_per_assessment': round(avg_growth_per_period, 2),
                'trajectory': 'upward' if total_growth > 0 else 'downward' if total_growth < 0 else 'flat'
            }

    return {
        'growth_rates': growth_rates,
        'total_assessments': len(sorted_history),
        'time_span_days': (
            sorted_history[-1].get('calculated_at', datetime.now()) -
            sorted_history[0].get('calculated_at', datetime.now())
        ).days if isinstance(sorted_history[0].get('calculated_at'), datetime) else None
    }


# CLI Interface
if __name__ == '__main__':
    # Example usage
    previous = {
        'iq_score': 70.0,
        'eq_score': 75.0,
        'dq_score': 65.0,
        'aq_score': 80.0,
        'profile_vector': {
            'iq_lr': 65.0,
            'iq_nr': 70.0,
            'eq_empathy': 80.0
        },
        'calculated_at': datetime.now() - timedelta(days=30)
    }

    current = {
        'iq_score': 85.0,
        'eq_score': 80.0,
        'dq_score': 75.0,
        'aq_score': 85.0,
        'profile_vector': {
            'iq_lr': 80.0,
            'iq_nr': 85.0,
            'eq_empathy': 85.0
        },
        'calculated_at': datetime.now()
    }

    result = compare_progress(current, previous)

    print(json.dumps(result, indent=2, default=str))
