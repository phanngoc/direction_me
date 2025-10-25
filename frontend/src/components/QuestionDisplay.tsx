'use client';

import React, { useState } from 'react';
import { Question, Answer } from '@/shared/types';

interface QuestionDisplayProps {
  question: Question;
  onAnswer: (answer: Answer) => void;
  currentAnswer?: Answer;
}

export default function QuestionDisplay({ question, onAnswer, currentAnswer }: QuestionDisplayProps) {
  const [selectedValue, setSelectedValue] = useState<number>(
    currentAnswer?.answer_value || 0
  );

  const handleAnswerChange = (value: number) => {
    setSelectedValue(value);
    onAnswer({
      question_id: question.id,
      answer_value: value,
      answer_text: question.question_type === 'Likert' ? value.toString() : undefined
    });
  };

  const renderMCQOptions = () => {
    if (!question.options) return null;

    return (
      <div className="space-y-3">
        {question.options.map((option, index) => (
          <label
            key={index}
            className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
          >
            <input
              type="radio"
              name={`question-${question.id}`}
              value={index + 1}
              checked={selectedValue === index + 1}
              onChange={() => handleAnswerChange(index + 1)}
              className="mr-3 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-gray-700">{option}</span>
          </label>
        ))}
      </div>
    );
  };

  const renderLikertScale = () => {
    const scaleLabels = [
      'Hoàn toàn không đồng ý',
      'Không đồng ý',
      'Trung lập',
      'Đồng ý',
      'Hoàn toàn đồng ý'
    ];

    return (
      <div className="space-y-4">
        <div className="flex justify-between text-sm text-gray-500 mb-4">
          <span>Hoàn toàn không đồng ý</span>
          <span>Hoàn toàn đồng ý</span>
        </div>
        
        <div className="space-y-3">
          {scaleLabels.map((label, index) => (
            <label
              key={index}
              className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
            >
              <input
                type="radio"
                name={`question-${question.id}`}
                value={index + 1}
                checked={selectedValue === index + 1}
                onChange={() => handleAnswerChange(index + 1)}
                className="mr-3 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-gray-700">{label}</span>
            </label>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Question Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-blue-600 bg-blue-100 px-3 py-1 rounded-full">
            {question.category}
          </span>
          <span className="text-sm text-gray-500">
            {question.question_type}
          </span>
        </div>
        <h2 className="text-xl font-semibold text-gray-900">
          {question.question_text}
        </h2>
      </div>

      {/* Answer Options */}
      <div className="mb-6">
        {question.question_type === 'MCQ' ? renderMCQOptions() : renderLikertScale()}
      </div>

      {/* Question Info */}
      <div className="text-sm text-gray-500 border-t pt-4">
        <p>
          <strong>Facet:</strong> {question.facet}
          {question.difficulty_weight && (
            <>
              {' • '}
              <strong>Độ khó:</strong> {question.difficulty_weight}
            </>
          )}
          {question.reverse_score && (
            <>
              {' • '}
              <span className="text-orange-600">Câu hỏi đảo ngược</span>
            </>
          )}
        </p>
      </div>
    </div>
  );
}