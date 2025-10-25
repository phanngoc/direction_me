import React, { useState, useEffect } from 'react';
import { AssessmentResult, CareerRecommendation } from '../../shared/types';
import RadarChart from './RadarChart';
import FacetBars from './FacetBars';
import IkigaiMap from './IkigaiMap';
import { useResultsAPI } from '../services/results_api';

interface ResultsPageProps {
  resultId: string;
  onBackToChatbot?: () => void;
  onRetakeAssessment?: () => void;
  className?: string;
}

const ResultsPage: React.FC<ResultsPageProps> = ({
  resultId,
  onBackToChatbot,
  onRetakeAssessment,
  className = ''
}) => {
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [recommendations, setRecommendations] = useState<CareerRecommendation[]>([]);
  const [visualizations, setVisualizations] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { 
    getResults,
    getCareerRecommendations,
    getVisualizationData,
    isLoading: apiLoading,
    error: apiError
  } = useResultsAPI();

  useEffect(() => {
    loadResults();
  }, [resultId]);

  const loadResults = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Load results data
      const [resultsData, recommendationsData, visualizationsData] = await Promise.all([
        getResults(resultId),
        getCareerRecommendations(resultId),
        getVisualizationData(resultId)
      ]);

      setResult(resultsData);
      setRecommendations(recommendationsData);
      setVisualizations(visualizationsData);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load results');
    } finally {
      setIsLoading(false);
    }
  };

  const getScoreInterpretation = (score: number) => {
    if (score >= 90) return { level: 'Xuất sắc', color: '#10B981', icon: '🌟' };
    if (score >= 80) return { level: 'Tốt', color: '#22C55E', icon: '👍' };
    if (score >= 70) return { level: 'Khá', color: '#EAB308', icon: '👌' };
    if (score >= 60) return { level: 'Trung bình', color: '#F59E0B', icon: '📈' };
    return { level: 'Cần cải thiện', color: '#EF4444', icon: '💪' };
  };

  const getOverallInsights = () => {
    if (!result) return null;

    const scores = [result.iq_score, result.eq_score, result.dq_score, result.aq_score];
    const average = scores.reduce((sum, score) => sum + score, 0) / scores.length;
    const maxScore = Math.max(...scores);
    const minScore = Math.min(...scores);

    return {
      average,
      maxScore,
      minScore,
      balance: maxScore - minScore,
      interpretation: getScoreInterpretation(average)
    };
  };

  if (isLoading || apiLoading) {
    return (
      <div className={`results-page ${className}`}>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Đang tải kết quả đánh giá...</p>
        </div>
      </div>
    );
  }

  if (error || apiError) {
    return (
      <div className={`results-page ${className}`}>
        <div className="error-container">
          <div className="error-icon">❌</div>
          <h3>Không thể tải kết quả</h3>
          <p>{error || apiError}</p>
          <button onClick={loadResults} className="retry-button">
            Thử lại
          </button>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className={`results-page ${className}`}>
        <div className="no-results">
          <div className="no-results-icon">📊</div>
          <h3>Không tìm thấy kết quả</h3>
          <p>Kết quả đánh giá không tồn tại hoặc đã bị xóa.</p>
        </div>
      </div>
    );
  }

  const insights = getOverallInsights();
  const radarData = {
    labels: ['IQ', 'EQ', 'DQ', 'AQ'],
    datasets: [{
      label: 'Điểm số của bạn',
      data: [result.iq_score, result.eq_score, result.dq_score, result.aq_score]
    }]
  };

  const facetData = {
    facets: ['Trí thông minh', 'Trí tuệ cảm xúc', 'Trí tuệ số', 'Trí tuệ thích nghi'],
    scores: [result.iq_score, result.eq_score, result.dq_score, result.aq_score]
  };

  const ikigaiData = {
    intersections: {
      love_good_at: (result.ikigai_love + result.ikigai_good_at) / 2,
      love_world_needs: (result.ikigai_love + result.ikigai_world_needs) / 2,
      good_at_paid_for: (result.ikigai_good_at + result.ikigai_paid_for) / 2,
      world_needs_paid_for: (result.ikigai_world_needs + result.ikigai_paid_for) / 2
    },
    dimensions: {
      love: result.ikigai_love,
      good_at: result.ikigai_good_at,
      world_needs: result.ikigai_world_needs,
      paid_for: result.ikigai_paid_for
    }
  };

  return (
    <div className={`results-page ${className}`}>
      <div className="results-header">
        <h1 className="results-title">Kết quả đánh giá nghề nghiệp</h1>
        <p className="results-subtitle">Khám phá điểm mạnh và định hướng nghề nghiệp của bạn</p>
        
        <div className="results-actions">
          {onBackToChatbot && (
            <button onClick={onBackToChatbot} className="action-button action-button--secondary">
              <span className="button-icon">💬</span>
              Quay lại chatbot
            </button>
          )}
          {onRetakeAssessment && (
            <button onClick={onRetakeAssessment} className="action-button action-button--primary">
              <span className="button-icon">🔄</span>
              Làm lại đánh giá
            </button>
          )}
        </div>
      </div>

      {insights && (
        <div className="overall-summary">
          <div className="summary-card">
            <div className="summary-header">
              <h2>Tổng quan kết quả</h2>
              <div className="overall-score">
                <span className="score-value">{insights.average.toFixed(1)}%</span>
                <span className="score-level" style={{ color: insights.interpretation.color }}>
                  {insights.interpretation.icon} {insights.interpretation.level}
                </span>
              </div>
            </div>
            
            <div className="summary-stats">
              <div className="stat-item">
                <span className="stat-label">Điểm cao nhất:</span>
                <span className="stat-value">{insights.maxScore.toFixed(1)}%</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Điểm thấp nhất:</span>
                <span className="stat-value">{insights.minScore.toFixed(1)}%</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Độ cân bằng:</span>
                <span className="stat-value">
                  {insights.balance < 20 ? 'Cân bằng' : 'Cần cân bằng'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="visualizations-section">
        <h2 className="section-title">Biểu đồ phân tích</h2>
        
        <div className="visualization-grid">
          <div className="visualization-item">
            <RadarChart 
              data={radarData}
              title="Biểu đồ Radar - 4 Chỉ số"
              height={400}
            />
          </div>
          
          <div className="visualization-item">
            <FacetBars 
              data={facetData}
              title="Biểu đồ Cột - Các Khía cạnh"
              height={400}
            />
          </div>
          
          <div className="visualization-item visualization-item--full">
            <IkigaiMap 
              data={ikigaiData}
              title="Bản đồ Ikigai - Tìm ra mục đích sống"
              height={500}
            />
          </div>
        </div>
      </div>

      {recommendations.length > 0 && (
        <div className="recommendations-section">
          <h2 className="section-title">Gợi ý nghề nghiệp</h2>
          
          <div className="recommendations-grid">
            {recommendations.map((rec, index) => (
              <div key={rec.id} className="recommendation-card">
                <div className="recommendation-header">
                  <h3 className="recommendation-title">{rec.career_title}</h3>
                  <div className="recommendation-score">
                    <span className="score-label">Độ phù hợp:</span>
                    <span className="score-value">{rec.alignment_score.toFixed(1)}%</span>
                  </div>
                </div>
                
                <p className="recommendation-description">{rec.career_description}</p>
                
                <div className="recommendation-details">
                  <div className="detail-item">
                    <span className="detail-label">Kỹ năng cần thiết:</span>
                    <div className="skills-list">
                      {rec.required_skills.map((skill, skillIndex) => (
                        <span key={skillIndex} className="skill-tag">{skill}</span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="detail-item">
                    <span className="detail-label">Nhu cầu thị trường:</span>
                    <span className="detail-value">{rec.market_demand}</span>
                  </div>
                  
                  {rec.salary_range_min && rec.salary_range_max && (
                    <div className="detail-item">
                      <span className="detail-label">Mức lương:</span>
                      <span className="detail-value">
                        {rec.salary_range_min.toLocaleString()} - {rec.salary_range_max.toLocaleString()} VNĐ
                      </span>
                    </div>
                  )}
                </div>
                
                <p className="recommendation-explanation">{rec.explanation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="results-footer">
        <div className="footer-info">
          <p>Kết quả được tạo lúc: {new Date(result.created_at).toLocaleString('vi-VN')}</p>
          <p>Độ chính xác: {result.consistency_score ? (result.consistency_score * 100).toFixed(1) : 'N/A'}%</p>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
