import React from 'react';

interface ComparisonData {
  assessment_1: {
    id: string;
    date: string;
    scores: {
      iq: number;
      eq: number;
      dq: number;
      aq: number;
      ikigai: number;
    };
  };
  assessment_2: {
    id: string;
    date: string;
    scores: {
      iq: number;
      eq: number;
      dq: number;
      aq: number;
      ikigai: number;
    };
  };
  improvements: {
    iq: number;
    eq: number;
    dq: number;
    aq: number;
    ikigai: number;
  };
  improvement_percentages: {
    iq: number;
    eq: number;
    dq: number;
    aq: number;
  };
  time_between_assessments: number;
}

interface ProgressComparisonProps {
  data: ComparisonData;
}

const ProgressComparison: React.FC<ProgressComparisonProps> = ({ data }) => {
  const getImprovementColor = (value: number): string => {
    if (value > 0) return 'text-green-600';
    if (value < 0) return 'text-red-600';
    return 'text-gray-600';
  };

  const getImprovementIcon = (value: number): string => {
    if (value > 0) return '↗️';
    if (value < 0) return '↘️';
    return '➡️';
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  const categories = ['iq', 'eq', 'dq', 'aq', 'ikigai'];

  return (
    <div className="progress-comparison w-full max-w-6xl mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Assessment Comparison</h2>

      {/* Time Period */}
      <div className="text-center mb-8 p-4 bg-blue-50 rounded-lg">
        <div className="text-sm text-blue-600 font-medium">Time Between Assessments</div>
        <div className="text-2xl font-bold text-blue-700">{data.time_between_assessments} days</div>
      </div>

      {/* Comparison Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-3 text-left font-semibold text-gray-700 border-b-2">Category</th>
              <th className="p-3 text-center font-semibold text-gray-700 border-b-2">
                Previous<br />
                <span className="text-xs font-normal text-gray-500">{formatDate(data.assessment_1.date)}</span>
              </th>
              <th className="p-3 text-center font-semibold text-gray-700 border-b-2">
                Current<br />
                <span className="text-xs font-normal text-gray-500">{formatDate(data.assessment_2.date)}</span>
              </th>
              <th className="p-3 text-center font-semibold text-gray-700 border-b-2">Change</th>
              <th className="p-3 text-center font-semibold text-gray-700 border-b-2">Change %</th>
            </tr>
          </thead>
          <tbody>
            {categories.map((category) => {
              const score1 = data.assessment_1.scores[category as keyof typeof data.assessment_1.scores];
              const score2 = data.assessment_2.scores[category as keyof typeof data.assessment_2.scores];
              const improvement = data.improvements[category as keyof typeof data.improvements];
              const percentage = category !== 'ikigai'
                ? data.improvement_percentages[category as keyof typeof data.improvement_percentages]
                : null;

              return (
                <tr key={category} className="border-b hover:bg-gray-50">
                  <td className="p-3 font-medium text-gray-800 uppercase">{category}</td>
                  <td className="p-3 text-center">
                    <span className="inline-block px-3 py-1 bg-gray-100 rounded">
                      {score1.toFixed(1)}
                    </span>
                  </td>
                  <td className="p-3 text-center">
                    <span className="inline-block px-3 py-1 bg-blue-100 rounded font-semibold">
                      {score2.toFixed(1)}
                    </span>
                  </td>
                  <td className={`p-3 text-center font-bold ${getImprovementColor(improvement)}`}>
                    {getImprovementIcon(improvement)} {improvement > 0 ? '+' : ''}{improvement.toFixed(1)}
                  </td>
                  <td className={`p-3 text-center font-semibold ${getImprovementColor(improvement)}`}>
                    {percentage !== null ? `${percentage > 0 ? '+' : ''}${percentage.toFixed(1)}%` : '-'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="text-sm text-green-600 font-medium mb-2">Biggest Improvement</div>
          {(() => {
            const maxImprovement = Math.max(...Object.values(data.improvements));
            const bestCategory = Object.entries(data.improvements)
              .find(([_, val]) => val === maxImprovement)?.[0] || '';
            return (
              <>
                <div className="text-2xl font-bold text-green-700 uppercase">{bestCategory}</div>
                <div className="text-sm text-green-600">+{maxImprovement.toFixed(1)} points</div>
              </>
            );
          })()}
        </div>

        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="text-sm text-blue-600 font-medium mb-2">Overall Progress</div>
          <div className="text-2xl font-bold text-blue-700">
            {Object.values(data.improvements).reduce((a, b) => a + b, 0).toFixed(1)}
          </div>
          <div className="text-sm text-blue-600">Total points gained</div>
        </div>

        <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
          <div className="text-sm text-purple-600 font-medium mb-2">Categories Improved</div>
          <div className="text-2xl font-bold text-purple-700">
            {Object.values(data.improvements).filter(v => v > 0).length}/{categories.length}
          </div>
          <div className="text-sm text-purple-600">Positive changes</div>
        </div>
      </div>

      {/* Insights */}
      <div className="mt-8 p-6 bg-yellow-50 border border-yellow-200 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 text-yellow-900">💡 Insights</h3>
        <ul className="space-y-2 text-yellow-800">
          {Object.values(data.improvements).every(v => v >= 0) && (
            <li>🎉 Excellent! You've improved or maintained all categories!</li>
          )}
          {Object.values(data.improvements).reduce((a, b) => a + b, 0) > 20 && (
            <li>🚀 Outstanding progress! You've gained over 20 total points across all categories!</li>
          )}
          {Object.values(data.improvements).some(v => v > 15) && (
            <li>⭐ Remarkable improvement in one or more categories - keep up the great work!</li>
          )}
          {data.time_between_assessments < 30 && (
            <li>⚡ Quick reassessment! Make sure to give yourself enough time between assessments for meaningful growth.</li>
          )}
          {data.time_between_assessments > 60 && (
            <li>📅 Good spacing between assessments - this allows for real skill development!</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default ProgressComparison;
