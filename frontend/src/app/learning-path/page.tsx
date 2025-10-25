'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import LearningPath from '@/components/LearningPath';
import SkillsTimeline from '@/components/SkillsTimeline';
import ProgressTracker from '@/components/ProgressTracker';

interface LearningPathData {
  id: string;
  career_name: string;
  skills: Array<{
    name: string;
    level: string;
    duration_weeks: number;
    resources: string[];
  }>;
  projects: Array<{
    name: string;
    description: string;
    duration_weeks: number;
    skills_required: string[];
  }>;
  habits: Array<{
    name: string;
    description: string;
    frequency: string;
  }>;
  timeline_weeks: number;
  priority: 'high' | 'medium' | 'low';
}

const LearningPathPage: React.FC = () => {
  const router = useRouter();
  const [learningPath, setLearningPath] = useState<LearningPathData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedView, setSelectedView] = useState<'overview' | 'timeline' | 'progress'>('overview');

  useEffect(() => {
    loadLearningPath();
  }, []);

  const loadLearningPath = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load learning path data
      const response = await fetch('/api/v1/learning-path');
      
      if (response.ok) {
        const data = await response.json();
        setLearningPath(data);
      } else {
        setError('Không thể tải lộ trình học tập');
      }
    } catch (err) {
      console.error('Error loading learning path:', err);
      setError('Có lỗi xảy ra khi tải lộ trình học tập');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải lộ trình học tập...</p>
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
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Lộ trình học tập
          </h1>
          <p className="text-gray-600">
            Kế hoạch phát triển kỹ năng cá nhân hóa dựa trên kết quả đánh giá
          </p>
        </div>

        {/* View Toggle */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg shadow-sm p-1">
            <button
              onClick={() => setSelectedView('overview')}
              className={`px-4 py-2 rounded-md transition-colors ${
                selectedView === 'overview'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Tổng quan
            </button>
            <button
              onClick={() => setSelectedView('timeline')}
              className={`px-4 py-2 rounded-md transition-colors ${
                selectedView === 'timeline'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Timeline
            </button>
            <button
              onClick={() => setSelectedView('progress')}
              className={`px-4 py-2 rounded-md transition-colors ${
                selectedView === 'progress'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Tiến độ
            </button>
          </div>
        </div>

        {/* Content */}
        {selectedView === 'overview' && learningPath && (
          <LearningPath data={learningPath} />
        )}
        
        {selectedView === 'timeline' && learningPath && (
          <SkillsTimeline skills={learningPath.skills} />
        )}
        
        {selectedView === 'progress' && (
          <ProgressTracker />
        )}
      </div>
    </div>
  );
};

export default LearningPathPage;
