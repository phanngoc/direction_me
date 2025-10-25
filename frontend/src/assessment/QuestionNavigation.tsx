import React from 'react';

interface QuestionNavigationProps {
  currentIndex: number;
  totalQuestions: number;
  onPrevious: () => void;
  onNext: () => void;
  canGoNext?: boolean;
  canGoPrevious?: boolean;
  className?: string;
}

const QuestionNavigation: React.FC<QuestionNavigationProps> = ({
  currentIndex,
  totalQuestions,
  onPrevious,
  onNext,
  canGoNext = true,
  canGoPrevious = true,
  className = ''
}) => {
  const isFirstQuestion = currentIndex === 0;
  const isLastQuestion = currentIndex === totalQuestions - 1;

  return (
    <div className={`question-navigation ${className}`}>
      <div className="question-navigation__info">
        <span className="question-navigation__counter">
          Câu {currentIndex + 1} / {totalQuestions}
        </span>
        <div className="question-navigation__progress">
          <div 
            className="question-navigation__progress-bar"
            style={{ width: `${((currentIndex + 1) / totalQuestions) * 100}%` }}
          />
        </div>
      </div>
      
      <div className="question-navigation__controls">
        <button
          className="nav-button nav-button--previous"
          onClick={onPrevious}
          disabled={!canGoPrevious || isFirstQuestion}
          title="Câu trước"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15,18 9,12 15,6"></polyline>
          </svg>
          <span>Câu trước</span>
        </button>
        
        <div className="question-navigation__spacer" />
        
        <button
          className="nav-button nav-button--next"
          onClick={onNext}
          disabled={!canGoNext}
          title={isLastQuestion ? "Hoàn thành" : "Câu tiếp theo"}
        >
          <span>{isLastQuestion ? "Hoàn thành" : "Câu tiếp theo"}</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="9,18 15,12 9,6"></polyline>
          </svg>
        </button>
      </div>
      
      <div className="question-navigation__hints">
        <div className="hint-item">
          <span className="hint-icon">⌨️</span>
          <span>Sử dụng phím mũi tên để điều hướng</span>
        </div>
        <div className="hint-item">
          <span className="hint-icon">↩️</span>
          <span>Enter để gửi câu trả lời</span>
        </div>
      </div>
    </div>
  );
};

export default QuestionNavigation;
