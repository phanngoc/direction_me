import React from 'react';
import ProgressChart from './ProgressChart';

interface ProgressData {
  total_assessments: number;
  trends: {
    iq: string;
    eq: string;
    dq: string;
    aq: string;
  };
  best_improvement: {
    category: string;
    total_points: number;
  };
  latest_scores: {
    iq: number;
    eq: number;
    dq: number;
    aq: number;
  };
  first_assessment_date: string;
  latest_assessment_date: string;
}

interface ProgressDashboardProps {
  data: ProgressData;
  history?: Array<{
    iq_score: number;
    eq_score: number;
    dq_score: number;
    aq_score: number;
    calculated_at: string;
  }>;
}

const ProgressDashboard: React.FC<ProgressDashboardProps> = ({ data, history }) => {
  const getTrendIcon = (trend: string): string => {
    switch (trend) {
      case 'improving':
        return '📈';
      case 'declining':
        return '📉';
      case 'stable':
        return '➡️';
      default:
        return '❓';
    }
  };

  const getTrendColor = (trend: string): string => {
    switch (trend) {
      case 'improving':
        return 'text-green-600';
      case 'declining':
        return 'text-red-600';
      case 'stable':
        return 'text-gray-600';
      default:
        return 'text-gray-400';
    }
  };

  return (
    <div className="progress-dashboard w-full max-w-6xl mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Your Progress Dashboard</h2>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <div className="text-sm text-blue-600 font-medium mb-1">Total Assessments</div>
          <div className="text-3xl font-bold text-blue-700">{data.total_assessments}</div>
        </div>

        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <div className="text-sm text-green-600 font-medium mb-1">Best Improvement</div>
          <div className="text-2xl font-bold text-green-700">{data.best_improvement.category}</div>
          <div className="text-sm text-green-600">+{data.best_improvement.total_points.toFixed(1)} pts</div>
        </div>

        <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <div className="text-sm text-purple-600 font-medium mb-1">Days Tracking</div>
          <div className="text-3xl font-bold text-purple-700">
            {Math.floor((new Date(data.latest_assessment_date).getTime() - new Date(data.first_assessment_date).getTime()) / (1000 * 60 * 60 * 24))}
          </div>
        </div>

        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <div className="text-sm text-yellow-600 font-medium mb-1">Latest Score</div>
          <div className="text-2xl font-bold text-yellow-700">
            {Math.round((data.latest_scores.iq + data.latest_scores.eq + data.latest_scores.dq + data.latest_scores.aq) / 4)}
          </div>
          <div className="text-xs text-yellow-600">Average</div>
        </div>
      </div>

      {/* Trends */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold mb-4 text-gray-700">Trends by Category</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(data.trends).map(([category, trend]) => (
            <div key={category} className="p-4 border rounded-lg bg-gray-50">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-600 uppercase">{category}</span>
                <span className="text-2xl">{getTrendIcon(trend)}</span>
              </div>
              <div className={`text-sm font-semibold ${getTrendColor(trend)}`}>
                {trend.replace('_', ' ')}
              </div>
              <div className="text-xs text-gray-500 mt-1">
                Current: {data.latest_scores[category as keyof typeof data.latest_scores].toFixed(1)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Progress Chart */}
      {history && history.length > 0 && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4 text-gray-700">Score History</h3>
          <ProgressChart history={history} />
        </div>
      )}

      {/* Insights */}
      <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold mb-3 text-blue-900">📊 Progress Insights</h3>
        <ul className="space-y-2 text-blue-800">
          {data.trends.iq === 'improving' && (
            <li className="flex items-start">
              <span className="mr-2">✅</span>
              <span>Your IQ scores show consistent improvement - keep practicing logical and analytical tasks!</span>
            </li>
          )}
          {data.trends.eq === 'improving' && (
            <li className="flex items-start">
              <span className="mr-2">✅</span>
              <span>Great emotional intelligence growth - your social skills are developing well!</span>
            </li>
          )}
          {data.best_improvement.total_points > 10 && (
            <li className="flex items-start">
              <span className="mr-2">🌟</span>
              <span>Outstanding progress in {data.best_improvement.category} - you've improved by {data.best_improvement.total_points.toFixed(1)} points!</span>
            </li>
          )}
          {data.total_assessments >= 5 && (
            <li className="flex items-start">
              <span className="mr-2">🎯</span>
              <span>You're committed to growth with {data.total_assessments} assessments completed!</span>
            </li>
          )}
          {Object.values(data.trends).filter(t => t === 'improving').length >= 3 && (
            <li className="flex items-start">
              <span className="mr-2">🚀</span>
              <span>Incredible! You're improving across multiple dimensions simultaneously!</span>
            </li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default ProgressDashboard;
