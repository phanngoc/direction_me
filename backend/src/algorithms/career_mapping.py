"""
Career mapping algorithm for MyWay Career Assessment System.
"""
from typing import Dict, List, Tuple, Optional
import json
import os
from ..models.profile_vector import ProfileVector
from ..models.career_rule import CareerRule


class CareerMappingAlgorithm:
    """Algorithm for mapping profile vectors to career suggestions."""
    
    # Default career rules if not loaded from database
    DEFAULT_CAREER_RULES = {
        "Software Engineer": {
            "weights": {
                "iq_lr": 0.9, "iq_nr": 0.8, "iq_vr": 0.7, "iq_sr": 0.8,
                "eq_empathy": 0.5, "eq_social": 0.6, "eq_self_awareness": 0.7, "eq_self_regulation": 0.8,
                "dq_info_literacy": 0.9, "dq_creativity": 0.8, "dq_safety": 0.7, "dq_collaboration": 0.8,
                "aq_control": 0.8, "aq_ownership": 0.9, "aq_reach": 0.6, "aq_endurance": 0.7
            },
            "thresholds": {
                "iq_lr": 60, "iq_nr": 60, "iq_vr": 50, "iq_sr": 60,
                "eq_empathy": 40, "eq_social": 50, "eq_self_awareness": 60, "eq_self_regulation": 60,
                "dq_info_literacy": 70, "dq_creativity": 60, "dq_safety": 50, "dq_collaboration": 60,
                "aq_control": 60, "aq_ownership": 70, "aq_reach": 40, "aq_endurance": 50
            },
            "bonus_keys": ["iq_lr", "iq_nr", "dq_info_literacy", "aq_ownership"]
        },
        "Data Scientist": {
            "weights": {
                "iq_lr": 0.9, "iq_nr": 0.9, "iq_vr": 0.6, "iq_sr": 0.7,
                "eq_empathy": 0.4, "eq_social": 0.5, "eq_self_awareness": 0.8, "eq_self_regulation": 0.8,
                "dq_info_literacy": 0.9, "dq_creativity": 0.7, "dq_safety": 0.8, "dq_collaboration": 0.6,
                "aq_control": 0.7, "aq_ownership": 0.8, "aq_reach": 0.5, "aq_endurance": 0.8
            },
            "thresholds": {
                "iq_lr": 70, "iq_nr": 80, "iq_vr": 50, "iq_sr": 50,
                "eq_empathy": 30, "eq_social": 40, "eq_self_awareness": 70, "eq_self_regulation": 70,
                "dq_info_literacy": 80, "dq_creativity": 50, "dq_safety": 70, "dq_collaboration": 50,
                "aq_control": 60, "aq_ownership": 70, "aq_reach": 40, "aq_endurance": 70
            },
            "bonus_keys": ["iq_nr", "dq_info_literacy", "aq_endurance"]
        },
        "UX Designer": {
            "weights": {
                "iq_lr": 0.6, "iq_nr": 0.5, "iq_vr": 0.8, "iq_sr": 0.8,
                "eq_empathy": 0.9, "eq_social": 0.8, "eq_self_awareness": 0.8, "eq_self_regulation": 0.7,
                "dq_info_literacy": 0.7, "dq_creativity": 0.9, "dq_safety": 0.6, "dq_collaboration": 0.8,
                "aq_control": 0.6, "aq_ownership": 0.7, "aq_reach": 0.7, "aq_endurance": 0.6
            },
            "thresholds": {
                "iq_lr": 50, "iq_nr": 40, "iq_vr": 60, "iq_sr": 60,
                "eq_empathy": 80, "eq_social": 70, "eq_self_awareness": 70, "eq_self_regulation": 60,
                "dq_info_literacy": 60, "dq_creativity": 80, "dq_safety": 40, "dq_collaboration": 70,
                "aq_control": 50, "aq_ownership": 60, "aq_reach": 60, "aq_endurance": 50
            },
            "bonus_keys": ["eq_empathy", "dq_creativity", "eq_social"]
        },
        "Marketing Manager": {
            "weights": {
                "iq_lr": 0.7, "iq_nr": 0.6, "iq_vr": 0.8, "iq_sr": 0.5,
                "eq_empathy": 0.8, "eq_social": 0.9, "eq_self_awareness": 0.7, "eq_self_regulation": 0.7,
                "dq_info_literacy": 0.8, "dq_creativity": 0.8, "dq_safety": 0.6, "dq_collaboration": 0.9,
                "aq_control": 0.7, "aq_ownership": 0.8, "aq_reach": 0.8, "aq_endurance": 0.7
            },
            "thresholds": {
                "iq_lr": 60, "iq_nr": 50, "iq_vr": 70, "iq_sr": 40,
                "eq_empathy": 70, "eq_social": 80, "eq_self_awareness": 60, "eq_self_regulation": 60,
                "dq_info_literacy": 70, "dq_creativity": 70, "dq_safety": 50, "dq_collaboration": 80,
                "aq_control": 60, "aq_ownership": 70, "aq_reach": 70, "aq_endurance": 60
            },
            "bonus_keys": ["eq_social", "dq_creativity", "aq_reach"]
        },
        "Financial Analyst": {
            "weights": {
                "iq_lr": 0.8, "iq_nr": 0.9, "iq_vr": 0.7, "iq_sr": 0.6,
                "eq_empathy": 0.4, "eq_social": 0.5, "eq_self_awareness": 0.8, "eq_self_regulation": 0.9,
                "dq_info_literacy": 0.8, "dq_creativity": 0.5, "dq_safety": 0.9, "dq_collaboration": 0.6,
                "aq_control": 0.8, "aq_ownership": 0.9, "aq_reach": 0.5, "aq_endurance": 0.8
            },
            "thresholds": {
                "iq_lr": 70, "iq_nr": 80, "iq_vr": 60, "iq_sr": 50,
                "eq_empathy": 30, "eq_social": 40, "eq_self_awareness": 70, "eq_self_regulation": 80,
                "dq_info_literacy": 70, "dq_creativity": 40, "dq_safety": 80, "dq_collaboration": 50,
                "aq_control": 70, "aq_ownership": 80, "aq_reach": 40, "aq_endurance": 70
            },
            "bonus_keys": ["iq_nr", "dq_safety", "aq_ownership"]
        },
        "Project Manager": {
            "weights": {
                "iq_lr": 0.8, "iq_nr": 0.6, "iq_vr": 0.8, "iq_sr": 0.6,
                "eq_empathy": 0.7, "eq_social": 0.8, "eq_self_awareness": 0.8, "eq_self_regulation": 0.8,
                "dq_info_literacy": 0.7, "dq_creativity": 0.6, "dq_safety": 0.7, "dq_collaboration": 0.9,
                "aq_control": 0.8, "aq_ownership": 0.8, "aq_reach": 0.7, "aq_endurance": 0.8
            },
            "thresholds": {
                "iq_lr": 70, "iq_nr": 50, "iq_vr": 70, "iq_sr": 50,
                "eq_empathy": 60, "eq_social": 70, "eq_self_awareness": 70, "eq_self_regulation": 70,
                "dq_info_literacy": 60, "dq_creativity": 50, "dq_safety": 60, "dq_collaboration": 80,
                "aq_control": 70, "aq_ownership": 70, "aq_reach": 60, "aq_endurance": 70
            },
            "bonus_keys": ["eq_social", "dq_collaboration", "aq_control"]
        },
        "Content Creator": {
            "weights": {
                "iq_lr": 0.6, "iq_nr": 0.5, "iq_vr": 0.9, "iq_sr": 0.7,
                "eq_empathy": 0.8, "eq_social": 0.8, "eq_self_awareness": 0.8, "eq_self_regulation": 0.7,
                "dq_info_literacy": 0.8, "dq_creativity": 0.9, "dq_safety": 0.6, "dq_collaboration": 0.7,
                "aq_control": 0.6, "aq_ownership": 0.8, "aq_reach": 0.8, "aq_endurance": 0.7
            },
            "thresholds": {
                "iq_lr": 50, "iq_nr": 40, "iq_vr": 80, "iq_sr": 60,
                "eq_empathy": 70, "eq_social": 70, "eq_self_awareness": 70, "eq_self_regulation": 60,
                "dq_info_literacy": 70, "dq_creativity": 80, "dq_safety": 50, "dq_collaboration": 60,
                "aq_control": 50, "aq_ownership": 70, "aq_reach": 70, "aq_endurance": 60
            },
            "bonus_keys": ["iq_vr", "dq_creativity", "aq_reach"]
        },
        "Entrepreneur": {
            "weights": {
                "iq_lr": 0.8, "iq_nr": 0.7, "iq_vr": 0.8, "iq_sr": 0.7,
                "eq_empathy": 0.7, "eq_social": 0.8, "eq_self_awareness": 0.9, "eq_self_regulation": 0.8,
                "dq_info_literacy": 0.8, "dq_creativity": 0.9, "dq_safety": 0.6, "dq_collaboration": 0.7,
                "aq_control": 0.8, "aq_ownership": 0.9, "aq_reach": 0.9, "aq_endurance": 0.8
            },
            "thresholds": {
                "iq_lr": 70, "iq_nr": 60, "iq_vr": 70, "iq_sr": 60,
                "eq_empathy": 60, "eq_social": 70, "eq_self_awareness": 80, "eq_self_regulation": 70,
                "dq_info_literacy": 70, "dq_creativity": 80, "dq_safety": 50, "dq_collaboration": 60,
                "aq_control": 70, "aq_ownership": 80, "aq_reach": 80, "aq_endurance": 70
            },
            "bonus_keys": ["eq_self_awareness", "dq_creativity", "aq_ownership", "aq_reach"]
        }
    }
    
    @staticmethod
    def calculate_career_fit_scores(profile_vector: ProfileVector, career_rules: List[CareerRule] = None) -> List[Dict[str, any]]:
        """
        Calculate career fit scores for all careers.
        
        Returns:
            List of career suggestions sorted by fit score (highest first)
        """
        if career_rules is None:
            # Use default rules
            career_rules = CareerMappingAlgorithm._load_default_rules()
        
        profile_scores = profile_vector.to_vector()
        career_suggestions = []
        
        for rule in career_rules:
            if not rule.is_active:
                continue
                
            fit_score = CareerMappingAlgorithm._calculate_career_fit_score(
                profile_scores, rule
            )
            
            # Only include careers that meet minimum threshold
            if fit_score >= 30:  # Minimum 30% fit
                career_suggestions.append({
                    'career_name': rule.career_name,
                    'fit_score': fit_score,
                    'explanation': CareerMappingAlgorithm._generate_explanation(
                        profile_scores, rule, fit_score
                    )
                })
        
        # Sort by fit score (highest first) and limit to top 8
        career_suggestions.sort(key=lambda x: x['fit_score'], reverse=True)
        return career_suggestions[:8]
    
    @staticmethod
    def _calculate_career_fit_score(profile_scores: List[float], rule: CareerRule) -> float:
        """Calculate fit score for a specific career."""
        weights = rule.weights
        thresholds = rule.thresholds
        bonus_keys = rule.bonus_keys or []
        
        total_weighted_score = 0.0
        total_weight = 0.0
        bonus_points = 0.0
        
        # Map profile scores to facet names
        facet_names = [
            'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
            'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
            'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
            'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
        ]
        
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
                # Calculate weighted score
                weighted_score = score * weight
                total_weighted_score += weighted_score
                total_weight += weight
                
                # Add bonus points for key facets
                if facet_name in bonus_keys and score >= threshold + 10:
                    bonus_points += 5.0  # 5 bonus points for exceeding threshold by 10+
            else:
                # Penalty for not meeting threshold
                penalty = (threshold - score) * 0.1
                total_weighted_score -= penalty
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        # Calculate base fit score
        base_score = (total_weighted_score / total_weight) + bonus_points
        
        # Normalize to 0-100 range
        fit_score = max(0, min(100, base_score))
        
        return round(fit_score, 2)
    
    @staticmethod
    def _generate_explanation(profile_scores: List[float], rule: CareerRule, fit_score: float) -> str:
        """Generate explanation for career suggestion."""
        facet_names = [
            'iq_lr', 'iq_nr', 'iq_vr', 'iq_sr',
            'eq_empathy', 'eq_social', 'eq_self_awareness', 'eq_self_regulation',
            'dq_info_literacy', 'dq_creativity', 'dq_safety', 'dq_collaboration',
            'aq_control', 'aq_ownership', 'aq_reach', 'aq_endurance'
        ]
        
        strengths = []
        areas_for_improvement = []
        
        for i, score in enumerate(profile_scores):
            if i >= len(facet_names):
                break
                
            facet_name = facet_names[i]
            if facet_name not in rule.weights:
                continue
            
            threshold = rule.thresholds.get(facet_name, 0)
            weight = rule.weights[facet_name]
            
            if score >= threshold:
                if weight >= 0.8:  # High importance facet
                    strengths.append(facet_name)
            else:
                if weight >= 0.7:  # Important but below threshold
                    areas_for_improvement.append(facet_name)
        
        explanation_parts = []
        
        if strengths:
            explanation_parts.append(f"Điểm mạnh: {', '.join(strengths[:3])}")
        
        if areas_for_improvement:
            explanation_parts.append(f"Cần cải thiện: {', '.join(areas_for_improvement[:2])}")
        
        if fit_score >= 80:
            explanation_parts.append("Phù hợp rất cao với nghề nghiệp này")
        elif fit_score >= 60:
            explanation_parts.append("Phù hợp tốt với nghề nghiệp này")
        elif fit_score >= 40:
            explanation_parts.append("Có tiềm năng phù hợp với nghề nghiệp này")
        else:
            explanation_parts.append("Cần phát triển thêm để phù hợp với nghề nghiệp này")
        
        return ". ".join(explanation_parts) + "."
    
    @staticmethod
    def _load_default_rules() -> List[CareerRule]:
        """Load default career rules."""
        rules = []
        for career_name, rule_data in CareerMappingAlgorithm.DEFAULT_CAREER_RULES.items():
            rule = CareerRule(
                career_name=career_name,
                weights=rule_data["weights"],
                thresholds=rule_data["thresholds"],
                bonus_keys=rule_data.get("bonus_keys", []),
                is_active=True
            )
            rules.append(rule)
        return rules
    
    @staticmethod
    def get_career_requirements(career_name: str) -> Dict[str, any]:
        """Get detailed requirements for a specific career."""
        if career_name in CareerMappingAlgorithm.DEFAULT_CAREER_RULES:
            rule_data = CareerMappingAlgorithm.DEFAULT_CAREER_RULES[career_name]
            return {
                "career_name": career_name,
                "description": CareerMappingAlgorithm._get_career_description(career_name),
                "key_skills": CareerMappingAlgorithm._get_key_skills(career_name),
                "education_requirements": CareerMappingAlgorithm._get_education_requirements(career_name),
                "experience_level": CareerMappingAlgorithm._get_experience_level(career_name),
                "salary_range": CareerMappingAlgorithm._get_salary_range(career_name),
                "growth_outlook": CareerMappingAlgorithm._get_growth_outlook(career_name)
            }
        return {}
    
    @staticmethod
    def _get_career_description(career_name: str) -> str:
        """Get career description."""
        descriptions = {
            "Software Engineer": "Phát triển và duy trì các ứng dụng phần mềm, hệ thống và nền tảng công nghệ.",
            "Data Scientist": "Phân tích dữ liệu lớn để tìm ra insights và hỗ trợ ra quyết định kinh doanh.",
            "UX Designer": "Thiết kế trải nghiệm người dùng để tạo ra sản phẩm dễ sử dụng và hấp dẫn.",
            "Marketing Manager": "Lập kế hoạch và thực hiện các chiến lược marketing để tăng doanh số.",
            "Financial Analyst": "Phân tích tài chính và đưa ra khuyến nghị đầu tư cho doanh nghiệp.",
            "Project Manager": "Quản lý và điều phối các dự án để đảm bảo hoàn thành đúng thời hạn và ngân sách.",
            "Content Creator": "Tạo ra nội dung sáng tạo cho các nền tảng digital và social media.",
            "Entrepreneur": "Khởi nghiệp và phát triển các ý tưởng kinh doanh mới."
        }
        return descriptions.get(career_name, "Mô tả nghề nghiệp không có sẵn")
    
    @staticmethod
    def _get_key_skills(career_name: str) -> List[str]:
        """Get key skills for career."""
        skills_map = {
            "Software Engineer": ["Lập trình", "Thuật toán", "Cơ sở dữ liệu", "Git", "Testing"],
            "Data Scientist": ["Python/R", "Machine Learning", "Statistics", "SQL", "Data Visualization"],
            "UX Designer": ["User Research", "Wireframing", "Prototyping", "Figma", "Usability Testing"],
            "Marketing Manager": ["Digital Marketing", "Analytics", "Content Strategy", "SEO/SEM", "Social Media"],
            "Financial Analyst": ["Financial Modeling", "Excel", "SQL", "Statistics", "Risk Assessment"],
            "Project Manager": ["Agile/Scrum", "Risk Management", "Communication", "Leadership", "Planning"],
            "Content Creator": ["Writing", "Video Editing", "Social Media", "Photography", "Storytelling"],
            "Entrepreneur": ["Leadership", "Strategic Thinking", "Risk Management", "Networking", "Innovation"]
        }
        return skills_map.get(career_name, [])
    
    @staticmethod
    def _get_education_requirements(career_name: str) -> str:
        """Get education requirements."""
        education_map = {
            "Software Engineer": "Cử nhân Khoa học Máy tính hoặc tương đương",
            "Data Scientist": "Cử nhân Toán học, Thống kê, hoặc Khoa học Máy tính",
            "UX Designer": "Cử nhân Thiết kế, Tâm lý học, hoặc tương đương",
            "Marketing Manager": "Cử nhân Marketing, Kinh doanh, hoặc tương đương",
            "Financial Analyst": "Cử nhân Tài chính, Kinh tế, hoặc Kế toán",
            "Project Manager": "Cử nhân Quản trị Kinh doanh hoặc tương đương",
            "Content Creator": "Không yêu cầu bằng cấp cụ thể, tập trung vào portfolio",
            "Entrepreneur": "Không yêu cầu bằng cấp cụ thể, tập trung vào kinh nghiệm"
        }
        return education_map.get(career_name, "Yêu cầu học vấn không xác định")
    
    @staticmethod
    def _get_experience_level(career_name: str) -> str:
        """Get experience level."""
        experience_map = {
            "Software Engineer": "0-2 năm (Junior), 3-5 năm (Mid), 5+ năm (Senior)",
            "Data Scientist": "1-3 năm (Junior), 3-6 năm (Mid), 6+ năm (Senior)",
            "UX Designer": "0-2 năm (Junior), 2-5 năm (Mid), 5+ năm (Senior)",
            "Marketing Manager": "2-4 năm (Junior), 4-7 năm (Mid), 7+ năm (Senior)",
            "Financial Analyst": "0-2 năm (Junior), 2-5 năm (Mid), 5+ năm (Senior)",
            "Project Manager": "1-3 năm (Junior), 3-6 năm (Mid), 6+ năm (Senior)",
            "Content Creator": "Portfolio-based, không yêu cầu kinh nghiệm cụ thể",
            "Entrepreneur": "Kinh nghiệm trong lĩnh vực liên quan, không yêu cầu cụ thể"
        }
        return experience_map.get(career_name, "Yêu cầu kinh nghiệm không xác định")
    
    @staticmethod
    def _get_salary_range(career_name: str) -> str:
        """Get salary range (VND per month)."""
        salary_map = {
            "Software Engineer": "15-50 triệu VND/tháng",
            "Data Scientist": "20-60 triệu VND/tháng",
            "UX Designer": "12-40 triệu VND/tháng",
            "Marketing Manager": "15-45 triệu VND/tháng",
            "Financial Analyst": "12-35 triệu VND/tháng",
            "Project Manager": "15-50 triệu VND/tháng",
            "Content Creator": "5-30 triệu VND/tháng (tùy thuộc vào thành công)",
            "Entrepreneur": "Không cố định, phụ thuộc vào thành công của startup"
        }
        return salary_map.get(career_name, "Mức lương không xác định")
    
    @staticmethod
    def _get_growth_outlook(career_name: str) -> str:
        """Get growth outlook."""
        outlook_map = {
            "Software Engineer": "Tăng trưởng mạnh, nhu cầu cao",
            "Data Scientist": "Tăng trưởng rất mạnh, thiếu nhân lực",
            "UX Designer": "Tăng trưởng tốt, nhu cầu ổn định",
            "Marketing Manager": "Tăng trưởng ổn định, cạnh tranh cao",
            "Financial Analyst": "Tăng trưởng ổn định, yêu cầu chuyên môn cao",
            "Project Manager": "Tăng trưởng tốt, nhu cầu đa dạng",
            "Content Creator": "Tăng trưởng mạnh, cơ hội lớn",
            "Entrepreneur": "Rủi ro cao, tiềm năng lợi nhuận lớn"
        }
        return outlook_map.get(career_name, "Triển vọng không xác định")