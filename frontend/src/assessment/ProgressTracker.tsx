import React from 'react';

interface ProgressTrackerProps {
  progress: {
    total: number;
    completed: number;
    current: number;
  };
  module: string;
  className?: string;
}

const ProgressTracker: React.FC<ProgressTrackerProps> = ({
  progress,
  module,
  className = ''
}) => {
  const percentage = progress.total > 0 ? (progress.completed / progress.total) * 100 : 0;
  const currentPercentage = progress.total > 0 ? (progress.current / progress.total) * 100 : 0;

  const getModuleProgress = () => {
    // This would typically calculate progress within the current module
    // For now, return a placeholder
    return {
      current: 1,
      total: 10,
      percentage: 10
    };
  };

  const moduleProgress = getModuleProgress();

  return (
    <div className={`progress-tracker ${className}`}>
      <div className="progress-tracker__overall">
        <div className="progress-tracker__header">
          <h3 className="progress-tracker__title">Tiến độ tổng thể</h3>
          <span className="progress-tracker__percentage">
            {Math.round(percentage)}%
          </span>
        </div>
        
        <div className="progress-tracker__bar">
          <div 
            className="progress-tracker__fill"
            style={{ width: `${percentage}%` }}
          />
          <div 
            className="progress-tracker__current"
            style={{ width: `${currentPercentage}%` }}
          />
        </div>
        
        <div className="progress-tracker__stats">
          <span className="progress-tracker__stat">
            <strong>{progress.completed}</strong> / {progress.total} câu đã hoàn thành
          </span>
          <span className="progress-tracker__stat">
            <strong>{progress.current}</strong> câu hiện tại
          </span>
        </div>
      </div>
      
      <div className="progress-tracker__module">
        <div className="progress-tracker__header">
          <h4 className="progress-tracker__title">
            {module} - {getModuleName(module)}
          </h4>
          <span className="progress-tracker__percentage">
            {Math.round(moduleProgress.percentage)}%
          </span>
        </div>
        
        <div className="progress-tracker__bar progress-tracker__bar--module">
          <div 
            className="progress-tracker__fill"
            style={{ width: `${moduleProgress.percentage}%` }}
          />
        </div>
        
        <div className="progress-tracker__stats">
          <span className="progress-tracker__stat">
            <strong>{moduleProgress.current}</strong> / {moduleProgress.total} câu trong module
          </span>
        </div>
      </div>
      
      <div className="progress-tracker__modules">
        <div className="module-indicator">
          <span className={`module-indicator__item ${module === 'IQ' ? 'active' : progress.completed > 0 ? 'completed' : ''}`}>
            🧠 IQ
          </span>
          <span className={`module-indicator__item ${module === 'EQ' ? 'active' : progress.completed > 10 ? 'completed' : ''}`}>
            ❤️ EQ
          </span>
          <span className={`module-indicator__item ${module === 'DQ' ? 'active' : progress.completed > 25 ? 'completed' : ''}`}>
            💻 DQ
          </span>
          <span className={`module-indicator__item ${module === 'AQ' ? 'active' : progress.completed > 37 ? 'completed' : ''}`}>
            🔄 AQ
          </span>
        </div>
      </div>
    </div>
  );
};

const getModuleName = (module: string): string => {
  const names = {
    IQ: 'Trí thông minh',
    EQ: 'Trí tuệ cảm xúc', 
    DQ: 'Trí tuệ số',
    AQ: 'Trí tuệ thích nghi'
  };
  return names[module as keyof typeof names] || module;
};

export default ProgressTracker;
