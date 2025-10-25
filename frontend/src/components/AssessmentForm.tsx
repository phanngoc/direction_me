'use client';

import React, { useState, useEffect } from 'react';
import { Question, Answer } from '@/shared/types';
import QuestionDisplay from './QuestionDisplay';

interface AssessmentFormProps {
  questions: Question[];
  onSubmit: (answers: Answer[]) => void;
  onProgress: (current: number, total: number) => void;
}

export default function AssessmentForm({ questions, onSubmit, onProgress }: AssessmentFormProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  useEffect(() => {
    onProgress(currentQuestionIndex + 1, questions.length);
  }, [currentQuestionIndex, questions.length, onProgress]);

  const handleAnswer = (answer: Answer) => {
    const existingAnswerIndex = answers.findIndex(a => a.question_id === answer.question_id);
    
    if (existingAnswerIndex >= 0) {
      // Update existing answer
      const newAnswers = [...answers];
      newAnswers[existingAnswerIndex] = answer;
      setAnswers(newAnswers);
    } else {
      // Add new answer
      setAnswers([...answers, answer]);
    }
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      await onSubmit(answers);
    } finally {
      setIsSubmitting(false);
    }
  };

  const isLastQuestion = currentQuestionIndex === questions.length - 1;
  const hasAnswered = answers.some(a => a.question_id === currentQuestion.id);

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Câu hỏi {currentQuestionIndex + 1} / {questions.length}</span>
          <span>{Math.round(progress)}% hoàn thành</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Question Display */}
      {currentQuestion && (
        <QuestionDisplay
          question={currentQuestion}
          onAnswer={handleAnswer}
          currentAnswer={answers.find(a => a.question_id === currentQuestion.id)}
        />
      )}

      {/* Navigation */}
      <div className="flex justify-between mt-8">
        <button
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
          className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ← Câu trước
        </button>

        <div className="flex gap-4">
          {!isLastQuestion ? (
            <button
              onClick={handleNext}
              disabled={!hasAnswered}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Câu tiếp theo →
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={!hasAnswered || isSubmitting}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Đang xử lý...' : 'Hoàn thành đánh giá'}
            </button>
          )}
        </div>
      </div>

      {/* Answer Summary */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-semibold text-gray-700 mb-2">Tóm tắt câu trả lời:</h3>
        <p className="text-sm text-gray-600">
          Đã trả lời: {answers.length} / {questions.length} câu hỏi
        </p>
      </div>
    </div>
  );
}