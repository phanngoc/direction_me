"""
Career fit score calculation algorithm for MyWay Career Assessment System.
"""
from typing import Dict, List, Tuple, Optional
import math
from ..models.profile_vector import ProfileVector
from ..models.career_rule import CareerRule


class CareerFitCalculator:
    """Calculates career fit scores based on profile vector and career rules."""
    
    @staticmethod
    def calculate_fit_score(
        profile_vector: ProfileVector,
        career_rule: CareerRule,
        include_explanation: bool = True
    ) -> Dict[str, any]:
        """
        Calculate career fit score for a given profile vector and career rule.
        
        Args:
            profile_vector: 16-dimensional profile vector
            career_rule: Career mapping rule with weights and thresholds
            include_explanation: Whether to include detailed explanation
            
        Returns:
            Dictionary containing fit score, breakdown, and explanation
        """
        profile_scores = profile_vector.to_vector()
        weights = career_rule.weights
        thresholds = career_rule.thresholds
        bonus_keys = career_rule.bonus_keys or []
        
        # Calculate weighted score
        weighted_score = 0.0
        total_weight = 0.0
        facet_scores = {}
        threshold_met = {}
        
        # Process each facet
        for i, score in enumerate(profile_scores):
            if i >= len(ProfileVector.FACET_NAMES):
                break
                
            facet_name = ProfileVector.FACET_NAMES[i]
            if facet_name not in weights:
                continue
            
            weight = weights[facet_name]
            threshold = thresholds.get(facet_name, 0)
            
            # Check if meets threshold
            meets_threshold = score >= threshold
            threshold_met[facet_name] = meets_threshold
            
            # Calculate weighted contribution
            facet_contribution = score * weight
            weighted_score += facet_contribution
            total_weight += weight
            
            # Store facet details
            facet_scores[facet_name] = {
                'score': score,
                'weight': weight,
                'threshold': threshold,
                'meets_threshold': meets_threshold,
                'contribution': facet_contribution
            }
        
        # Calculate base fit score
        if total_weight > 0:
            base_fit_score = (weighted_score / total_weight) * 100
        else:
            base_fit_score = 0.0
        
        # Apply bonus for key facets
        bonus_score = 0.0
        bonus_details = {}
        
        for facet_name in bonus_keys:
            if facet_name in facet_scores:
                facet_data = facet_scores[facet_name]
                if facet_data['meets_threshold']:
                    # Bonus proportional to how much above threshold
                    excess = max(0, facet_data['score'] - facet_data['threshold'])
                    bonus = min(10, excess * 0.1)  # Max 10 bonus points
                    bonus_score += bonus
                    bonus_details[facet_name] = bonus
        
        # Calculate final fit score
        final_fit_score = min(100, base_fit_score + bonus_score)
        
        # Calculate threshold compliance
        total_facets = len(facet_scores)
        met_thresholds = sum(1 for met in threshold_met.values() if met)
        threshold_compliance = (met_thresholds / total_facets) * 100 if total_facets > 0 else 0
        
        # Generate explanation if requested
        explanation = ""
        if include_explanation:
            explanation = CareerFitCalculator._generate_explanation(
                career_rule.career_name,
                facet_scores,
                threshold_met,
                bonus_details,
                final_fit_score,
                threshold_compliance
            )
        
        return {
            'fit_score': round(final_fit_score, 2),
            'base_score': round(base_fit_score, 2),
            'bonus_score': round(bonus_score, 2),
            'threshold_compliance': round(threshold_compliance, 2),
            'facet_scores': facet_scores,
            'threshold_met': threshold_met,
            'bonus_details': bonus_details,
            'explanation': explanation,
            'career_name': career_rule.career_name
        }
    
    @staticmethod
    def calculate_multiple_fit_scores(
        profile_vector: ProfileVector,
        career_rules: List[CareerRule],
        include_explanations: bool = True
    ) -> List[Dict[str, any]]:
        """
        Calculate fit scores for multiple careers.
        
        Args:
            profile_vector: 16-dimensional profile vector
            career_rules: List of career mapping rules
            include_explanations: Whether to include detailed explanations
            
        Returns:
            List of fit score dictionaries, sorted by fit score (descending)
        """
        results = []
        
        for career_rule in career_rules:
            if not career_rule.is_active:
                continue
                
            fit_data = CareerFitCalculator.calculate_fit_score(
                profile_vector,
                career_rule,
                include_explanations
            )
            results.append(fit_data)
        
        # Sort by fit score (descending)
        results.sort(key=lambda x: x['fit_score'], reverse=True)
        
        # Add ranking
        for i, result in enumerate(results):
            result['rank'] = i + 1
        
        return results
    
    @staticmethod
    def _generate_explanation(
        career_name: str,
        facet_scores: Dict[str, Dict],
        threshold_met: Dict[str, bool],
        bonus_details: Dict[str, float],
        final_fit_score: float,
        threshold_compliance: float
    ) -> str:
        """Generate human-readable explanation for career fit."""
        explanation_parts = []
        
        # Overall assessment
        if final_fit_score >= 80:
            explanation_parts.append(f"Bạn có tiềm năng rất cao để thành công trong {career_name}")
        elif final_fit_score >= 60:
            explanation_parts.append(f"Bạn có tiềm năng tốt để phát triển trong {career_name}")
        elif final_fit_score >= 40:
            explanation_parts.append(f"Bạn có thể phát triển để phù hợp với {career_name}")
        else:
            explanation_parts.append(f"Bạn cần đầu tư thời gian để phát triển các kỹ năng cần thiết cho {career_name}")
        
        # Threshold compliance
        if threshold_compliance >= 80:
            explanation_parts.append("Bạn đáp ứng hầu hết các yêu cầu cơ bản")
        elif threshold_compliance >= 60:
            explanation_parts.append("Bạn đáp ứng phần lớn các yêu cầu cơ bản")
        else:
            explanation_parts.append("Bạn cần cải thiện nhiều kỹ năng cơ bản")
        
        # Key strengths
        strengths = []
        for facet_name, data in facet_scores.items():
            if data['meets_threshold'] and data['weight'] >= 0.8:
                strengths.append(facet_name)
        
        if strengths:
            explanation_parts.append(f"Điểm mạnh chính: {', '.join(strengths[:3])}")
        
        # Bonus achievements
        if bonus_details:
            bonus_facets = list(bonus_details.keys())
            explanation_parts.append(f"Thành tích đặc biệt: {', '.join(bonus_facets[:2])}")
        
        # Areas for improvement
        weak_areas = []
        for facet_name, data in facet_scores.items():
            if not data['meets_threshold'] and data['weight'] >= 0.7:
                weak_areas.append(facet_name)
        
        if weak_areas:
            explanation_parts.append(f"Cần cải thiện: {', '.join(weak_areas[:3])}")
        
        return ". ".join(explanation_parts) + "."
    
    @staticmethod
    def get_fit_score_interpretation(fit_score: float) -> Dict[str, str]:
        """
        Get interpretation of fit score.
        
        Args:
            fit_score: Career fit score (0-100)
            
        Returns:
            Dictionary with interpretation details
        """
        if fit_score >= 90:
            return {
                'level': 'Excellent',
                'description': 'Rất phù hợp',
                'color': 'green',
                'recommendation': 'Nghề nghiệp lý tưởng cho bạn'
            }
        elif fit_score >= 80:
            return {
                'level': 'Very Good',
                'description': 'Phù hợp cao',
                'color': 'blue',
                'recommendation': 'Nghề nghiệp tốt, nên theo đuổi'
            }
        elif fit_score >= 70:
            return {
                'level': 'Good',
                'description': 'Phù hợp tốt',
                'color': 'yellow',
                'recommendation': 'Có tiềm năng, cần phát triển thêm'
            }
        elif fit_score >= 60:
            return {
                'level': 'Fair',
                'description': 'Phù hợp trung bình',
                'color': 'orange',
                'recommendation': 'Cần đầu tư thời gian để phát triển'
            }
        else:
            return {
                'level': 'Poor',
                'description': 'Ít phù hợp',
                'color': 'red',
                'recommendation': 'Cần cải thiện đáng kể các kỹ năng'
            }