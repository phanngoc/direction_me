"""
Career explanation generation logic for MyWay Career Assessment System.
"""
from typing import Dict, List, Tuple
import random


class CareerExplanationGenerator:
    """Generates human-readable explanations for career suggestions."""
    
    # Explanation templates
    STRENGTH_TEMPLATES = {
        "iq_lr": [
            "Bạn có tư duy logic mạnh mẽ, rất phù hợp với {career}",
            "Khả năng phân tích logic của bạn sẽ giúp bạn thành công trong {career}",
            "Tư duy logic tốt là điểm mạnh quan trọng cho {career}"
        ],
        "iq_nr": [
            "Kỹ năng toán học và số học của bạn rất phù hợp với {career}",
            "Khả năng xử lý số liệu sẽ là lợi thế lớn trong {career}",
            "Tư duy định lượng mạnh mẽ là yếu tố quan trọng cho {career}"
        ],
        "iq_vr": [
            "Khả năng ngôn ngữ và giao tiếp của bạn rất phù hợp với {career}",
            "Kỹ năng diễn đạt tốt sẽ giúp bạn thành công trong {career}",
            "Tư duy ngôn ngữ mạnh mẽ là điểm mạnh cho {career}"
        ],
        "iq_sr": [
            "Khả năng tư duy không gian của bạn rất phù hợp với {career}",
            "Tư duy hình học và không gian sẽ là lợi thế trong {career}",
            "Kỹ năng tư duy không gian tốt là yếu tố quan trọng cho {career}"
        ],
        "eq_empathy": [
            "Khả năng thấu hiểu cảm xúc của bạn rất phù hợp với {career}",
            "Sự đồng cảm sẽ giúp bạn thành công trong {career}",
            "Khả năng thấu hiểu người khác là điểm mạnh cho {career}"
        ],
        "eq_social": [
            "Kỹ năng giao tiếp xã hội của bạn rất phù hợp với {career}",
            "Khả năng tương tác với mọi người sẽ là lợi thế trong {career}",
            "Kỹ năng xã hội tốt là yếu tố quan trọng cho {career}"
        ],
        "eq_self_awareness": [
            "Khả năng tự nhận thức của bạn rất phù hợp với {career}",
            "Sự hiểu biết về bản thân sẽ giúp bạn thành công trong {career}",
            "Tự nhận thức tốt là điểm mạnh quan trọng cho {career}"
        ],
        "eq_self_regulation": [
            "Khả năng tự kiểm soát của bạn rất phù hợp với {career}",
            "Sự tự chủ sẽ là lợi thế lớn trong {career}",
            "Khả năng quản lý cảm xúc tốt là yếu tố quan trọng cho {career}"
        ],
        "dq_info_literacy": [
            "Kỹ năng tìm kiếm và đánh giá thông tin của bạn rất phù hợp với {career}",
            "Khả năng xử lý thông tin sẽ giúp bạn thành công trong {career}",
            "Kỹ năng thông tin tốt là điểm mạnh cho {career}"
        ],
        "dq_creativity": [
            "Khả năng sáng tạo của bạn rất phù hợp với {career}",
            "Tư duy sáng tạo sẽ là lợi thế lớn trong {career}",
            "Sự sáng tạo là yếu tố quan trọng cho {career}"
        ],
        "dq_safety": [
            "Khả năng bảo mật và an toàn của bạn rất phù hợp với {career}",
            "Ý thức về an toàn sẽ giúp bạn thành công trong {career}",
            "Kỹ năng bảo mật tốt là điểm mạnh cho {career}"
        ],
        "dq_collaboration": [
            "Khả năng hợp tác của bạn rất phù hợp với {career}",
            "Kỹ năng làm việc nhóm sẽ là lợi thế trong {career}",
            "Tinh thần hợp tác tốt là yếu tố quan trọng cho {career}"
        ],
        "aq_control": [
            "Khả năng kiểm soát tình huống của bạn rất phù hợp với {career}",
            "Sự chủ động sẽ giúp bạn thành công trong {career}",
            "Khả năng kiểm soát tốt là điểm mạnh cho {career}"
        ],
        "aq_ownership": [
            "Tinh thần trách nhiệm của bạn rất phù hợp với {career}",
            "Sự sở hữu công việc sẽ là lợi thế trong {career}",
            "Tinh thần chủ động tốt là yếu tố quan trọng cho {career}"
        ],
        "aq_reach": [
            "Khả năng mở rộng tầm ảnh hưởng của bạn rất phù hợp với {career}",
            "Tầm nhìn xa sẽ giúp bạn thành công trong {career}",
            "Khả năng tác động tích cực là điểm mạnh cho {career}"
        ],
        "aq_endurance": [
            "Khả năng kiên trì của bạn rất phù hợp với {career}",
            "Sự bền bỉ sẽ là lợi thế lớn trong {career}",
            "Tinh thần kiên trì tốt là yếu tố quan trọng cho {career}"
        ]
    }
    
    IMPROVEMENT_TEMPLATES = {
        "iq_lr": [
            "Cần phát triển tư duy logic để phù hợp hơn với {career}",
            "Rèn luyện khả năng phân tích logic sẽ giúp bạn thành công trong {career}",
            "Tư duy logic cần được cải thiện để phù hợp với {career}"
        ],
        "iq_nr": [
            "Cần cải thiện kỹ năng toán học để phù hợp với {career}",
            "Rèn luyện tư duy định lượng sẽ giúp bạn thành công trong {career}",
            "Kỹ năng số học cần được phát triển cho {career}"
        ],
        "iq_vr": [
            "Cần phát triển kỹ năng ngôn ngữ để phù hợp với {career}",
            "Rèn luyện khả năng giao tiếp sẽ giúp bạn thành công trong {career}",
            "Kỹ năng diễn đạt cần được cải thiện cho {career}"
        ],
        "iq_sr": [
            "Cần cải thiện tư duy không gian để phù hợp với {career}",
            "Rèn luyện khả năng tư duy hình học sẽ giúp bạn thành công trong {career}",
            "Kỹ năng không gian cần được phát triển cho {career}"
        ],
        "eq_empathy": [
            "Cần phát triển khả năng thấu hiểu cảm xúc để phù hợp với {career}",
            "Rèn luyện sự đồng cảm sẽ giúp bạn thành công trong {career}",
            "Khả năng thấu hiểu người khác cần được cải thiện cho {career}"
        ],
        "eq_social": [
            "Cần cải thiện kỹ năng giao tiếp xã hội để phù hợp với {career}",
            "Rèn luyện khả năng tương tác sẽ giúp bạn thành công trong {career}",
            "Kỹ năng xã hội cần được phát triển cho {career}"
        ],
        "eq_self_awareness": [
            "Cần phát triển khả năng tự nhận thức để phù hợp với {career}",
            "Rèn luyện sự hiểu biết về bản thân sẽ giúp bạn thành công trong {career}",
            "Tự nhận thức cần được cải thiện cho {career}"
        ],
        "eq_self_regulation": [
            "Cần cải thiện khả năng tự kiểm soát để phù hợp với {career}",
            "Rèn luyện sự tự chủ sẽ giúp bạn thành công trong {career}",
            "Khả năng quản lý cảm xúc cần được phát triển cho {career}"
        ],
        "dq_info_literacy": [
            "Cần phát triển kỹ năng tìm kiếm thông tin để phù hợp với {career}",
            "Rèn luyện khả năng đánh giá thông tin sẽ giúp bạn thành công trong {career}",
            "Kỹ năng thông tin cần được cải thiện cho {career}"
        ],
        "dq_creativity": [
            "Cần cải thiện khả năng sáng tạo để phù hợp với {career}",
            "Rèn luyện tư duy sáng tạo sẽ giúp bạn thành công trong {career}",
            "Sự sáng tạo cần được phát triển cho {career}"
        ],
        "dq_safety": [
            "Cần phát triển ý thức bảo mật để phù hợp với {career}",
            "Rèn luyện khả năng đảm bảo an toàn sẽ giúp bạn thành công trong {career}",
            "Kỹ năng bảo mật cần được cải thiện cho {career}"
        ],
        "dq_collaboration": [
            "Cần cải thiện khả năng hợp tác để phù hợp với {career}",
            "Rèn luyện kỹ năng làm việc nhóm sẽ giúp bạn thành công trong {career}",
            "Tinh thần hợp tác cần được phát triển cho {career}"
        ],
        "aq_control": [
            "Cần phát triển khả năng kiểm soát tình huống để phù hợp với {career}",
            "Rèn luyện sự chủ động sẽ giúp bạn thành công trong {career}",
            "Khả năng kiểm soát cần được cải thiện cho {career}"
        ],
        "aq_ownership": [
            "Cần cải thiện tinh thần trách nhiệm để phù hợp với {career}",
            "Rèn luyện sự sở hữu công việc sẽ giúp bạn thành công trong {career}",
            "Tinh thần chủ động cần được phát triển cho {career}"
        ],
        "aq_reach": [
            "Cần phát triển khả năng mở rộng tầm ảnh hưởng để phù hợp với {career}",
            "Rèn luyện tầm nhìn xa sẽ giúp bạn thành công trong {career}",
            "Khả năng tác động tích cực cần được cải thiện cho {career}"
        ],
        "aq_endurance": [
            "Cần cải thiện khả năng kiên trì để phù hợp với {career}",
            "Rèn luyện sự bền bỉ sẽ giúp bạn thành công trong {career}",
            "Tinh thần kiên trì cần được phát triển cho {career}"
        ]
    }
    
    @staticmethod
    def generate_explanation(
        career_name: str,
        profile_scores: List[float],
        weights: Dict[str, float],
        thresholds: Dict[str, float],
        bonus_keys: List[str] = None
    ) -> str:
        """Generate explanation for career suggestion."""
        if not profile_scores or len(profile_scores) != 16:
            return f"Không đủ dữ liệu để đánh giá phù hợp với {career_name}"
        
        # Map profile scores to facet names
        facet_names = [
            'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
            'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
            'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
            'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
        ]
        
        strengths = []
        improvements = []
        
        # Analyze each facet
        for i, score in enumerate(profile_scores):
            if i >= len(facet_names):
                break
                
            facet_name = facet_names[i]
            if facet_name not in weights:
                continue
            
            weight = weights[facet_name]
            threshold = thresholds.get(facet_name, 0)
            
            # Check if meets threshold
            if score >= threshold:
                if weight >= 0.8:  # High importance facet
                    template = random.choice(CareerExplanationGenerator.STRENGTH_TEMPLATES[facet_name])
                    strengths.append(template.format(career=career_name))
            else:
                if weight >= 0.7:  # Important but below threshold
                    template = random.choice(CareerExplanationGenerator.IMPROVEMENT_TEMPLATES[facet_name])
                    improvements.append(template.format(career=career_name))
        
        # Generate explanation
        explanation_parts = []
        
        if strengths:
            explanation_parts.append("Điểm mạnh: " + ". ".join(strengths[:2]))
        
        if improvements:
            explanation_parts.append("Cần cải thiện: " + ". ".join(improvements[:2]))
        
        # Add overall assessment
        total_score = sum(profile_scores)
        avg_score = total_score / len(profile_scores)
        
        if avg_score >= 80:
            explanation_parts.append("Bạn có tiềm năng rất cao để thành công trong nghề này")
        elif avg_score >= 60:
            explanation_parts.append("Bạn có tiềm năng tốt để phát triển trong nghề này")
        elif avg_score >= 40:
            explanation_parts.append("Bạn có thể phát triển để phù hợp với nghề này")
        else:
            explanation_parts.append("Bạn cần đầu tư thời gian để phát triển các kỹ năng cần thiết")
        
        return ". ".join(explanation_parts) + "."
    
    @staticmethod
    def generate_detailed_explanation(
        career_name: str,
        profile_scores: List[float],
        weights: Dict[str, float],
        thresholds: Dict[str, float],
        bonus_keys: List[str] = None
    ) -> Dict[str, any]:
        """Generate detailed explanation with breakdown."""
        if not profile_scores or len(profile_scores) != 16:
            return {
                "summary": f"Không đủ dữ liệu để đánh giá phù hợp với {career_name}",
                "strengths": [],
                "improvements": [],
                "recommendations": []
            }
        
        facet_names = [
            'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
            'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
            'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
            'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
        ]
        
        strengths = []
        improvements = []
        recommendations = []
        
        # Analyze each facet
        for i, score in enumerate(profile_scores):
            if i >= len(facet_names):
                break
                
            facet_name = facet_names[i]
            if facet_name not in weights:
                continue
            
            weight = weights[facet_name]
            threshold = thresholds.get(facet_name, 0)
            
            # Check if meets threshold
            if score >= threshold:
                if weight >= 0.8:  # High importance facet
                    template = random.choice(CareerExplanationGenerator.STRENGTH_TEMPLATES[facet_name])
                    strengths.append({
                        "facet": facet_name,
                        "score": score,
                        "weight": weight,
                        "explanation": template.format(career=career_name)
                    })
            else:
                if weight >= 0.7:  # Important but below threshold
                    template = random.choice(CareerExplanationGenerator.IMPROVEMENT_TEMPLATES[facet_name])
                    improvements.append({
                        "facet": facet_name,
                        "score": score,
                        "threshold": threshold,
                        "weight": weight,
                        "explanation": template.format(career=career_name)
                    })
        
        # Generate recommendations
        if improvements:
            recommendations.append("Tập trung phát triển các kỹ năng còn yếu")
        
        if strengths:
            recommendations.append("Tận dụng điểm mạnh hiện có")
        
        # Overall assessment
        total_score = sum(profile_scores)
        avg_score = total_score / len(profile_scores)
        
        if avg_score >= 80:
            summary = f"Bạn có tiềm năng rất cao để thành công trong {career_name}"
        elif avg_score >= 60:
            summary = f"Bạn có tiềm năng tốt để phát triển trong {career_name}"
        elif avg_score >= 40:
            summary = f"Bạn có thể phát triển để phù hợp với {career_name}"
        else:
            summary = f"Bạn cần đầu tư thời gian để phát triển các kỹ năng cần thiết cho {career_name}"
        
        return {
            "summary": summary,
            "strengths": strengths,
            "improvements": improvements,
            "recommendations": recommendations,
            "overall_score": avg_score
        }