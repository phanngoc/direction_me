from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.assessment_result import AssessmentResult
from models.career_recommendation import CareerRecommendation
import json

class CareerService:
    def __init__(self):
        # Career database - in production, this would be loaded from a database
        self.career_database = self._load_career_database()
    
    def _load_career_database(self) -> List[Dict[str, Any]]:
        """Load career database (placeholder)"""
        return [
            {
                "title": "Lập trình viên Full-stack",
                "description": "Phát triển ứng dụng web và mobile với các công nghệ hiện đại",
                "required_skills": ["JavaScript", "React", "Node.js", "Python", "SQL"],
                "iq_weight": 0.4,
                "eq_weight": 0.2,
                "dq_weight": 0.3,
                "aq_weight": 0.1,
                "market_demand": "high",
                "salary_min": 15000000,
                "salary_max": 35000000
            },
            {
                "title": "Nhà phân tích dữ liệu",
                "description": "Phân tích và diễn giải dữ liệu để đưa ra quyết định kinh doanh",
                "required_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Excel"],
                "iq_weight": 0.5,
                "eq_weight": 0.1,
                "dq_weight": 0.3,
                "aq_weight": 0.1,
                "market_demand": "high",
                "salary_min": 12000000,
                "salary_max": 30000000
            },
            {
                "title": "Quản lý dự án",
                "description": "Lập kế hoạch, điều phối và quản lý các dự án trong tổ chức",
                "required_skills": ["Leadership", "Communication", "Planning", "Risk Management"],
                "iq_weight": 0.2,
                "eq_weight": 0.4,
                "dq_weight": 0.2,
                "aq_weight": 0.2,
                "market_demand": "medium",
                "salary_min": 18000000,
                "salary_max": 40000000
            },
            {
                "title": "Chuyên viên Marketing Digital",
                "description": "Phát triển và thực hiện các chiến lược marketing trực tuyến",
                "required_skills": ["Digital Marketing", "SEO", "Social Media", "Analytics", "Content Creation"],
                "iq_weight": 0.2,
                "eq_weight": 0.3,
                "dq_weight": 0.4,
                "aq_weight": 0.1,
                "market_demand": "high",
                "salary_min": 10000000,
                "salary_max": 25000000
            },
            {
                "title": "Nhà tư vấn tâm lý",
                "description": "Hỗ trợ và tư vấn cho các cá nhân về các vấn đề tâm lý và cảm xúc",
                "required_skills": ["Psychology", "Communication", "Empathy", "Active Listening"],
                "iq_weight": 0.1,
                "eq_weight": 0.6,
                "dq_weight": 0.1,
                "aq_weight": 0.2,
                "market_demand": "medium",
                "salary_min": 8000000,
                "salary_max": 20000000
            }
        ]
    
    def generate_recommendations(self, result: AssessmentResult, db: Session) -> List[CareerRecommendation]:
        """Generate career recommendations based on assessment results"""
        recommendations = []
        
        # Calculate alignment scores for each career
        for career_data in self.career_database:
            alignment_score = self._calculate_alignment_score(result, career_data)
            
            if alignment_score > 0.3:  # Only recommend careers with decent alignment
                recommendation = CareerRecommendation(
                    result_id=result.id,
                    user_id=result.user_id,
                    career_title=career_data["title"],
                    career_description=career_data["description"],
                    alignment_score=alignment_score,
                    required_skills=career_data["required_skills"],
                    market_demand=career_data["market_demand"],
                    salary_range_min=career_data["salary_min"],
                    salary_range_max=career_data["salary_max"],
                    priority_rank=self._calculate_priority_rank(alignment_score, career_data),
                    explanation=self._generate_explanation(result, career_data, alignment_score)
                )
                recommendations.append(recommendation)
        
        # Sort by priority rank
        recommendations.sort(key=lambda x: x.priority_rank)
        
        # Limit to top 3 recommendations
        return recommendations[:3]
    
    def _calculate_alignment_score(self, result: AssessmentResult, career_data: Dict[str, Any]) -> float:
        """Calculate alignment score between user profile and career"""
        # Normalize scores to 0-1 range
        iq_score = result.iq_score / 100.0
        eq_score = result.eq_score / 100.0
        dq_score = result.dq_score / 100.0
        aq_score = result.aq_score / 100.0
        
        # Calculate weighted alignment
        alignment = (
            iq_score * career_data["iq_weight"] +
            eq_score * career_data["eq_weight"] +
            dq_score * career_data["dq_weight"] +
            aq_score * career_data["aq_weight"]
        )
        
        return round(alignment * 100, 2)  # Convert to percentage
    
    def _calculate_priority_rank(self, alignment_score: float, career_data: Dict[str, Any]) -> int:
        """Calculate priority rank for recommendation"""
        # Base rank on alignment score
        if alignment_score >= 80:
            return 1
        elif alignment_score >= 60:
            return 2
        else:
            return 3
    
    def _generate_explanation(self, result: AssessmentResult, career_data: Dict[str, Any], alignment_score: float) -> str:
        """Generate explanation for why this career is recommended"""
        strongest_quotient = result.strongest_quotient
        career_name = career_data["title"]
        
        explanations = {
            "IQ": f"Dựa trên kết quả đánh giá, bạn có khả năng tư duy logic cao, phù hợp với {career_name} - một nghề đòi hỏi khả năng phân tích và giải quyết vấn đề.",
            "EQ": f"Với chỉ số cảm xúc cao, bạn có khả năng hiểu và quản lý cảm xúc tốt, rất phù hợp với {career_name} - một nghề cần sự đồng cảm và giao tiếp.",
            "DQ": f"Khả năng số hóa mạnh của bạn rất phù hợp với {career_name} - một nghề trong thời đại công nghệ số.",
            "AQ": f"Khả năng thích nghi cao của bạn giúp bạn dễ dàng học hỏi và phát triển trong {career_name} - một nghề luôn thay đổi và phát triển."
        }
        
        base_explanation = explanations.get(strongest_quotient, f"Kết quả đánh giá cho thấy bạn phù hợp với {career_name}.")
        
        return f"{base_explanation} Điểm phù hợp: {alignment_score}%."
    
    def get_career_insights(self, result: AssessmentResult) -> Dict[str, Any]:
        """Get insights about user's career potential"""
        insights = {
            "strongest_quotient": result.strongest_quotient,
            "weakest_quotient": result.weakest_quotient,
            "career_advice": self._generate_career_advice(result),
            "development_areas": self._identify_development_areas(result)
        }
        
        return insights
    
    def _generate_career_advice(self, result: AssessmentResult) -> str:
        """Generate career advice based on results"""
        strongest = result.strongest_quotient
        weakest = result.weakest_quotient
        
        advice_map = {
            "IQ": "Bạn có khả năng tư duy logic mạnh, phù hợp với các nghề đòi hỏi phân tích, nghiên cứu và giải quyết vấn đề phức tạp.",
            "EQ": "Khả năng cảm xúc cao giúp bạn phù hợp với các nghề liên quan đến con người như tư vấn, giáo dục, quản lý nhân sự.",
            "DQ": "Khả năng số hóa mạnh mở ra nhiều cơ hội trong lĩnh vực công nghệ, marketing digital và chuyển đổi số.",
            "AQ": "Khả năng thích nghi cao giúp bạn dễ dàng học hỏi và phát triển trong môi trường thay đổi nhanh."
        }
        
        return advice_map.get(strongest, "Dựa trên kết quả đánh giá, bạn có tiềm năng phát triển trong nhiều lĩnh vực khác nhau.")
    
    def _identify_development_areas(self, result: AssessmentResult) -> List[str]:
        """Identify areas for development"""
        areas = []
        
        if result.iq_score < 70:
            areas.append("Phát triển khả năng tư duy logic và phân tích")
        if result.eq_score < 70:
            areas.append("Cải thiện khả năng quản lý cảm xúc và giao tiếp")
        if result.dq_score < 70:
            areas.append("Nâng cao kỹ năng số hóa và công nghệ")
        if result.aq_score < 70:
            areas.append("Rèn luyện khả năng thích nghi và học hỏi")
        
        return areas
