import React from 'react';

interface Skill {
  name: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  duration_weeks: number;
  resources: string[];
}

interface TimelinePhase {
  phase: string;
  weeks: number;
  skills: Skill[];
}

interface SkillsTimelineProps {
  timeline: TimelinePhase[];
  currentWeek?: number;
}

const SkillsTimeline: React.FC<SkillsTimelineProps> = ({ timeline, currentWeek = 0 }) => {
  const getLevelColor = (level: string): string => {
    switch (level) {
      case 'beginner':
        return 'bg-green-500';
      case 'intermediate':
        return 'bg-yellow-500';
      case 'advanced':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusColor = (phaseWeeks: number, previousWeeks: number): string => {
    if (currentWeek >= previousWeeks + phaseWeeks) {
      return 'bg-green-100 border-green-500';
    } else if (currentWeek >= previousWeeks) {
      return 'bg-blue-100 border-blue-500';
    }
    return 'bg-gray-100 border-gray-300';
  };

  let cumulativeWeeks = 0;

  return (
    <div className="skills-timeline w-full max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6 text-center">Skills Development Timeline</h2>

      <div className="timeline-container relative">
        {/* Vertical timeline line */}
        <div className="absolute left-8 top-0 bottom-0 w-1 bg-gray-300"></div>

        {timeline.map((phase, index) => {
          const phaseStartWeek = cumulativeWeeks;
          const isCompleted = currentWeek >= cumulativeWeeks + phase.weeks;
          const isActive = currentWeek >= cumulativeWeeks && currentWeek < cumulativeWeeks + phase.weeks;

          const result = (
            <div key={index} className="phase-item mb-8 relative">
              {/* Timeline dot */}
              <div className={`absolute left-6 w-5 h-5 rounded-full border-4 ${
                isCompleted ? 'bg-green-500 border-green-700' :
                isActive ? 'bg-blue-500 border-blue-700' :
                'bg-gray-300 border-gray-400'
              } z-10`}></div>

              {/* Phase content */}
              <div className={`ml-16 p-6 border-2 rounded-lg ${getStatusColor(phase.weeks, phaseStartWeek)}`}>
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-xl font-semibold">{phase.phase}</h3>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    isCompleted ? 'bg-green-500 text-white' :
                    isActive ? 'bg-blue-500 text-white' :
                    'bg-gray-400 text-white'
                  }`}>
                    {isCompleted ? 'Completed' : isActive ? 'In Progress' : `Week ${phaseStartWeek + 1}-${phaseStartWeek + phase.weeks}`}
                  </span>
                </div>

                {/* Skills list */}
                <div className="skills-list space-y-3">
                  {phase.skills.map((skill, skillIndex) => (
                    <div key={skillIndex} className="skill-item bg-white p-4 rounded border border-gray-200">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-medium text-gray-800">{skill.name}</h4>
                        <span className={`px-2 py-1 rounded text-xs font-medium text-white ${getLevelColor(skill.level)}`}>
                          {skill.level}
                        </span>
                      </div>

                      <div className="text-sm text-gray-600 mb-2">
                        Duration: {skill.duration_weeks} {skill.duration_weeks === 1 ? 'week' : 'weeks'}
                      </div>

                      {skill.resources && skill.resources.length > 0 && (
                        <div className="resources">
                          <p className="text-xs text-gray-500 mb-1">Resources:</p>
                          <ul className="list-disc list-inside text-xs text-gray-600">
                            {skill.resources.map((resource, resIndex) => (
                              <li key={resIndex}>{resource}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );

          cumulativeWeeks += phase.weeks;
          return result;
        })}
      </div>

      {/* Progress summary */}
      <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded">
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-700">Overall Progress</span>
          <span className="text-sm font-semibold text-blue-600">
            Week {currentWeek} of {cumulativeWeeks}
          </span>
        </div>
        <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${Math.min((currentWeek / cumulativeWeeks) * 100, 100)}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default SkillsTimeline;
