from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from models.assessment_question import AssessmentQuestion
from models.assessment_response import AssessmentResponse
import random
from datetime import datetime

class AssessmentQuestionService:
    def __init__(self):
        pass
    
    def get_questions_by_module(self, module: str, db: Session, limit: int = None) -> List[AssessmentQuestion]:
        """Get questions for a specific module (IQ, EQ, DQ, AQ)"""
        try:
            query = db.query(AssessmentQuestion).filter(
                AssessmentQuestion.module == module,
                AssessmentQuestion.is_active == True
            )
            
            if limit:
                query = query.limit(limit)
            
            questions = query.all()
            return questions
            
        except Exception as e:
            raise Exception(f"Failed to get questions for module {module}: {str(e)}")
    
    def get_question_by_id(self, question_id: str, db: Session) -> Optional[AssessmentQuestion]:
        """Get specific question by ID"""
        try:
            return db.query(AssessmentQuestion).filter(
                AssessmentQuestion.id == question_id
            ).first()
        except Exception as e:
            raise Exception(f"Failed to get question {question_id}: {str(e)}")
    
    def get_random_questions(self, module: str, count: int, db: Session) -> List[AssessmentQuestion]:
        """Get random questions for a module"""
        try:
            all_questions = self.get_questions_by_module(module, db)
            
            if len(all_questions) <= count:
                return all_questions
            
            # Randomly select questions
            selected_questions = random.sample(all_questions, count)
            return selected_questions
            
        except Exception as e:
            raise Exception(f"Failed to get random questions: {str(e)}")
    
    def get_questions_by_difficulty(self, module: str, difficulty: int, db: Session) -> List[AssessmentQuestion]:
        """Get questions by difficulty level"""
        try:
            return db.query(AssessmentQuestion).filter(
                AssessmentQuestion.module == module,
                AssessmentQuestion.difficulty == difficulty,
                AssessmentQuestion.is_active == True
            ).all()
        except Exception as e:
            raise Exception(f"Failed to get questions by difficulty: {str(e)}")
    
    def get_assessment_sequence(self, db: Session) -> Dict[str, List[AssessmentQuestion]]:
        """Get complete assessment sequence with questions for all modules"""
        try:
            assessment_sequence = {}
            
            # Define question counts per module
            module_questions = {
                "IQ": 10,  # 10 IQ questions
                "EQ": 15,  # 15 EQ questions  
                "DQ": 12,  # 12 DQ questions
                "AQ": 8    # 8 AQ questions
            }
            
            for module, count in module_questions.items():
                questions = self.get_random_questions(module, count, db)
                assessment_sequence[module] = questions
            
            return assessment_sequence
            
        except Exception as e:
            raise Exception(f"Failed to get assessment sequence: {str(e)}")
    
    def validate_response(self, question: AssessmentQuestion, answer: str, answer_value: int = None) -> Dict[str, Any]:
        """Validate user response to a question"""
        try:
            validation_result = {
                "is_valid": True,
                "score": 0,
                "feedback": ""
            }
            
            if question.question_type == "multiple_choice":
                # For IQ questions - check if answer is correct
                if question.correct_answer:
                    is_correct = answer.strip().lower() == question.correct_answer.lower()
                    validation_result["score"] = 1 if is_correct else 0
                    validation_result["feedback"] = "Đúng!" if is_correct else "Sai. Đáp án đúng là: " + question.correct_answer
                else:
                    validation_result["score"] = 0.5  # Partial credit if no correct answer defined
                    
            elif question.question_type == "likert_scale":
                # For EQ, DQ, AQ questions - validate answer value
                if answer_value is not None and 1 <= answer_value <= 5:
                    # Apply reverse scoring if needed
                    if question.reverse_scored:
                        score = 6 - answer_value
                    else:
                        score = answer_value
                    
                    validation_result["score"] = score
                    validation_result["feedback"] = "Cảm ơn bạn đã trả lời"
                else:
                    validation_result["is_valid"] = False
                    validation_result["feedback"] = "Vui lòng chọn một giá trị từ 1-5"
            
            return validation_result
            
        except Exception as e:
            return {
                "is_valid": False,
                "score": 0,
                "feedback": f"Lỗi xác thực: {str(e)}"
            }
    
    def calculate_module_score(self, module: str, responses: List[AssessmentResponse], db: Session) -> Dict[str, Any]:
        """Calculate score for a specific module"""
        try:
            if not responses:
                return {"score": 0, "max_score": 0, "percentage": 0}
            
            total_score = 0
            max_score = 0
            weighted_score = 0
            total_weight = 0
            
            for response in responses:
                # Get question details
                question = self.get_question_by_id(response.question_id, db)
                if not question or question.module != module:
                    continue
                
                # Calculate score based on question type
                if question.question_type == "multiple_choice":
                    # IQ questions - binary scoring
                    question_score = response.score or 0
                    question_max = 1
                else:
                    # Likert scale questions - use answer_value
                    question_score = response.answer_value or 0
                    question_max = 5
                
                # Apply question weight
                weight = float(question.weight)
                weighted_score += question_score * weight
                total_weight += weight
                max_score += question_max * weight
                total_score += question_score
            
            # Calculate final scores
            if total_weight > 0:
                final_score = weighted_score / total_weight
                final_max = max_score / total_weight
                percentage = (final_score / final_max) * 100 if final_max > 0 else 0
            else:
                final_score = 0
                final_max = 0
                percentage = 0
            
            return {
                "score": round(final_score, 2),
                "max_score": round(final_max, 2),
                "percentage": round(percentage, 2),
                "total_questions": len(responses),
                "module": module
            }
            
        except Exception as e:
            raise Exception(f"Failed to calculate module score: {str(e)}")
    
    def get_question_statistics(self, db: Session) -> Dict[str, Any]:
        """Get statistics about questions in the database"""
        try:
            stats = {}
            
            for module in ["IQ", "EQ", "DQ", "AQ"]:
                total_questions = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.module == module
                ).count()
                
                active_questions = db.query(AssessmentQuestion).filter(
                    AssessmentQuestion.module == module,
                    AssessmentQuestion.is_active == True
                ).count()
                
                stats[module] = {
                    "total": total_questions,
                    "active": active_questions,
                    "inactive": total_questions - active_questions
                }
            
            return stats
            
        except Exception as e:
            raise Exception(f"Failed to get question statistics: {str(e)}")
    
    def create_question(self, module: str, question_text: str, question_type: str, 
                       options: List[Dict] = None, correct_answer: str = None,
                       reverse_scored: bool = False, difficulty: int = 1,
                       weight: float = 1.0, db: Session) -> AssessmentQuestion:
        """Create a new assessment question"""
        try:
            question = AssessmentQuestion(
                module=module,
                question_text=question_text,
                question_type=question_type,
                options=options,
                correct_answer=correct_answer,
                reverse_scored=reverse_scored,
                difficulty=difficulty,
                weight=weight,
                is_active=True
            )
            
            db.add(question)
            db.commit()
            db.refresh(question)
            
            return question
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to create question: {str(e)}")
    
    def update_question(self, question_id: str, updates: Dict[str, Any], db: Session) -> AssessmentQuestion:
        """Update an existing question"""
        try:
            question = self.get_question_by_id(question_id, db)
            if not question:
                raise Exception("Question not found")
            
            for key, value in updates.items():
                if hasattr(question, key):
                    setattr(question, key, value)
            
            db.commit()
            db.refresh(question)
            
            return question
            
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to update question: {str(e)}")
    
    def deactivate_question(self, question_id: str, db: Session) -> bool:
        """Deactivate a question"""
        try:
            question = self.get_question_by_id(question_id, db)
            if question:
                question.is_active = False
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to deactivate question: {str(e)}")
