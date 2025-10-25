'use client';

import React from 'react';
import RadarChart from './RadarChart';
import { AssessmentResult } from '@/shared/types';
import { formatScore, getCategoryDisplayName } from '@/utils/helpers';

interface ResultsDisplayProps {
  result: AssessmentResult;
  className?: string;
}

export default function ResultsDisplay({ result, className = '' }: ResultsDisplayProps) {
  const scores = {
    iq_score: result.iq_score || 0,
    eq_score: result.eq_score || 0,
    dq_score: result.dq_score || 0,
    aq_score: result.aq_score || 0,
  };

  const getScoreLevel = (score: number) => {
    if (score >= 80) return { level: 'Xuất sắc', color: 'text-green-600', bgColor: 'bg-green-100' };
    if (score >= 60) return { level: 'Tốt', color: 'text-blue-600', bgColor: 'bg-blue-100' };
    if (score >= 40) return { level: 'Trung bình', color: 'text-yellow-600', bgColor: 'bg-yellow-100' };
    return { level: 'Cần cải thiện', color: 'text-red-600', bgColor: 'bg-red-100' };
  };

  const getScoreDescription = (category: string, score: number) => {
    const descriptions = {
      IQ: {
        high: 'Bạn có khả năng tư duy logic, phân tích và giải quyết vấn đề rất tốt.',
        medium: 'Bạn có khả năng tư duy logic và phân tích ở mức trung bình.',
        low: 'Bạn cần rèn luyện thêm khả năng tư duy logic và phân tích.'
      },
      EQ: {
        high: 'Bạn có khả năng hiểu và quản lý cảm xúc của bản thân và người khác rất tốt.',
        medium: 'Bạn có khả năng hiểu và quản lý cảm xúc ở mức trung bình.',
        low: 'Bạn cần rèn luyện thêm khả năng hiểu và quản lý cảm xúc.'
      },
      DQ: {
        high: 'Bạn có khả năng sử dụng công nghệ số và tư duy sáng tạo rất tốt.',
        medium: 'Bạn có khả năng sử dụng công nghệ số ở mức trung bình.',
        low: 'Bạn cần rèn luyện thêm khả năng sử dụng công nghệ số.'
      },
      AQ: {
        high: 'Bạn có khả năng vượt qua khó khăn và thích ứng với thay đổi rất tốt.',
        medium: 'Bạn có khả năng vượt qua khó khăn ở mức trung bình.',
        low: 'Bạn cần rèn luyện thêm khả năng vượt qua khó khăn.'
      }
    };

    const level = score >= 60 ? 'high' : score >= 40 ? 'medium' : 'low';
    return descriptions[category as keyof typeof descriptions]?.[level] || '';
  };

  return (
    <div className={`space-y-8 ${className}`}>
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Kết quả đánh giá của bạn
        </h1>
        <p className="text-gray-600">
          Dựa trên bài đánh giá, đây là phân tích chi tiết về 4 chỉ số phát triển của bạn
        </p>
      </div>

      {/* Radar Chart */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 text-center">
          Biểu đồ tổng quan
        </h2>
        <RadarChart data={scores} />
      </div>

      {/* Detailed Scores */}
      <div className="grid md:grid-cols-2 gap-6">
        {Object.entries(scores).map(([key, score]) => {
          const category = key.replace('_score', '').toUpperCase();
          const levelInfo = getScoreLevel(score);
          const description = getScoreDescription(category, score);

          return (
            <div key={key} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">
                  {getCategoryDisplayName(category)}
                </h3>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${levelInfo.bgColor} ${levelInfo.color}`}>
                  {levelInfo.level}
                </span>
              </div>

              <div className="mb-4">
                <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                  <span>Điểm số</span>
                  <span className="text-2xl font-bold text-gray-900">
                    {formatScore(score)}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all duration-500 ${
                      score >= 80 ? 'bg-green-500' :
                      score >= 60 ? 'bg-blue-500' :
                      score >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${score}%` }}
                  />
                </div>
              </div>

              <p className="text-gray-600 text-sm leading-relaxed">
                {description}
              </p>
            </div>
          );
        })}
      </div>

      {/* Ikigai Scores (if available) */}
      {(result.ikigai_love || result.ikigai_good_at || result.ikigai_world_needs || result.ikigai_paid_for) && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4 text-center">
            Phân tích Ikigai
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { key: 'ikigai_love', label: 'Đam mê', value: result.ikigai_love },
              { key: 'ikigai_good_at', label: 'Giỏi', value: result.ikigai_good_at },
              { key: 'ikigai_world_needs', label: 'Thế giới cần', value: result.ikigai_world_needs },
              { key: 'ikigai_paid_for', label: 'Được trả tiền', value: result.ikigai_paid_for },
            ].map(({ key, label, value }) => (
              <div key={key} className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  {formatScore(value || 0)}
                </div>
                <div className="text-sm text-gray-600">{label}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button className="btn-primary">
          Xem gợi ý nghề nghiệp
        </button>
        <button className="btn-secondary">
          Tạo lộ trình học tập
        </button>
        <button className="btn-secondary">
          Làm lại bài test
        </button>
      </div>
    </div>
  );
}