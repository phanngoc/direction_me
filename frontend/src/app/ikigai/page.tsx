'use client';

/**
 * Ikigai Analysis Page for MyWay Career Assessment System.
 * Displays comprehensive Ikigai analysis and interpretation.
 */
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import IkigaiChart from '@/components/IkigaiChart';
import CareerSuggestions from '@/components/CareerSuggestions';
import ErrorBoundary from '@/components/ErrorBoundary';
import { apiClient } from '@/services/api';

interface IkigaiScores {
  ikigai_love: number;
  ikigai_good_at: number;
  ikigai_world_needs: number;
  ikigai_paid_for: number;
  ikigai_harmonic: number;
  ikigai_geometric: number;
}

const IkigaiPage: React.FC = () => {
  const router = useRouter();
  const [ikigaiData, setIkigaiData] = useState<IkigaiScores | null>(null);
  const [careerSuggestions, setCareerSuggestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadIkigaiData();
  }, []);

  const loadIkigaiData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load Ikigai analysis data
      const response = await apiClient.get('/ikigai/analysis');
      
      if (response.success) {
        setIkigaiData(response.data.ikigai_scores);
        setCareerSuggestions(response.data.career_suggestions || []);
      } else {
        setError('Không thể tải dữ liệu phân tích Ikigai');
      }
    } catch (err) {
      console.error('Error loading Ikigai data:', err);
      setError('Có lỗi xảy ra khi tải dữ liệu Ikigai');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải phân tích Ikigai...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Không thể tải dữ liệu
          </h1>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => router.push('/assessment')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Làm bài đánh giá
          </button>
        </div>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Phân tích Ikigai
            </h1>
            <p className="text-gray-600">
              Khám phá vùng giao thoa giữa đam mê, tài năng, nhu cầu xã hội và thu nhập
            </p>
          </div>

          {ikigaiData && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Biểu đồ Ikigai
                </h2>
                <IkigaiChart data={ikigaiData} />
              </div>

              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Gợi ý nghề nghiệp
                </h2>
                {careerSuggestions.length > 0 ? (
                  <CareerSuggestions 
                    suggestions={careerSuggestions}
                    onCareerSelect={(career) => console.log('Selected career:', career)}
                    onViewDetails={(careerName) => router.push(`/careers?career=${encodeURIComponent(careerName)}`)}
                  />
                ) : (
                  <p className="text-gray-500">Chưa có gợi ý nghề nghiệp</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </ErrorBoundary>
  );
};

export default IkigaiPage;
