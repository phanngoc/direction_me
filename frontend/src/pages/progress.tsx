import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import ProgressDashboard from '../components/ProgressDashboard';
import ProgressChart from '../components/ProgressChart';
import ProgressComparison from '../components/ProgressComparison';

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
      const token = localStorage.getItem('token');
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      // Fetch analytics
      const analyticsRes = await fetch(`${apiUrl}/progress/analytics`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!analyticsRes.ok) throw new Error('Failed to fetch analytics');
      const analyticsData = await analyticsRes.json();
      setAnalytics(analyticsData);

      // Fetch history
      const historyRes = await fetch(`${apiUrl}/progress/history?limit=20`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!historyRes.ok) throw new Error('Failed to fetch history');
      const historyData = await historyRes.json();
      setHistory(historyData);

      // Fetch latest comparison if available
      if (historyData.length >= 2) {
        const compareRes = await fetch(
          `${apiUrl}/progress/compare/${historyData[1].assessment_id}/${historyData[0].assessment_id}`,
          {
            headers: { 'Authorization': `Bearer ${token}` }
          }
        );

        if (compareRes.ok) {
          const compareData = await compareRes.json();
          setComparison(compareData);
        }
      }

      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your progress...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Error Loading Progress</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-gray-600">No progress data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Progress Tracking</h1>
          <p className="text-gray-600">Monitor your development journey and see how you're improving over time</p>
        </div>

        {/* View Selector */}
        <div className="mb-6 flex space-x-4 border-b border-gray-200">
          <button
            onClick={() => setSelectedView('dashboard')}
            className={`px-6 py-3 font-medium transition-colors ${
              selectedView === 'dashboard'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            📊 Dashboard
          </button>
          <button
            onClick={() => setSelectedView('chart')}
            className={`px-6 py-3 font-medium transition-colors ${
              selectedView === 'chart'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            📈 Score History
          </button>
          {comparison && (
            <button
              onClick={() => setSelectedView('comparison')}
              className={`px-6 py-3 font-medium transition-colors ${
                selectedView === 'comparison'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              🔍 Comparison
            </button>
          )}
        </div>

        {/* Content */}
        <div className="mb-8">
          {selectedView === 'dashboard' && (
            <ProgressDashboard data={analytics} history={history} />
          )}
          {selectedView === 'chart' && (
            <div className="bg-white p-6 rounded-lg shadow">
              <ProgressChart history={history} />
            </div>
          )}
          {selectedView === 'comparison' && comparison && (
            <ProgressComparison data={comparison} />
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex justify-between items-center mt-8">
          <button
            onClick={() => router.push('/dashboard')}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-100"
          >
            Back to Dashboard
          </button>
          <button
            onClick={() => router.push('/assessment')}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Take New Assessment
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProgressPage;
