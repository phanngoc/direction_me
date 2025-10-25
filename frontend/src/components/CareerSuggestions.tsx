/**
 * Career Suggestions Component for MyWay Career Assessment System.
 * Displays career recommendations with fit scores and explanations.
 */
import React, { useState } from 'react';

interface CareerSuggestion {
  id: string;
  career_name: string;
  fit_score: number;
  rank: number;
  explanation: string;
}

interface CareerSuggestionsProps {
  suggestions: CareerSuggestion[];
  onCareerSelect?: (career: CareerSuggestion) => void;
  onViewDetails?: (careerName: string) => void;
  className?: string;
}

const CareerSuggestions: React.FC<CareerSuggestionsProps> = ({
  suggestions,
  onCareerSelect,
  onViewDetails,
  className = ''
}) => {
  const [selectedCareer, setSelectedCareer] = useState<string | null>(null);

  const getFitScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 60) return 'text-blue-600 bg-blue-50 border-blue-200';
    if (score >= 40) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getFitScoreLabel = (score: number) => {
    if (score >= 80) return 'Phù hợp rất cao';
    if (score >= 60) return 'Phù hợp tốt';
    if (score >= 40) return 'Có tiềm năng';
    return 'Cần phát triển';
  };

  const getRankIcon = (rank: number) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  const handleCareerClick = (career: CareerSuggestion) => {
    setSelectedCareer(selectedCareer === career.id ? null : career.id);
    onCareerSelect?.(career);
  };

  const handleViewDetails = (e: React.MouseEvent, careerName: string) => {
    e.stopPropagation();
    onViewDetails?.(careerName);
  };

  if (!suggestions || suggestions.length === 0) {
    return (
      <div className={`career-suggestions ${className}`}>
        <div className="text-center py-8">
          <div className="text-gray-400 text-6xl mb-4">💼</div>
          <h3 className="text-lg font-semibold text-gray-600 mb-2">
            Chưa có gợi ý nghề nghiệp
          </h3>
          <p className="text-gray-500 text-sm">
            Hãy hoàn thành bài đánh giá để nhận gợi ý nghề nghiệp phù hợp
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`career-suggestions ${className}`}>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Gợi ý nghề nghiệp phù hợp
        </h2>
        <p className="text-gray-600">
          Dựa trên kết quả đánh giá, đây là những nghề nghiệp phù hợp nhất với bạn
        </p>
      </div>

      <div className="space-y-4">
        {suggestions.map((career) => (
          <div
            key={career.id}
            className={`career-card bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer ${
              selectedCareer === career.id ? 'ring-2 ring-blue-500' : ''
            }`}
            onClick={() => handleCareerClick(career)}
          >
            <div className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="text-2xl">
                    {getRankIcon(career.rank)}
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900">
                      {career.career_name}
                    </h3>
                    <div className="flex items-center space-x-2 mt-1">
                      <span
                        className={`px-3 py-1 rounded-full text-sm font-medium border ${getFitScoreColor(
                          career.fit_score
                        )}`}
                      >
                        {getFitScoreLabel(career.fit_score)}
                      </span>
                      <span className="text-gray-500 text-sm">
                        {career.fit_score.toFixed(1)}/100
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <button
                    onClick={(e) => handleViewDetails(e, career.career_name)}
                    className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-md transition-colors"
                  >
                    Chi tiết
                  </button>
                  <div className="text-gray-400">
                    {selectedCareer === career.id ? '▼' : '▶'}
                  </div>
                </div>
              </div>

              {/* Progress bar */}
              <div className="mb-4">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${
                      career.fit_score >= 80
                        ? 'bg-green-500'
                        : career.fit_score >= 60
                        ? 'bg-blue-500'
                        : career.fit_score >= 40
                        ? 'bg-yellow-500'
                        : 'bg-red-500'
                    }`}
                    style={{ width: `${career.fit_score}%` }}
                  />
                </div>
              </div>

              {/* Explanation (collapsible) */}
              {selectedCareer === career.id && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h4 className="font-semibold text-gray-900 mb-2">
                    Tại sao nghề này phù hợp với bạn?
                  </h4>
                  <p className="text-gray-700 text-sm leading-relaxed">
                    {career.explanation}
                  </p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="mt-8 bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Tổng quan gợi ý
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {suggestions.filter(s => s.fit_score >= 80).length}
            </div>
            <div className="text-gray-600">Phù hợp cao</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {suggestions.filter(s => s.fit_score >= 60 && s.fit_score < 80).length}
            </div>
            <div className="text-gray-600">Phù hợp tốt</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {suggestions.filter(s => s.fit_score >= 40 && s.fit_score < 60).length}
            </div>
            <div className="text-gray-600">Có tiềm năng</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-600">
              {suggestions.length}
            </div>
            <div className="text-gray-600">Tổng cộng</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CareerSuggestions;