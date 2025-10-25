#!/usr/bin/env python3
"""
Assessment Question Data Loader

This script loads assessment questions from data_question.md format
into the database for the chatbot assessment interface.
"""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.connection import SessionLocal, engine
from models.assessment_question import AssessmentQuestion
from models import Base

def load_questions_from_file(file_path: str):
    """Load questions from data_question.md file"""
    questions = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the markdown content
        # This is a simplified parser - in production, you'd want a more robust parser
        sections = content.split('## ')
        
        for section in sections[1:]:  # Skip the first empty section
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            module = lines[0].strip()
            if module not in ['IQ', 'EQ', 'DQ', 'AQ']:
                continue
            
            # Parse questions in this module
            current_question = None
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('**Q'):
                    # Save previous question if exists
                    if current_question:
                        questions.append(current_question)
                    
                    # Start new question
                    current_question = {
                        'module': module,
                        'question_text': line.replace('**Q:**', '').strip(),
                        'question_type': 'multiple_choice' if module == 'IQ' else 'likert_scale',
                        'options': [],
                        'correct_answer': None,
                        'reverse_scored': module != 'IQ',
                        'difficulty': 1,
                        'weight': 1.0,
                        'is_active': True
                    }
                
                elif line.startswith('**A:') and current_question:
                    # Answer options
                    options_text = line.replace('**A:**', '').strip()
                    if module == 'IQ':
                        # Parse multiple choice options
                        options = [opt.strip() for opt in options_text.split(',')]
                        current_question['options'] = options
                    else:
                        # Likert scale options
                        current_question['options'] = ['Hoàn toàn không đồng ý', 'Không đồng ý', 'Trung lập', 'Đồng ý', 'Hoàn toàn đồng ý']
                
                elif line.startswith('**Đáp án:') and current_question:
                    # Correct answer for IQ questions
                    if module == 'IQ':
                        current_question['correct_answer'] = line.replace('**Đáp án:**', '').strip()
                
                elif line.startswith('**Giải thích:') and current_question:
                    # Add explanation to question text
                    explanation = line.replace('**Giải thích:**', '').strip()
                    current_question['question_text'] += f" (Giải thích: {explanation})"
            
            # Save last question
            if current_question:
                questions.append(current_question)
    
    except Exception as e:
        print(f"Error loading questions from file: {e}")
        return []
    
    return questions

def load_questions_to_database(questions: list):
    """Load questions into database"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        for question_data in questions:
            # Check if question already exists
            existing = db.query(AssessmentQuestion).filter(
                AssessmentQuestion.question_text == question_data['question_text']
            ).first()
            
            if existing:
                print(f"Question already exists: {question_data['question_text'][:50]}...")
                continue
            
            # Create new question
            question = AssessmentQuestion(**question_data)
            db.add(question)
            print(f"Added question: {question_data['question_text'][:50]}...")
        
        db.commit()
        print(f"Successfully loaded {len(questions)} questions")
        
    except Exception as e:
        print(f"Error loading questions to database: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function"""
    # Get data_question.md path
    project_root = Path(__file__).parent.parent.parent.parent
    data_file = project_root / "data_question.md"
    
    if not data_file.exists():
        print(f"Data file not found: {data_file}")
        print("Please ensure data_question.md exists in the project root")
        return
    
    print(f"Loading questions from: {data_file}")
    
    # Load questions from file
    questions = load_questions_from_file(str(data_file))
    
    if not questions:
        print("No questions found to load")
        return
    
    print(f"Found {len(questions)} questions")
    
    # Load questions to database
    load_questions_to_database(questions)

if __name__ == "__main__":
    main()
