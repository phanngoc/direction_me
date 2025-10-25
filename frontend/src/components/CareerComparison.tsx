/**
 * Career Comparison Component for MyWay Career Assessment System.
 * Displays side-by-side comparison of multiple careers.
 */
import React, { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

interface CareerRequirements {
  career_name: string;
  description: string;
  key_skills: string[];
  education_requirements: string;
  experience_level: string;
  salary_range: string;
  growth_outlook: string;
}

interface CareerComparisonProps {
  careerNames: string[];
  onBack?: () => void;
  className?: string;
}

const CareerComparison: React.FC<CareerComparisonProps> = ({
  careerNames,
  onBack,
  className = ''
}) => {
  const [careers, setCareers] = useState<CareerRequirements[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadCareerData();
  }, [careerNames]);

  const loadCareerData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.get(`/careers/compare?career_names=${careerNames.join(',')}`);
      
      if (response.success) {
        setCareers(Object.values(response.data));
      } else {
        setError('Không thể tải thông tin so sánh');
      }
    } catch (err) {
      console.error('Error loading career comparison:', err);
      setError('Có lỗi xảy ra khi tải thông tin so sánh');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={`career-comparison ${className}`}>
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải thông tin so sánh...</p>
        </div>
      </div>
    );
  }

  if (error || careers.length === 0) {
    return (
      <div className={`career-comparison ${className}`}>
        <div className="text-center py-8">
          <div className="text-red-500 text-4xl mb-4">⚠️</div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Không thể tải thông tin so sánh
          </h3>
          <p className="text-gray-600 mb-4">{error}</p>
          {onBack && (
            <button
              onClick={onBack}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              Quay lại
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={`career-comparison ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          So sánh nghề nghiệp
        </h2>
        {onBack && (
          <button
            onClick={onBack}
            className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            ← Quay lại
          </button>
        )}
      </div>

      {/* Comparison Table */}
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tiêu chí
                </th>
                {careers.map((career) => (
                  <th
                    key={career.career_name}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[200px]"
                  >
                    {career.career_name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {/* Description */}
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Mô tả
                </td>
                {careers.map((career) => (
                  <td key={career.career_name} className="px-6 py-4 text-sm text-gray-700">
                    {career.description}
                  </td>
                ))}
              </tr>

              {/* Key Skills */}
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Kỹ năng cần thiết
                </td>
                {careers.map((career) => (
                  <td key={career.career_name} className="px-6 py-4 text-sm text-gray-700">
                    <div className="flex flex-wrap gap-1">
                      {career.key_skills.slice(0, 3).map((skill, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs"
                        >
                          {skill}
                        </span>
                      ))}
                      {career.key_skills.length > 3 && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                          +{career.key_skills.length - 3} khác
                        </span>
                      )}
                    </div>
                  </td>
                ))}
              </tr>

              {/* Education Requirements */}
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Yêu cầu học vấn
                </td>
                {careers.map((career) => (
                  <td key={career.career_name} className="px-6 py-4 text-sm text-gray-700">
                    {career.education_requirements}
                  </td>
                ))}
              </tr>

              {/* Experience Level */}
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Cấp độ kinh nghiệm
                </td>
                {careers.map((career) => (
                  <td key={career.career_name} className="px-6 py-4 text-sm text-gray-700">
                    {career.experience_level}
                  </td>
                ))}
              </tr>

              {/* Salary Range */}
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Mức lương
                </td>
                {careers.map((career) => (
                  <td key={career.career_name} className="px-6 py-4 text-sm text-gray-700">
                    {career.salary_range}
                  </td>
                ))}
              </tr>

              {/* Growth Outlook */}
              <tr>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Triển vọng phát triển
                </td>
                {careers.map((career) => (
                  <td key={career.career_name} className="px-6 py-4 text-sm text-gray-700">
                    {career.growth_outlook}
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Summary */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {careers.map((career, index) => (
          <div key={career.career_name} className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {career.career_name}
            </h3>
            
            <div className="space-y-3">
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">
                  Kỹ năng chính
                </h4>
                <div className="flex flex-wrap gap-1">
                  {career.key_skills.slice(0, 4).map((skill, skillIndex) => (
                    <span
                      key={skillIndex}
                      className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">
                  Mức lương
                </h4>
                <p className="text-sm text-gray-600">{career.salary_range}</p>
              </div>
              
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">
                  Triển vọng
                </h4>
                <p className="text-sm text-gray-600">{career.growth_outlook}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CareerComparison;