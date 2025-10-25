'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ResultsDisplay from '@/components/ResultsDisplay';
import { AssessmentResult } from '@/shared/types';
import { getFromStorage, STORAGE_KEYS } from '@/utils/helpers';

interface ResultsPageProps {
  params: {
    assessmentId: string;
  };
}

export default function ResultsPage({ params }: ResultsPageProps) {
  const router = useRouter();
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResults();
  }, [params.assessmentId]);

  const loadResults = async () => {
    try {
      setLoading(true);
      setError(null);

      // Check if user is authenticated
      const token = getFromStorage<string>(STORAGE_KEYS.ACCESS_TOKEN);
      if (!token) {
        router.push('/login');
        return;
      }

      // Load assessment results
      const response = await fetch(`/api/v1/results/${params.assessmentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Không tìm thấy kết quả đánh giá');
        }
        throw new Error('Không thể tải kết quả đánh giá');
      }

      const resultData = await response.json();
      setResult(resultData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Đã xảy ra lỗi không xác định');
    } finally {
      setLoading(false);
    }
  };

  const handleViewCareers = () => {
    router.push(`/careers/${params.assessmentId}`);
  };

  const handleCreateLearningPath = () => {
    router.push(`/learning-path/${params.assessmentId}`);
  };

  const handleRetakeTest = () => {
    router.push('/assessment');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải kết quả...</p>
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
          <div className="space-x-4">
            <button
              onClick={() => window.location.reload()}
              className="btn-primary"
            >
              Thử lại
            </button>
            <button
              onClick={() => router.push('/')}
              className="btn-secondary"
            >
              Về trang chủ
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-6xl mb-4">📊</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Không có kết quả</h2>
          <p className="text-gray-600 mb-4">Không tìm thấy kết quả đánh giá cho assessment này.</p>
          <button
            onClick={() => router.push('/assessment')}
            className="btn-primary"
          >
            Làm bài đánh giá
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <ResultsDisplay result={result} />
      </div>
    </div>
  );
}
