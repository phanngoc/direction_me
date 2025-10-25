import React from 'react';
import { AssessmentQuestion } from '../../shared/types';

interface QuestionDisplayProps {
  question: AssessmentQuestion;
  questionNumber: number;
  totalQuestions: number;
  className?: string;
}

const QuestionDisplay: React.FC<QuestionDisplayProps> = ({
  question,
  questionNumber,
  totalQuestions,
  className = ''
}) => {
  const formatQuestionText = (text: string) => {
    // Simple formatting for line breaks and emphasis
    return text.split('\n').map((line, index) => (
      <span key={index}>
        {line}
        {index < text.split('\n').length - 1 && <br />}
      </span>
    ));
  };

  const getQuestionTypeInfo = (type: string) => {
    const typeInfo = {
      multiple_choice: {
        name: 'Câu hỏi trắc nghiệm',
        icon: '📝',
        description: 'Chọn một đáp án đúng nhất'
      },
      likert_scale: {
        name: 'Thang đo Likert',
        icon: '📊',
        description: 'Đánh giá mức độ đồng ý từ 1-5'
      }
    };
    return typeInfo[type as keyof typeof typeInfo] || typeInfo.multiple_choice;
  };

  const typeInfo = getQuestionTypeInfo(question.question_type);

  return (
    <div className={`question-display ${className}`}>
      <div className="question-display__header">
        <div className="question-display__meta">
          <span className="question-display__number">
            Câu {questionNumber} / {totalQuestions}
          </span>
          <span className="question-display__type">
            <span className="question-display__type-icon">{typeInfo.icon}</span>
            {typeInfo.name}
          </span>
        </div>
        
        <div className="question-display__difficulty">
          <span className="difficulty-label">
            Độ khó: {getDifficultyStars(question.difficulty)}
          </span>
        </div>
      </div>
      
      <div className="question-display__content">
        <div className="question-display__text">
          {formatQuestionText(question.question_text)}
        </div>
        
        {question.facet && (
          <div className="question-display__facet">
            <span className="facet-label">Khía cạnh: {question.facet}</span>
          </div>
        )}
        
        <div className="question-display__instructions">
          <p className="instruction-text">
            {typeInfo.description}
          </p>
        </div>
      </div>
      
      {question.options && question.options.length > 0 && (
        <div className="question-display__options">
          <h4 className="options-title">Các lựa chọn:</h4>
          <div className="options-list">
            {question.options.map((option, index) => (
              <div key={index} className="option-item">
                <span className="option-key">{option.key}</span>
                <span className="option-value">{option.value}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {question.reverse_scored && (
        <div className="question-display__note">
          <span className="note-icon">⚠️</span>
          <span className="note-text">
            Câu hỏi này được tính điểm ngược. Hãy trả lời cẩn thận.
          </span>
        </div>
      )}
    </div>
  );
};

const getDifficultyStars = (difficulty: number): string => {
  const stars = '★'.repeat(difficulty) + '☆'.repeat(5 - difficulty);
  return stars;
};

export default QuestionDisplay;
