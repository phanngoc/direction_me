/**
 * Ikigai Analysis Page for MyWay Career Assessment System.
 * Displays comprehensive Ikigai analysis and interpretation.
 */
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import IkigaiChart from '../components/IkigaiChart';
import CareerSuggestions from '../components/CareerSuggestions';
import ErrorBoundary from '../components/ErrorBoundary';
import { apiClient } from '../services/api';

interface IkigaiScores {
  ikigai_love: number;
  ikigai_good_at: number;
  ikigai_world_needs: number;
  ikigai_paid_for: number;
  ikigai_harmonic: number;
  ikigai_geometric: number;
}

interface IkigaiInterpretation {
  love: string;
  good_at: string;
  world_needs: string;
  paid_for: string;
  overall: string;
}

interface CareerSuggestion {
  id: string;
  career_name: string;
  fit_score: number;
  rank: number;
  explanation: string;
}

interface IkigaiAnalysis {
  ikigai_scores: IkigaiScores;
  ikigai_interpretation: IkigaiInterpretation;
  ikigai_quadrant: string;
  development_recommendations: string[];
  career_suggestions: CareerSuggestion[];
}

const IkigaiAnalysisPage: React.FC = () => {
  const router = useRouter();
  const { assessment_result_id } = router.query;
  
  const [analysis, setAnalysis] = useState<IkigaiAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'careers' | 'recommendations'>('overview');

  useEffect(() => {
    if (assessment_result_id) {
      loadIkigaiAnalysis(assessment_result_id as string);
    }
  }, [assessment_result_id]);

  const loadIkigaiAnalysis = async (resultId: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.get(`/ikigai/analysis/${resultId}`);
      
      if (response.success) {
        setAnalysis(response.data);
      } else {
        setError('Không thể tải phân tích Ikigai');
      }
    } catch (err) {
      console.error('Error loading Ikigai analysis:', err);
      setError('Có lỗi xảy ra khi tải phân tích Ikigai');
    } finally {
      setLoading(false);
    }
  };

  const handleCareerSelect = (career: CareerSuggestion) => {
    console.log('Selected career:', career);
    // Handle career selection logic
  };

  const handleViewCareerDetails = (careerName: string) => {
    router.push(`/careers?career=${encodeURIComponent(careerName)}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang phân tích Ikigai của bạn...</p>
        </div>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Không thể tải phân tích
          </h1>
          <p className="text-gray-600 mb-6">
            {error || 'Không tìm thấy kết quả đánh giá'}
          </p>
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
      <Head>
        <title>Phân tích Ikigai - MyWay</title>
        <meta name="description" content="Phân tích Ikigai và gợi ý nghề nghiệp dựa trên kết quả đánh giá" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center">
                <button
                  onClick={() => router.back()}
                  className="mr-4 p-2 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  ← Quay lại
                </button>
                <h1 className="text-2xl font-bold text-gray-900">
                  Phân tích Ikigai
                </h1>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Ikigai Quadrant */}
          <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Vùng Ikigai của bạn
            </h2>
            <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-lg p-6 text-center">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {analysis.ikigai_quadrant}
              </h3>
              <p className="text-gray-600">
                {analysis.ikigai_interpretation.overall}
              </p>
            </div>
          </div>

          {/* Tabs */}
          <div className="bg-white rounded-lg shadow-sm mb-8">
            <div className="border-b border-gray-200">
              <nav className="flex space-x-8 px-6">
                {[
                  { id: 'overview', label: 'Tổng quan', icon: '📊' },
                  { id: 'careers', label: 'Nghề nghiệp', icon: '💼' },
                  { id: 'recommendations', label: 'Khuyến nghị', icon: '💡' }
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <span className="mr-2">{tab.icon}</span>
                    {tab.label}
                  </button>
                ))}
              </nav>
            </div>

            <div className="p-6">
              {/* Overview Tab */}
              {activeTab === 'overview' && (
                <div className="space-y-8">
                  {/* Ikigai Chart */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                      Biểu đồ Ikigai
                    </h3>
                    <IkigaiChart scores={analysis.ikigai_scores} />
                  </div>

                  {/* Individual Interpretations */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                      Phân tích chi tiết
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="bg-red-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-red-900 mb-2">
                          🔥 Đam mê (Love)
                        </h4>
                        <p className="text-red-700 text-sm">
                          {analysis.ikigai_interpretation.love}
                        </p>
                      </div>
                      
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-blue-900 mb-2">
                          🎯 Tài năng (Good at)
                        </h4>
                        <p className="text-blue-700 text-sm">
                          {analysis.ikigai_interpretation.good_at}
                        </p>
                      </div>
                      
                      <div className="bg-green-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-green-900 mb-2">
                          🌍 Nhu cầu xã hội (World needs)
                        </h4>
                        <p className="text-green-700 text-sm">
                          {analysis.ikigai_interpretation.world_needs}
                        </p>
                      </div>
                      
                      <div className="bg-yellow-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-yellow-900 mb-2">
                          💰 Khả năng kiếm tiền (Paid for)
                        </h4>
                        <p className="text-yellow-700 text-sm">
                          {analysis.ikigai_interpretation.paid_for}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Careers Tab */}
              {activeTab === 'careers' && (
                <CareerSuggestions
                  suggestions={analysis.career_suggestions}
                  onCareerSelect={handleCareerSelect}
                  onViewDetails={handleViewCareerDetails}
                />
              )}

              {/* Recommendations Tab */}
              {activeTab === 'recommendations' && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Khuyến nghị phát triển
                  </h3>
                  <div className="space-y-4">
                    {analysis.development_recommendations.map((recommendation, index) => (
                      <div key={index} className="bg-blue-50 p-4 rounded-lg">
                        <div className="flex items-start">
                          <div className="flex-shrink-0">
                            <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                              {index + 1}
                            </div>
                          </div>
                          <div className="ml-3">
                            <p className="text-blue-900 text-sm">
                              {recommendation}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-center space-x-4">
            <button
              onClick={() => router.push('/assessment')}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              Làm lại bài test
            </button>
            <button
              onClick={() => router.push('/learning-path')}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Xem lộ trình học tập
            </button>
          </div>
        </div>
      </div>
    </ErrorBoundary>
  );
};

export default IkigaiAnalysisPage;