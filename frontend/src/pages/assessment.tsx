'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import AssessmentForm from '@/components/AssessmentForm';
import { Question, Answer } from '@/shared/types';
import { getFromStorage, setToStorage, STORAGE_KEYS } from '@/utils/helpers';

export default function AssessmentPage() {
  const router = useRouter();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState(1);
  const [totalQuestions, setTotalQuestions] = useState(0);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      setError(null);

      // Check if user is authenticated
      const token = getFromStorage<string>(STORAGE_KEYS.ACCESS_TOKEN);
      if (!token) {
        router.push('/login');
        return;
      }

      // Create assessment
      const assessmentResponse = await fetch('/api/v1/assessments', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ user_id: 'current_user' }),
      });

      if (!assessmentResponse.ok) {
        throw new Error('Failed to create assessment');
      }

      const assessment = await assessmentResponse.json();
      setToStorage(STORAGE_KEYS.CURRENT_ASSESSMENT, assessment);

      // Load questions
      const questionsResponse = await fetch(`/api/v1/assessments/${assessment.id}/questions`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!questionsResponse.ok) {
        throw new Error('Failed to load questions');
      }

      const questionsData = await questionsResponse.json();
      setQuestions(questionsData);
      setTotalQuestions(questionsData.length);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleProgress = (current: number, total: number) => {
    setCurrentQuestion(current);
    setTotalQuestions(total);
  };

  const handleSubmit = async (answers: Answer[]) => {
    try {
      const token = getFromStorage<string>(STORAGE_KEYS.ACCESS_TOKEN);
      const assessment = getFromStorage(STORAGE_KEYS.CURRENT_ASSESSMENT);

      if (!token || !assessment) {
        throw new Error('No active assessment found');
      }

      // Submit answers
      const submitResponse = await fetch(`/api/v1/assessments/${assessment.id}/answers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ answers }),
      });

      if (!submitResponse.ok) {
        throw new Error('Failed to submit answers');
      }

      // Complete assessment
      const completeResponse = await fetch(`/api/v1/assessments/${assessment.id}/complete`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!completeResponse.ok) {
        throw new Error('Failed to complete assessment');
      }

      // Redirect to results
      router.push(`/results/${assessment.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit assessment');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải câu hỏi...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Có lỗi xảy ra</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="btn-primary"
          >
            Thử lại
          </button>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-6xl mb-4">📝</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Không có câu hỏi</h2>
          <p className="text-gray-600">Không tìm thấy câu hỏi nào để đánh giá.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Đánh giá 4 chỉ số phát triển
          </h1>
          <p className="text-gray-600">
            Hãy trả lời tất cả câu hỏi một cách chân thật để nhận được kết quả chính xác nhất.
          </p>
        </div>

        <AssessmentForm
          questions={questions}
          onSubmit={handleSubmit}
          onProgress={handleProgress}
        />
      </div>
    </div>
  );
}