'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ProgressDashboard from '@/components/ProgressDashboard';
import ProgressChart from '@/components/ProgressChart';
import ProgressComparison from '@/components/ProgressComparison';

const ProgressPage: React.FC = () => {
  const router = useRouter();
  const [analytics, setAnalytics] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [comparison, setComparison] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedView, setSelectedView] = useState<'dashboard' | 'chart' | 'comparison'>('dashboard');

  useEffect(() => {
    fetchProgressData();
  }, []);

  const fetchProgressData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Load progress data
      const response = await fetch('/api/v1/progress');
      
      if (response.ok) {
        const data = await response.json();
        setAnalytics(data.analytics);
        setHistory(data.history);
        setComparison(data.comparison);
      } else {
        setError('Không thể tải dữ liệu tiến độ');
      }
    } catch (err) {
      console.error('Error loading progress data:', err);
      setError('Có lỗi xảy ra khi tải dữ liệu tiến độ');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dữ liệu tiến độ...</p>
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
            Theo dõi tiến độ
          </h1>
          <p className="text-gray-600">
            Phân tích sự phát triển và cải thiện qua các lần đánh giá
          </p>
        </div>

        {/* View Toggle */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg shadow-sm p-1">
            <button
              onClick={() => setSelectedView('dashboard')}
              className={`px-4 py-2 rounded-md transition-colors ${
                selectedView === 'dashboard'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setSelectedView('chart')}
              className={`px-4 py-2 rounded-md transition-colors ${
                selectedView === 'chart'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Biểu đồ
            </button>
            <button
              onClick={() => setSelectedView('comparison')}
              className={`px-4 py-2 rounded-md transition-colors ${
                selectedView === 'comparison'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              So sánh
            </button>
          </div>
        </div>

        {/* Content */}
        {selectedView === 'dashboard' && (
          <ProgressDashboard 
            analytics={analytics}
            history={history}
          />
        )}
        
        {selectedView === 'chart' && (
          <ProgressChart 
            data={history}
          />
        )}
        
        {selectedView === 'comparison' && (
          <ProgressComparison 
            comparison={comparison}
          />
        )}
      </div>
    </div>
  );
};

export default ProgressPage;
