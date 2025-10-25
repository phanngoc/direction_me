import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import LearningPath from '../components/LearningPath';
import SkillsTimeline from '../components/SkillsTimeline';
import ProgressTracker from '../components/ProgressTracker';

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
    frequency: string;
    duration_minutes: number;
  }>;
  timeline_weeks: number;
  priority: string;
  created_at: string;
}

interface TimelinePhase {
  phase: string;
  weeks: number;
  skills: Array<{
    name: string;
    level: 'beginner' | 'intermediate' | 'advanced';
    duration_weeks: number;
    resources: string[];
  }>;
}

const LearningPathPage: React.FC = () => {
  const router = useRouter();
  const { result_id } = router.query;

  const [learningPath, setLearningPath] = useState<LearningPathData | null>(null);
  const [timelineData, setTimelineData] = useState<TimelinePhase[]>([]);
  const [currentWeek, setCurrentWeek] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!result_id) return;

    const fetchLearningPath = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem('token');

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/results/${result_id}/learning-path`,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          }
        );

        if (!response.ok) {
          throw new Error('Failed to fetch learning path');
        }

        const data: LearningPathData = await response.json();
        setLearningPath(data);

        // Transform data into timeline phases
        const phases = generateTimelinePhases(data);
        setTimelineData(phases);

        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setLoading(false);
      }
    };

    fetchLearningPath();
  }, [result_id]);

  const generateTimelinePhases = (data: LearningPathData): TimelinePhase[] => {
    const phases: TimelinePhase[] = [];
    const skillsByLevel: { [key: string]: typeof data.skills } = {
      beginner: [],
      intermediate: [],
      advanced: [],
    };

    // Group skills by level
    data.skills.forEach(skill => {
      const level = skill.level.toLowerCase();
      if (skillsByLevel[level]) {
        skillsByLevel[level].push(skill);
      }
    });

    // Create phases
    if (skillsByLevel.beginner.length > 0) {
      phases.push({
        phase: 'Foundation Phase',
        weeks: skillsByLevel.beginner.reduce((sum, s) => sum + s.duration_weeks, 0),
        skills: skillsByLevel.beginner as Array<{
          name: string;
          level: 'beginner' | 'intermediate' | 'advanced';
          duration_weeks: number;
          resources: string[];
        }>,
      });
    }

    if (skillsByLevel.intermediate.length > 0) {
      phases.push({
        phase: 'Intermediate Phase',
        weeks: skillsByLevel.intermediate.reduce((sum, s) => sum + s.duration_weeks, 0),
        skills: skillsByLevel.intermediate as Array<{
          name: string;
          level: 'beginner' | 'intermediate' | 'advanced';
          duration_weeks: number;
          resources: string[];
        }>,
      });
    }

    if (skillsByLevel.advanced.length > 0) {
      phases.push({
        phase: 'Advanced Phase',
        weeks: skillsByLevel.advanced.reduce((sum, s) => sum + s.duration_weeks, 0),
        skills: skillsByLevel.advanced as Array<{
          name: string;
          level: 'beginner' | 'intermediate' | 'advanced';
          duration_weeks: number;
          resources: string[];
        }>,
      });
    }

    return phases;
  };

  const handleWeekChange = (week: number) => {
    setCurrentWeek(week);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your learning path...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="text-red-600 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Error Loading Learning Path</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => router.push('/results')}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            Go Back to Results
          </button>
        </div>
      </div>
    );
  }

  if (!learningPath) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-gray-600">No learning path found</p>
          <button
            onClick={() => router.push('/results')}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            Go Back to Results
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Your Personalized Learning Path
          </h1>
          <p className="text-gray-600">
            Target Career: <span className="font-semibold text-blue-600">{learningPath.career_name}</span>
          </p>
          <p className="text-sm text-gray-500 mt-1">
            Estimated Duration: {learningPath.timeline_weeks} weeks
          </p>
        </div>

        {/* Main Learning Path Component */}
        <div className="mb-8">
          <LearningPath learningPath={learningPath} />
        </div>

        {/* Skills Timeline */}
        <div className="mb-8">
          <SkillsTimeline timeline={timelineData} currentWeek={currentWeek} />
        </div>

        {/* Progress Tracker */}
        <div className="mb-8">
          <ProgressTracker
            totalWeeks={learningPath.timeline_weeks}
            currentWeek={currentWeek}
            onWeekChange={handleWeekChange}
          />
        </div>

        {/* Action Buttons */}
        <div className="flex justify-between items-center mt-8">
          <button
            onClick={() => router.push(`/results?id=${result_id}`)}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-100 transition"
          >
            Back to Results
          </button>
          <button
            onClick={() => router.push('/careers')}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            Explore Other Careers
          </button>
        </div>
      </div>
    </div>
  );
};

export default LearningPathPage;
