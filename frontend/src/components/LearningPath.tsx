/**
 * Learning Path Component for MyWay Career Assessment System.
 * Displays personalized learning paths with skills, projects, and habits.
 */
import React, { useState, useEffect } from 'react';
import { apiClient } from '../services/api';

interface Skill {
  name: string;
  description: string;
  weeks: number;
  priority: 'high' | 'medium' | 'low';
  category: string;
  resources: string[];
  projects: string[];
}

interface Project {
  name: string;
  description: string;
  skills_required: string[];
  duration_weeks: number;
  difficulty: string;
  priority: string;
}

interface Habit {
  name: string;
  description: string;
  frequency: string;
  duration_weeks: number;
  priority: string;
}

interface LearningPath {
  id: string;
  career_name: string;
  skills: Skill[];
  projects: Project[];
  habits: Habit[];
  timeline_weeks: number;
  priority: string;
  created_at: string;
}

interface LearningPathProps {
  assessmentResultId: string;
  onPathSelect?: (path: LearningPath) => void;
  className?: string;
}

const LearningPath: React.FC<LearningPathProps> = ({
  assessmentResultId,
  onPathSelect,
  className = ''
}) => {
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [selectedPath, setSelectedPath] = useState<LearningPath | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'skills' | 'projects' | 'habits'>('skills');

  useEffect(() => {
    loadLearningPaths();
  }, [assessmentResultId]);

  const loadLearningPaths = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.get(`/learning-paths/${assessmentResultId}`);
      
      if (response.success) {
        setLearningPaths(response.data);
        if (response.data.length > 0) {
          setSelectedPath(response.data[0]);
        }
      } else {
        setError('Không thể tải lộ trình học tập');
      }
    } catch (err) {
      console.error('Error loading learning paths:', err);
      setError('Có lỗi xảy ra khi tải lộ trình học tập');
    } finally {
      setLoading(false);
    }
  };

  const generateNewPaths = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await apiClient.post(`/learning-paths/${assessmentResultId}/generate`);
      
      if (response.success) {
        setLearningPaths(response.data);
        if (response.data.length > 0) {
          setSelectedPath(response.data[0]);
        }
      } else {
        setError('Không thể tạo lộ trình học tập mới');
      }
    } catch (err) {
      console.error('Error generating learning paths:', err);
      setError('Có lỗi xảy ra khi tạo lộ trình học tập');
    } finally {
      setLoading(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case 'high': return 'Ưu tiên cao';
      case 'medium': return 'Ưu tiên trung bình';
      case 'low': return 'Ưu tiên thấp';
      default: return priority;
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className={`learning-path ${className}`}>
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải lộ trình học tập...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`learning-path ${className}`}>
        <div className="text-center py-8">
          <div className="text-red-500 text-4xl mb-4">⚠️</div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Không thể tải lộ trình học tập
          </h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={loadLearningPaths}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Thử lại
          </button>
        </div>
      </div>
    );
  }

  if (learningPaths.length === 0) {
    return (
      <div className={`learning-path ${className}`}>
        <div className="text-center py-8">
          <div className="text-gray-400 text-4xl mb-4">📚</div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Chưa có lộ trình học tập
          </h3>
          <p className="text-gray-600 mb-4">
            Tạo lộ trình học tập cá nhân hóa dựa trên kết quả đánh giá của bạn
          </p>
          <button
            onClick={generateNewPaths}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Tạo lộ trình học tập
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`learning-path ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          Lộ trình học tập cá nhân hóa
        </h2>
        <button
          onClick={generateNewPaths}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Tạo lộ trình mới
        </button>
      </div>

      {/* Path Selection */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          Chọn nghề nghiệp mục tiêu
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {learningPaths.map((path) => (
            <div
              key={path.id}
              className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                selectedPath?.id === path.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => {
                setSelectedPath(path);
                onPathSelect?.(path);
              }}
            >
              <h4 className="font-semibold text-gray-900 mb-2">
                {path.career_name}
              </h4>
              <div className="flex items-center justify-between text-sm text-gray-600">
                <span>{path.timeline_weeks} tuần</span>
                <span className={`px-2 py-1 rounded text-xs ${getPriorityColor(path.priority)}`}>
                  {getPriorityLabel(path.priority)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Path Details */}
      {selectedPath && (
        <div className="bg-white rounded-lg shadow-sm border">
          {/* Path Header */}
          <div className="p-6 border-b">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900">
                {selectedPath.career_name}
              </h3>
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <span>{selectedPath.timeline_weeks} tuần</span>
                <span className={`px-2 py-1 rounded ${getPriorityColor(selectedPath.priority)}`}>
                  {getPriorityLabel(selectedPath.priority)}
                </span>
              </div>
            </div>
            
            {/* Progress Overview */}
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-blue-600">{selectedPath.skills.length}</div>
                <div className="text-sm text-gray-600">Kỹ năng</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">{selectedPath.projects.length}</div>
                <div className="text-sm text-gray-600">Dự án</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">{selectedPath.habits.length}</div>
                <div className="text-sm text-gray-600">Thói quen</div>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="border-b">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'skills', label: 'Kỹ năng', count: selectedPath.skills.length },
                { id: 'projects', label: 'Dự án', count: selectedPath.projects.length },
                { id: 'habits', label: 'Thói quen', count: selectedPath.habits.length }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.label} ({tab.count})
                </button>
              ))}
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'skills' && (
              <div className="space-y-4">
                {selectedPath.skills.map((skill, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">{skill.name}</h4>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs ${getPriorityColor(skill.priority)}`}>
                          {getPriorityLabel(skill.priority)}
                        </span>
                        <span className="text-sm text-gray-600">{skill.weeks} tuần</span>
                      </div>
                    </div>
                    <p className="text-gray-600 mb-3">{skill.description}</p>
                    {skill.resources.length > 0 && (
                      <div className="mb-2">
                        <h5 className="text-sm font-medium text-gray-700 mb-1">Tài liệu học tập:</h5>
                        <ul className="text-sm text-gray-600 list-disc list-inside">
                          {skill.resources.map((resource, idx) => (
                            <li key={idx}>{resource}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {skill.projects.length > 0 && (
                      <div>
                        <h5 className="text-sm font-medium text-gray-700 mb-1">Dự án thực hành:</h5>
                        <ul className="text-sm text-gray-600 list-disc list-inside">
                          {skill.projects.map((project, idx) => (
                            <li key={idx}>{project}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'projects' && (
              <div className="space-y-4">
                {selectedPath.projects.map((project, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">{project.name}</h4>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs ${getDifficultyColor(project.difficulty)}`}>
                          {project.difficulty}
                        </span>
                        <span className="text-sm text-gray-600">{project.duration_weeks} tuần</span>
                      </div>
                    </div>
                    <p className="text-gray-600 mb-3">{project.description}</p>
                    <div>
                      <h5 className="text-sm font-medium text-gray-700 mb-1">Kỹ năng cần thiết:</h5>
                      <div className="flex flex-wrap gap-1">
                        {project.skills_required.map((skill, idx) => (
                          <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'habits' && (
              <div className="space-y-4">
                {selectedPath.habits.map((habit, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-900">{habit.name}</h4>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs ${getPriorityColor(habit.priority)}`}>
                          {getPriorityLabel(habit.priority)}
                        </span>
                        <span className="text-sm text-gray-600">{habit.frequency}</span>
                      </div>
                    </div>
                    <p className="text-gray-600 mb-2">{habit.description}</p>
                    <div className="text-sm text-gray-500">
                      Thời gian: {habit.duration_weeks} tuần
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default LearningPath;