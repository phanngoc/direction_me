/**
 * Career Suggestions Page for MyWay Career Assessment System.
 * Displays detailed career information and comparison.
 */
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import CareerSuggestions from '../components/CareerSuggestions';
import CareerComparison from '../components/CareerComparison';
import ErrorBoundary from '../components/ErrorBoundary';
import { apiClient } from '../services/api';

interface CareerSuggestion {
  id: string;
  career_name: string;
  fit_score: number;
  rank: number;
  explanation: string;
}

interface CareerRequirements {
  career_name: string;
  description: string;
  key_skills: string[];
  education_requirements: string;
  experience_level: string;
  salary_range: string;
  growth_outlook: string;
}

const CareersPage: React.FC = () => {
  const router = useRouter();
  const { assessment_result_id, career } = router.query;
  
  const [suggestions, setSuggestions] = useState<CareerSuggestion[]>([]);
  const [selectedCareers, setSelectedCareers] = useState<string[]>([]);
  const [careerDetails, setCareerDetails] = useState<CareerRequirements | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'suggestions' | 'comparison' | 'details'>('suggestions');

  useEffect(() => {
    if (assessment_result_id) {
      loadCareerSuggestions(assessment_result_id as string);
    }
    
    if (career) {
      loadCareerDetails(career as string);
      setViewMode('details');
    }
  }, [assessment_result_id, career]);

  const loadCareerSuggestions = async (resultId: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.get(`/careers/suggestions/${resultId}`);
      
      if (response.success) {
        setSuggestions(response.data);
      } else {
        setError('Không thể tải gợi ý nghề nghiệp');
      }
    } catch (err) {
      console.error('Error loading career suggestions:', err);
      setError('Có lỗi xảy ra khi tải gợi ý nghề nghiệp');
    } finally {
      setLoading(false);
    }
  };

  const loadCareerDetails = async (careerName: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.get(`/careers/requirements/${encodeURIComponent(careerName)}`);
      
      if (response.success) {
        setCareerDetails(response.data);
      } else {
        setError('Không thể tải thông tin nghề nghiệp');
      }
    } catch (err) {
      console.error('Error loading career details:', err);
      setError('Có lỗi xảy ra khi tải thông tin nghề nghiệp');
    } finally {
      setLoading(false);
    }
  };

  const handleCareerSelect = (career: CareerSuggestion) => {
    console.log('Selected career:', career);
  };

  const handleViewCareerDetails = (careerName: string) => {
    router.push(`/careers?career=${encodeURIComponent(careerName)}`);
  };

  const handleAddToComparison = (careerName: string) => {
    if (!selectedCareers.includes(careerName)) {
      setSelectedCareers([...selectedCareers, careerName]);
    }
  };

  const handleRemoveFromComparison = (careerName: string) => {
    setSelectedCareers(selectedCareers.filter(name => name !== careerName));
  };

  const handleCompareCareers = () => {
    if (selectedCareers.length >= 2) {
      setViewMode('comparison');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải thông tin nghề nghiệp...</p>
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
            Không thể tải thông tin
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
      <Head>
        <title>Gợi ý nghề nghiệp - MyWay</title>
        <meta name="description" content="Gợi ý nghề nghiệp phù hợp dựa trên kết quả đánh giá Ikigai" />
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
                  Gợi ý nghề nghiệp
                </h1>
              </div>
              
              {/* View Mode Toggle */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setViewMode('suggestions')}
                  className={`px-3 py-2 text-sm rounded-md transition-colors ${
                    viewMode === 'suggestions'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Gợi ý
                </button>
                <button
                  onClick={() => setViewMode('comparison')}
                  className={`px-3 py-2 text-sm rounded-md transition-colors ${
                    viewMode === 'comparison'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                  disabled={selectedCareers.length < 2}
                >
                  So sánh ({selectedCareers.length})
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Career Details View */}
          {viewMode === 'details' && careerDetails && (
            <div className="bg-white rounded-lg shadow-sm p-8">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">
                    {careerDetails.career_name}
                  </h2>
                  <p className="text-gray-600 text-lg">
                    {careerDetails.description}
                  </p>
                </div>
                <button
                  onClick={() => setViewMode('suggestions')}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  ← Quay lại danh sách
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Key Skills */}
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    Kỹ năng cần thiết
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {careerDetails.key_skills.map((skill, index) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Education Requirements */}
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    Yêu cầu học vấn
                  </h3>
                  <p className="text-gray-700">
                    {careerDetails.education_requirements}
                  </p>
                </div>

                {/* Experience Level */}
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    Cấp độ kinh nghiệm
                  </h3>
                  <p className="text-gray-700">
                    {careerDetails.experience_level}
                  </p>
                </div>

                {/* Salary Range */}
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    Mức lương
                  </h3>
                  <p className="text-gray-700">
                    {careerDetails.salary_range}
                  </p>
                </div>

                {/* Growth Outlook */}
                <div className="lg:col-span-2">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    Triển vọng phát triển
                  </h3>
                  <p className="text-gray-700">
                    {careerDetails.growth_outlook}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Suggestions View */}
          {viewMode === 'suggestions' && (
            <div>
              {/* Comparison Selection */}
              {suggestions.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    So sánh nghề nghiệp
                  </h3>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {suggestions.map((suggestion) => (
                      <button
                        key={suggestion.id}
                        onClick={() => {
                          if (selectedCareers.includes(suggestion.career_name)) {
                            handleRemoveFromComparison(suggestion.career_name);
                          } else {
                            handleAddToComparison(suggestion.career_name);
                          }
                        }}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                          selectedCareers.includes(suggestion.career_name)
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                        }`}
                      >
                        {suggestion.career_name}
                        {selectedCareers.includes(suggestion.career_name) && ' ✓'}
                      </button>
                    ))}
                  </div>
                  {selectedCareers.length >= 2 && (
                    <button
                      onClick={handleCompareCareers}
                      className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      So sánh {selectedCareers.length} nghề nghiệp
                    </button>
                  )}
                </div>
              )}

              {/* Career Suggestions */}
              <CareerSuggestions
                suggestions={suggestions}
                onCareerSelect={handleCareerSelect}
                onViewDetails={handleViewCareerDetails}
              />
            </div>
          )}

          {/* Comparison View */}
          {viewMode === 'comparison' && selectedCareers.length >= 2 && (
            <CareerComparison
              careerNames={selectedCareers}
              onBack={() => setViewMode('suggestions')}
            />
          )}
        </div>
      </div>
    </ErrorBoundary>
  );
};

export default CareersPage;