import React, { useState } from 'react';

interface ProgressTrackerProps {
  totalWeeks: number;
  currentWeek: number;
  onWeekChange?: (week: number) => void;
  milestones?: Array<{
    week: number;
    title: string;
    description: string;
  }>;
}

const ProgressTracker: React.FC<ProgressTrackerProps> = ({
  totalWeeks,
  currentWeek,
  onWeekChange,
  milestones = []
}) => {
  const [selectedWeek, setSelectedWeek] = useState<number>(currentWeek);

  const handleWeekClick = (week: number) => {
    setSelectedWeek(week);
    if (onWeekChange) {
      onWeekChange(week);
    }
  };

  const progressPercentage = (currentWeek / totalWeeks) * 100;

  // Generate week markers
  const weekMarkers = Array.from({ length: totalWeeks }, (_, i) => i + 1);

  // Determine week status
  const getWeekStatus = (week: number): 'completed' | 'current' | 'future' => {
    if (week < currentWeek) return 'completed';
    if (week === currentWeek) return 'current';
    return 'future';
  };

  // Get milestone for a specific week
  const getMilestone = (week: number) => {
    return milestones.find(m => m.week === week);
  };

  return (
    <div className="progress-tracker w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Learning Progress Tracker</h2>

      {/* Overall Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Overall Progress</span>
          <span className="text-sm font-semibold text-blue-600">
            {Math.round(progressPercentage)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div
            className="bg-blue-600 h-4 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${Math.min(progressPercentage, 100)}%` }}
          >
            <div className="h-full w-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full animate-pulse"></div>
          </div>
        </div>
        <div className="flex justify-between mt-2 text-xs text-gray-500">
          <span>Week 1</span>
          <span>Week {totalWeeks}</span>
        </div>
      </div>

      {/* Week by Week Progress */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-700">Week-by-Week Progress</h3>
        <div className="grid grid-cols-10 gap-2">
          {weekMarkers.map((week) => {
            const status = getWeekStatus(week);
            const milestone = getMilestone(week);
            const isSelected = week === selectedWeek;

            return (
              <div key={week} className="relative group">
                <button
                  onClick={() => handleWeekClick(week)}
                  className={`
                    w-full aspect-square rounded-lg border-2 transition-all duration-200
                    ${status === 'completed'
                      ? 'bg-green-500 border-green-600 text-white hover:bg-green-600'
                      : status === 'current'
                      ? 'bg-blue-500 border-blue-600 text-white hover:bg-blue-600 ring-2 ring-blue-300'
                      : 'bg-gray-100 border-gray-300 text-gray-600 hover:bg-gray-200'
                    }
                    ${isSelected ? 'ring-4 ring-yellow-400' : ''}
                    ${milestone ? 'ring-2 ring-purple-400' : ''}
                  `}
                  aria-label={`Week ${week}`}
                >
                  <span className="text-xs font-semibold">{week}</span>
                  {milestone && (
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-purple-500 rounded-full border-2 border-white"></div>
                  )}
                </button>

                {/* Tooltip */}
                {milestone && (
                  <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-48 opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10">
                    <div className="bg-gray-900 text-white text-xs rounded py-2 px-3 shadow-lg">
                      <div className="font-semibold mb-1">{milestone.title}</div>
                      <div className="text-gray-300">{milestone.description}</div>
                      <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-900"></div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Legend */}
      <div className="flex justify-center items-center space-x-6 text-sm">
        <div className="flex items-center">
          <div className="w-4 h-4 bg-green-500 border-2 border-green-600 rounded mr-2"></div>
          <span className="text-gray-700">Completed</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-blue-500 border-2 border-blue-600 rounded mr-2"></div>
          <span className="text-gray-700">Current</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-gray-100 border-2 border-gray-300 rounded mr-2"></div>
          <span className="text-gray-700">Future</span>
        </div>
        {milestones.length > 0 && (
          <div className="flex items-center">
            <div className="w-4 h-4 bg-purple-500 rounded-full mr-2"></div>
            <span className="text-gray-700">Milestone</span>
          </div>
        )}
      </div>

      {/* Selected Week Details */}
      {selectedWeek > 0 && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded">
          <h4 className="font-semibold text-blue-900 mb-2">Week {selectedWeek} Details</h4>
          {getMilestone(selectedWeek) ? (
            <div>
              <p className="text-sm font-medium text-blue-800">{getMilestone(selectedWeek)?.title}</p>
              <p className="text-sm text-blue-700 mt-1">{getMilestone(selectedWeek)?.description}</p>
            </div>
          ) : (
            <p className="text-sm text-blue-700">
              {getWeekStatus(selectedWeek) === 'completed'
                ? 'Completed - Great job!'
                : getWeekStatus(selectedWeek) === 'current'
                ? 'Current week - Keep going!'
                : 'Upcoming week - Stay focused!'}
            </p>
          )}
        </div>
      )}

      {/* Statistics */}
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="text-center p-4 bg-green-50 border border-green-200 rounded">
          <div className="text-2xl font-bold text-green-700">{currentWeek - 1}</div>
          <div className="text-sm text-green-600">Completed Weeks</div>
        </div>
        <div className="text-center p-4 bg-blue-50 border border-blue-200 rounded">
          <div className="text-2xl font-bold text-blue-700">{totalWeeks - currentWeek + 1}</div>
          <div className="text-sm text-blue-600">Remaining Weeks</div>
        </div>
        <div className="text-center p-4 bg-purple-50 border border-purple-200 rounded">
          <div className="text-2xl font-bold text-purple-700">{milestones.length}</div>
          <div className="text-sm text-purple-600">Milestones</div>
        </div>
      </div>
    </div>
  );
};

export default ProgressTracker;
