"""
Ikigai calculation algorithm for MyWay Career Assessment System.
"""
from typing import Dict, List, Tuple
import math
from ..models.profile_vector import ProfileVector


class IkigaiCalculationAlgorithm:
    """Algorithm for calculating Ikigai scores from assessment results."""
    
    @staticmethod
    def calculate_ikigai_scores(profile_vector: ProfileVector) -> Dict[str, float]:
        """
        Calculate Ikigai scores from profile vector.
        
        Ikigai Formula:
        - Love = (EQ_empathy + EQ_social + DQ_creativity) / 3
        - Good at = (IQ_lr + IQ_nr + IQ_vr + IQ_sr) / 4
        - World needs = (DQ_info_literacy + DQ_safety + AQ_control + AQ_ownership) / 4
        - Paid for = (AQ_reach + AQ_endurance + EQ_self_awareness + EQ_self_regulation) / 4
        
        Harmonic Mean: 4 / (1/Love + 1/Good_at + 1/World_needs + 1/Paid_for)
        Geometric Mean: (Love * Good_at * World_needs * Paid_for)^(1/4)
        """
        # Extract scores from profile vector
        scores = profile_vector.to_vector()
        
        # Calculate individual Ikigai axes
        love = IkigaiCalculationAlgorithm._calculate_love_axis(scores)
        good_at = IkigaiCalculationAlgorithm._calculate_good_at_axis(scores)
        world_needs = IkigaiCalculationAlgorithm._calculate_world_needs_axis(scores)
        paid_for = IkigaiCalculationAlgorithm._calculate_paid_for_axis(scores)
        
        # Calculate harmonic and geometric means
        harmonic_mean = IkigaiCalculationAlgorithm._calculate_harmonic_mean(
            love, good_at, world_needs, paid_for
        )
        geometric_mean = IkigaiCalculationAlgorithm._calculate_geometric_mean(
            love, good_at, world_needs, paid_for
        )
        
        return {
            'ikigai_love': love,
            'ikigai_good_at': good_at,
            'ikigai_world_needs': world_needs,
            'ikigai_paid_for': paid_for,
            'ikigai_harmonic': harmonic_mean,
            'ikigai_geometric': geometric_mean
        }
    
    @staticmethod
    def _calculate_love_axis(scores: List[float]) -> float:
        """Calculate Love axis: passion and what you love doing."""
        # EQ_empathy (index 4) + EQ_social (index 5) + DQ_creativity (index 9)
        empathy = scores[4] if len(scores) > 4 else 0
        social = scores[5] if len(scores) > 5 else 0
        creativity = scores[9] if len(scores) > 9 else 0
        
        return (empathy + social + creativity) / 3
    
    @staticmethod
    def _calculate_good_at_axis(scores: List[float]) -> float:
        """Calculate Good at axis: what you're good at."""
        # IQ_lr (index 0) + IQ_nr (index 1) + IQ_vr (index 2) + IQ_sr (index 3)
        lr = scores[0] if len(scores) > 0 else 0
        nr = scores[1] if len(scores) > 1 else 0
        vr = scores[2] if len(scores) > 2 else 0
        sr = scores[3] if len(scores) > 3 else 0
        
        return (lr + nr + vr + sr) / 4
    
    @staticmethod
    def _calculate_world_needs_axis(scores: List[float]) -> float:
        """Calculate World needs axis: what the world needs."""
        # DQ_info_literacy (index 8) + DQ_safety (index 10) + AQ_control (index 12) + AQ_ownership (index 13)
        info_literacy = scores[8] if len(scores) > 8 else 0
        safety = scores[10] if len(scores) > 10 else 0
        control = scores[12] if len(scores) > 12 else 0
        ownership = scores[13] if len(scores) > 13 else 0
        
        return (info_literacy + safety + control + ownership) / 4
    
    @staticmethod
    def _calculate_paid_for_axis(scores: List[float]) -> float:
        """Calculate Paid for axis: what you can be paid for."""
        # AQ_reach (index 14) + AQ_endurance (index 15) + EQ_self_awareness (index 6) + EQ_self_regulation (index 7)
        reach = scores[14] if len(scores) > 14 else 0
        endurance = scores[15] if len(scores) > 15 else 0
        self_awareness = scores[6] if len(scores) > 6 else 0
        self_regulation = scores[7] if len(scores) > 7 else 0
        
        return (reach + endurance + self_awareness + self_regulation) / 4
    
    @staticmethod
    def _calculate_harmonic_mean(love: float, good_at: float, world_needs: float, paid_for: float) -> float:
        """Calculate harmonic mean of Ikigai scores."""
        # Avoid division by zero
        if any(score == 0 for score in [love, good_at, world_needs, paid_for]):
            return 0.0
        
        return 4 / (1/love + 1/good_at + 1/world_needs + 1/paid_for)
    
    @staticmethod
    def _calculate_geometric_mean(love: float, good_at: float, world_needs: float, paid_for: float) -> float:
        """Calculate geometric mean of Ikigai scores."""
        # Avoid negative values or zero
        if any(score <= 0 for score in [love, good_at, world_needs, paid_for]):
            return 0.0
        
        return math.pow(love * good_at * world_needs * paid_for, 1/4)
    
    @staticmethod
    def get_ikigai_interpretation(scores: Dict[str, float]) -> Dict[str, str]:
        """Get interpretation of Ikigai scores."""
        love = scores.get('ikigai_love', 0)
        good_at = scores.get('ikigai_good_at', 0)
        world_needs = scores.get('ikigai_world_needs', 0)
        paid_for = scores.get('ikigai_paid_for', 0)
        
        interpretations = {
            'love': IkigaiCalculationAlgorithm._interpret_axis(love, 'đam mê'),
            'good_at': IkigaiCalculationAlgorithm._interpret_axis(good_at, 'tài năng'),
            'world_needs': IkigaiCalculationAlgorithm._interpret_axis(world_needs, 'nhu cầu xã hội'),
            'paid_for': IkigaiCalculationAlgorithm._interpret_axis(paid_for, 'khả năng kiếm tiền')
        }
        
        # Overall interpretation
        harmonic = scores.get('ikigai_harmonic', 0)
        geometric = scores.get('ikigai_geometric', 0)
        
        if harmonic >= 80 and geometric >= 80:
            overall = "Bạn đã tìm thấy vùng Ikigai của mình! Tất cả 4 yếu tố đều ở mức cao."
        elif harmonic >= 60 and geometric >= 60:
            overall = "Bạn đang tiến gần đến vùng Ikigai. Một số yếu tố cần được phát triển thêm."
        elif harmonic >= 40 and geometric >= 40:
            overall = "Bạn đang trong quá trình khám phá Ikigai. Cần tập trung phát triển các yếu tố còn yếu."
        else:
            overall = "Bạn cần thời gian để khám phá và phát triển các yếu tố Ikigai."
        
        interpretations['overall'] = overall
        return interpretations
    
    @staticmethod
    def _interpret_axis(score: float, axis_name: str) -> str:
        """Interpret individual axis score."""
        if score >= 80:
            return f"Bạn có {axis_name} rất mạnh ({score:.1f}/100)"
        elif score >= 60:
            return f"Bạn có {axis_name} khá tốt ({score:.1f}/100)"
        elif score >= 40:
            return f"Bạn có {axis_name} ở mức trung bình ({score:.1f}/100)"
        else:
            return f"Bạn cần phát triển {axis_name} ({score:.1f}/100)"
    
    @staticmethod
    def get_ikigai_quadrant(love: float, good_at: float, world_needs: float, paid_for: float) -> str:
        """Determine which Ikigai quadrant the user is in."""
        # Define quadrants based on high/low scores
        high_love = love >= 60
        high_good_at = good_at >= 60
        high_world_needs = world_needs >= 60
        high_paid_for = paid_for >= 60
        
        if high_love and high_good_at and high_world_needs and high_paid_for:
            return "Ikigai Zone - Perfect balance of all four elements"
        elif high_love and high_good_at and not high_world_needs and not high_paid_for:
            return "Passion - You love it and you're good at it, but world doesn't need it and you can't be paid for it"
        elif high_love and not high_good_at and high_world_needs and not high_paid_for:
            return "Mission - You love it and world needs it, but you're not good at it and can't be paid for it"
        elif not high_love and high_good_at and high_world_needs and not high_paid_for:
            return "Profession - You're good at it and world needs it, but you don't love it and can't be paid for it"
        elif not high_love and high_good_at and not high_world_needs and high_paid_for:
            return "Vocation - You're good at it and can be paid for it, but you don't love it and world doesn't need it"
        else:
            return "Exploration - You're still discovering your Ikigai"
    
    @staticmethod
    def get_development_recommendations(scores: Dict[str, float]) -> List[str]:
        """Get recommendations for developing Ikigai scores."""
        recommendations = []
        
        love = scores.get('ikigai_love', 0)
        good_at = scores.get('ikigai_good_at', 0)
        world_needs = scores.get('ikigai_world_needs', 0)
        paid_for = scores.get('ikigai_paid_for', 0)
        
        if love < 60:
            recommendations.append("Phát triển kỹ năng giao tiếp và sáng tạo để tăng điểm Đam mê")
        
        if good_at < 60:
            recommendations.append("Rèn luyện tư duy logic và kỹ năng phân tích để tăng điểm Tài năng")
        
        if world_needs < 60:
            recommendations.append("Học hỏi về công nghệ và phát triển kỹ năng giải quyết vấn đề để tăng điểm Nhu cầu xã hội")
        
        if paid_for < 60:
            recommendations.append("Phát triển kỹ năng lãnh đạo và khả năng thích ứng để tăng điểm Khả năng kiếm tiền")
        
        if not recommendations:
            recommendations.append("Tuyệt vời! Bạn đã có sự cân bằng tốt trong tất cả các yếu tố Ikigai")
        
        return recommendations