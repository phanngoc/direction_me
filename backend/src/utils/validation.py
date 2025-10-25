"""
Validation utilities for MyWay Career Assessment System.
"""
from typing import List, Dict, Any, Optional
from ..models.question_bank import QuestionBank
from ..schemas import Answer


class AnswerValidator:
    """Validator for assessment answers."""
    
    @staticmethod
    def validate_answers(answers: List[Answer], questions: List[QuestionBank]) -> Dict[str, Any]:
        """
        Validate assessment answers against questions.
        
        Returns:
            Dict with validation results including:
            - is_valid: bool
            - errors: List[str]
            - warnings: List[str]
            - missing_questions: List[str]
            - invalid_answers: List[str]
        """
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'missing_questions': [],
            'invalid_answers': []
        }
        
        if not answers:
            result['errors'].append("No answers provided")
            result['is_valid'] = False
            return result
        
        if not questions:
            result['errors'].append("No questions provided")
            result['is_valid'] = False
            return result
        
        # Create question lookup
        question_lookup = {str(q.id): q for q in questions}
        answer_question_ids = {ans.question_id for ans in answers}
        
        # Check for missing required questions
        required_question_ids = {str(q.id) for q in questions if q.is_active}
        missing_questions = required_question_ids - answer_question_ids
        
        if missing_questions:
            result['missing_questions'] = list(missing_questions)
            result['warnings'].append(f"Missing answers for {len(missing_questions)} questions")
        
        # Validate each answer
        for answer in answers:
            if answer.question_id not in question_lookup:
                result['invalid_answers'].append(f"Unknown question ID: {answer.question_id}")
                result['is_valid'] = False
                continue
            
            question = question_lookup[answer.question_id]
            validation_result = AnswerValidator._validate_single_answer(answer, question)
            
            if not validation_result['is_valid']:
                result['invalid_answers'].extend(validation_result['errors'])
                result['is_valid'] = False
            
            if validation_result['warnings']:
                result['warnings'].extend(validation_result['warnings'])
        
        return result
    
    @staticmethod
    def _validate_single_answer(answer: Answer, question: QuestionBank) -> Dict[str, Any]:
        """Validate a single answer against its question."""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validate answer value
        if not isinstance(answer.answer_value, (int, float)):
            result['errors'].append(f"Answer value must be a number for question {answer.question_id}")
            result['is_valid'] = False
            return result
        
        answer_value = int(answer.answer_value)
        
        # Validate based on question type
        if question.question_type == 'MCQ':
            # For MCQ, answer should be 1-4 (assuming 4 options)
            if not (1 <= answer_value <= 4):
                result['errors'].append(f"MCQ answer must be between 1-4 for question {answer.question_id}")
                result['is_valid'] = False
        
        elif question.question_type == 'Likert':
            # For Likert scale, answer should be 1-5
            if not (1 <= answer_value <= 5):
                result['errors'].append(f"Likert answer must be between 1-5 for question {answer.question_id}")
                result['is_valid'] = False
        
        # Validate answer text if provided
        if answer.answer_text:
            if len(answer.answer_text) > 1000:
                result['warnings'].append(f"Answer text is very long for question {answer.question_id}")
        
        return result
    
    @staticmethod
    def validate_completeness(answers: List[Answer], questions: List[QuestionBank]) -> bool:
        """Check if all required questions are answered."""
        if not answers or not questions:
            return False
        
        answer_question_ids = {ans.question_id for ans in answers}
        required_question_ids = {str(q.id) for q in questions if q.is_active}
        
        return answer_question_ids.issuperset(required_question_ids)
    
    @staticmethod
    def get_validation_summary(validation_result: Dict[str, Any]) -> str:
        """Get a human-readable validation summary."""
        if validation_result['is_valid']:
            summary = "✅ All answers are valid"
            if validation_result['warnings']:
                summary += f" (with {len(validation_result['warnings'])} warnings)"
            return summary
        else:
            error_count = len(validation_result['errors'])
            warning_count = len(validation_result['warnings'])
            return f"❌ {error_count} errors, {warning_count} warnings"


class AssessmentValidator:
    """Validator for assessment data."""
    
    @staticmethod
    def validate_assessment_data(assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate assessment creation data."""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        required_fields = ['user_id']
        for field in required_fields:
            if field not in assessment_data:
                result['errors'].append(f"Missing required field: {field}")
                result['is_valid'] = False
        
        # Validate user_id format (should be UUID)
        if 'user_id' in assessment_data:
            user_id = assessment_data['user_id']
            if not isinstance(user_id, str) or len(user_id) != 36:
                result['warnings'].append("User ID format may be invalid")
        
        return result
    
    @staticmethod
    def validate_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user registration data."""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        required_fields = ['email', 'password', 'full_name', 'age']
        for field in required_fields:
            if field not in user_data:
                result['errors'].append(f"Missing required field: {field}")
                result['is_valid'] = False
        
        # Validate email format
        if 'email' in user_data:
            email = user_data['email']
            if not isinstance(email, str) or '@' not in email:
                result['errors'].append("Invalid email format")
                result['is_valid'] = False
        
        # Validate password strength
        if 'password' in user_data:
            password = user_data['password']
            if not isinstance(password, str) or len(password) < 8:
                result['errors'].append("Password must be at least 8 characters")
                result['is_valid'] = False
        
        # Validate age
        if 'age' in user_data:
            try:
                age = int(user_data['age'])
                if not (16 <= age <= 25):
                    result['errors'].append("Age must be between 16 and 25")
                    result['is_valid'] = False
            except (ValueError, TypeError):
                result['errors'].append("Age must be a valid number")
                result['is_valid'] = False
        
        return result


class ScoreValidator:
    """Validator for calculated scores."""
    
    @staticmethod
    def validate_score_range(score: float, min_val: float = 0, max_val: float = 100) -> bool:
        """Validate that score is within expected range."""
        return min_val <= score <= max_val
    
    @staticmethod
    def validate_scores(scores: Dict[str, float]) -> Dict[str, Any]:
        """Validate multiple scores."""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        for score_name, score_value in scores.items():
            if not isinstance(score_value, (int, float)):
                result['errors'].append(f"Score {score_name} must be a number")
                result['is_valid'] = False
                continue
            
            if not ScoreValidator.validate_score_range(score_value):
                result['errors'].append(f"Score {score_name} ({score_value}) is out of range (0-100)")
                result['is_valid'] = False
        
        return result