"""
Progress Tracking Service
Manages user progress tracking and comparison over time
"""

from typing import Dict, List, Optional
from datetime import datetime
import uuid


class ProgressTrackingService:
    """Service for tracking and analyzing user progress over time"""

    def __init__(self, db_connection):
        """Initialize service with database connection"""
        self.db = db_connection

    async def create_progress_record(
        self,
        user_id: str,
        assessment_id: str,
        previous_assessment_id: Optional[str] = None
    ) -> Dict:
        """
        Create a new progress tracking record

        Args:
            user_id: User identifier
            assessment_id: Latest assessment identifier
            previous_assessment_id: Previous assessment for comparison

        Returns:
            Dictionary containing progress tracking record
        """
        # Get current and previous results
        current_result = await self._get_assessment_result(assessment_id)

        if not current_result:
            raise ValueError("Assessment result not found")

        improvements = {}

        if previous_assessment_id:
            previous_result = await self._get_assessment_result(previous_assessment_id)

            if previous_result:
                # Calculate improvements
                improvements = {
                    'iq': current_result['iq_score'] - previous_result['iq_score'],
                    'eq': current_result['eq_score'] - previous_result['eq_score'],
                    'dq': current_result['dq_score'] - previous_result['dq_score'],
                    'aq': current_result['aq_score'] - previous_result['aq_score']
                }

        # Create progress record
        progress_id = str(uuid.uuid4())
        record = {
            'id': progress_id,
            'user_id': user_id,
            'assessment_id': assessment_id,
            'previous_assessment_id': previous_assessment_id,
            'improvement_iq': improvements.get('iq', None),
            'improvement_eq': improvements.get('eq', None),
            'improvement_dq': improvements.get('dq', None),
            'improvement_aq': improvements.get('aq', None),
            'tracked_at': datetime.utcnow()
        }

        # Save to database
        await self._save_progress_record(record)

        return record

    async def get_user_progress_history(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get user's progress history

        Args:
            user_id: User identifier
            limit: Maximum number of records to return

        Returns:
            List of progress tracking records
        """
        query = """
            SELECT pt.*,
                   ar.iq_score, ar.eq_score, ar.dq_score, ar.aq_score,
                   ar.ikigai_harmonic, ar.calculated_at
            FROM progress_tracking pt
            JOIN assessments a ON pt.assessment_id = a.id
            JOIN assessment_results ar ON a.id = ar.assessment_id
            WHERE pt.user_id = %s
            ORDER BY pt.tracked_at DESC
            LIMIT %s
        """

        records = await self.db.fetch_all(query, (user_id, limit))

        return [dict(record) for record in records]

    async def compare_assessments(
        self,
        assessment_id_1: str,
        assessment_id_2: str
    ) -> Dict:
        """
        Compare two assessments and show progress

        Args:
            assessment_id_1: First assessment (usually older)
            assessment_id_2: Second assessment (usually newer)

        Returns:
            Dictionary containing comparison results
        """
        result1 = await self._get_assessment_result(assessment_id_1)
        result2 = await self._get_assessment_result(assessment_id_2)

        if not result1 or not result2:
            raise ValueError("One or both assessment results not found")

        comparison = {
            'assessment_1': {
                'id': assessment_id_1,
                'date': result1['calculated_at'],
                'scores': {
                    'iq': result1['iq_score'],
                    'eq': result1['eq_score'],
                    'dq': result1['dq_score'],
                    'aq': result1['aq_score'],
                    'ikigai': result1['ikigai_harmonic']
                }
            },
            'assessment_2': {
                'id': assessment_id_2,
                'date': result2['calculated_at'],
                'scores': {
                    'iq': result2['iq_score'],
                    'eq': result2['eq_score'],
                    'dq': result2['dq_score'],
                    'aq': result2['aq_score'],
                    'ikigai': result2['ikigai_harmonic']
                }
            },
            'improvements': {
                'iq': result2['iq_score'] - result1['iq_score'],
                'eq': result2['eq_score'] - result1['eq_score'],
                'dq': result2['dq_score'] - result1['dq_score'],
                'aq': result2['aq_score'] - result1['aq_score'],
                'ikigai': result2['ikigai_harmonic'] - result1['ikigai_harmonic']
            },
            'improvement_percentages': {
                'iq': ((result2['iq_score'] - result1['iq_score']) / result1['iq_score'] * 100) if result1['iq_score'] > 0 else 0,
                'eq': ((result2['eq_score'] - result1['eq_score']) / result1['eq_score'] * 100) if result1['eq_score'] > 0 else 0,
                'dq': ((result2['dq_score'] - result1['dq_score']) / result1['dq_score'] * 100) if result1['dq_score'] > 0 else 0,
                'aq': ((result2['aq_score'] - result1['aq_score']) / result1['aq_score'] * 100) if result1['aq_score'] > 0 else 0,
            },
            'time_between_assessments': (result2['calculated_at'] - result1['calculated_at']).days
        }

        return comparison

    async def get_progress_analytics(self, user_id: str) -> Dict:
        """
        Get analytics for user's progress over time

        Args:
            user_id: User identifier

        Returns:
            Dictionary containing progress analytics
        """
        history = await self.get_user_progress_history(user_id, limit=100)

        if len(history) < 2:
            return {
                'total_assessments': len(history),
                'message': 'Need at least 2 assessments for analytics'
            }

        # Calculate trends
        iq_trend = self._calculate_trend([h['iq_score'] for h in history])
        eq_trend = self._calculate_trend([h['eq_score'] for h in history])
        dq_trend = self._calculate_trend([h['dq_score'] for h in history])
        aq_trend = self._calculate_trend([h['aq_score'] for h in history])

        # Find best improvement
        best_improvement = max(
            [
                ('IQ', sum(h.get('improvement_iq', 0) or 0 for h in history)),
                ('EQ', sum(h.get('improvement_eq', 0) or 0 for h in history)),
                ('DQ', sum(h.get('improvement_dq', 0) or 0 for h in history)),
                ('AQ', sum(h.get('improvement_aq', 0) or 0 for h in history))
            ],
            key=lambda x: x[1]
        )

        return {
            'total_assessments': len(history),
            'trends': {
                'iq': iq_trend,
                'eq': eq_trend,
                'dq': dq_trend,
                'aq': aq_trend
            },
            'best_improvement': {
                'category': best_improvement[0],
                'total_points': round(best_improvement[1], 2)
            },
            'latest_scores': {
                'iq': history[0]['iq_score'],
                'eq': history[0]['eq_score'],
                'dq': history[0]['dq_score'],
                'aq': history[0]['aq_score']
            },
            'first_assessment_date': history[-1]['calculated_at'],
            'latest_assessment_date': history[0]['calculated_at']
        }

    def _calculate_trend(self, scores: List[float]) -> str:
        """Calculate trend from list of scores"""
        if len(scores) < 2:
            return 'insufficient_data'

        # Simple linear trend
        avg_change = (scores[0] - scores[-1]) / len(scores)

        if avg_change > 1:
            return 'improving'
        elif avg_change < -1:
            return 'declining'
        else:
            return 'stable'

    async def _get_assessment_result(self, assessment_id: str) -> Optional[Dict]:
        """Get assessment result from database"""
        query = """
            SELECT * FROM assessment_results
            WHERE assessment_id = %s
        """

        result = await self.db.fetch_one(query, (assessment_id,))

        return dict(result) if result else None

    async def _save_progress_record(self, record: Dict) -> None:
        """Save progress record to database"""
        query = """
            INSERT INTO progress_tracking
            (id, user_id, assessment_id, previous_assessment_id,
             improvement_iq, improvement_eq, improvement_dq, improvement_aq, tracked_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        await self.db.execute(
            query,
            (
                record['id'],
                record['user_id'],
                record['assessment_id'],
                record.get('previous_assessment_id'),
                record.get('improvement_iq'),
                record.get('improvement_eq'),
                record.get('improvement_dq'),
                record.get('improvement_aq'),
                record['tracked_at']
            )
        )
