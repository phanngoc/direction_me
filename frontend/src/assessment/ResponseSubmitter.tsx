import React, { useState, useEffect, useRef } from 'react';
import { AssessmentQuestion, AssessmentResponse } from '../../shared/types';

interface ResponseSubmitterProps {
  question: AssessmentQuestion;
  onSubmit: (response: Partial<AssessmentResponse>) => void;
  isSubmitting?: boolean;
  className?: string;
}

const ResponseSubmitter: React.FC<ResponseSubmitterProps> = ({
  question,
  onSubmit,
  isSubmitting = false,
  className = ''
}) => {
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [selectedValue, setSelectedValue] = useState<number | null>(null);
  const [responseTime, setResponseTime] = useState<number>(0);
  const [isValid, setIsValid] = useState<boolean>(false);
  
  const startTimeRef = useRef<number>(Date.now());
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Start timing when component mounts
  useEffect(() => {
    startTimeRef.current = Date.now();
    
    intervalRef.current = setInterval(() => {
      setResponseTime(Math.floor((Date.now() - startTimeRef.current) / 1000));
    }, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [question.id]);

  // Validate response based on question type
  useEffect(() => {
    if (question.question_type === 'multiple_choice') {
      setIsValid(selectedAnswer.trim() !== '');
    } else if (question.question_type === 'likert_scale') {
      setIsValid(selectedValue !== null && selectedValue >= 1 && selectedValue <= 5);
    }
  }, [selectedAnswer, selectedValue, question.question_type]);

  const handleSubmit = () => {
    if (!isValid || isSubmitting) return;

    const response: Partial<AssessmentResponse> = {
      answer: selectedAnswer,
      answer_value: selectedValue,
      response_time_seconds: responseTime
    };

    onSubmit(response);
  };

  const handleMultipleChoiceSelect = (answer: string) => {
    setSelectedAnswer(answer);
  };

  const handleLikertScaleSelect = (value: number) => {
    setSelectedValue(value);
  };

  const getLikertScaleLabels = () => {
    return [
      { value: 1, label: 'Hoàn toàn không đồng ý', color: '#EF4444' },
      { value: 2, label: 'Không đồng ý', color: '#F97316' },
      { value: 3, label: 'Trung lập', color: '#EAB308' },
      { value: 4, label: 'Đồng ý', color: '#22C55E' },
      { value: 5, label: 'Hoàn toàn đồng ý', color: '#10B981' }
    ];
  };

  if (question.question_type === 'multiple_choice') {
    return (
      <div className={`response-submitter ${className}`}>
        <div className="response-submitter__options">
          {question.options?.map((option, index) => (
            <button
              key={index}
              className={`option-button ${selectedAnswer === option.key ? 'selected' : ''}`}
              onClick={() => handleMultipleChoiceSelect(option.key)}
              disabled={isSubmitting}
            >
              <span className="option-key">{option.key}</span>
              <span className="option-value">{option.value}</span>
            </button>
          ))}
        </div>
        
        <div className="response-submitter__actions">
          <button
            className="submit-button"
            onClick={handleSubmit}
            disabled={!isValid || isSubmitting}
          >
            {isSubmitting ? 'Đang gửi...' : 'Gửi câu trả lời'}
          </button>
        </div>
      </div>
    );
  }

  if (question.question_type === 'likert_scale') {
    const likertOptions = getLikertScaleLabels();
    
    return (
      <div className={`response-submitter ${className}`}>
        <div className="response-submitter__likert">
          <div className="likert-scale">
            {likertOptions.map((option) => (
              <button
                key={option.value}
                className={`likert-option ${selectedValue === option.value ? 'selected' : ''}`}
                onClick={() => handleLikertScaleSelect(option.value)}
                disabled={isSubmitting}
                style={{ 
                  borderColor: selectedValue === option.value ? option.color : '#E5E7EB',
                  backgroundColor: selectedValue === option.value ? option.color + '20' : 'transparent'
                }}
              >
                <span className="likert-value">{option.value}</span>
                <span className="likert-label">{option.label}</span>
              </button>
            ))}
          </div>
        </div>
        
        <div className="response-submitter__actions">
          <button
            className="submit-button"
            onClick={handleSubmit}
            disabled={!isValid || isSubmitting}
          >
            {isSubmitting ? 'Đang gửi...' : 'Gửi câu trả lời'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`response-submitter ${className}`}>
      <div className="response-submitter__error">
        <p>Loại câu hỏi không được hỗ trợ: {question.question_type}</p>
      </div>
    </div>
  );
};

export default ResponseSubmitter;
