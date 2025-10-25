import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

interface FacetBarsProps {
  data: {
    facets: string[];
    scores: number[];
  };
  className?: string;
  title?: string;
  height?: number;
}

const FacetBars: React.FC<FacetBarsProps> = ({
  data,
  className = '',
  title = 'Biểu đồ Cột - Các Khía cạnh',
  height = 400
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chartRef = useRef<Chart | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    // Destroy existing chart
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    // Create new chart
    const ctx = canvasRef.current.getContext('2d');
    if (!ctx) return;

    // Define colors for each facet
    const colors = [
      'rgba(59, 130, 246, 0.8)',   // Blue for IQ
      'rgba(239, 68, 68, 0.8)',    // Red for EQ
      'rgba(16, 185, 129, 0.8)',   // Green for DQ
      'rgba(245, 158, 11, 0.8)'    // Yellow for AQ
    ];

    const borderColors = [
      'rgba(59, 130, 246, 1)',
      'rgba(239, 68, 68, 1)',
      'rgba(16, 185, 129, 1)',
      'rgba(245, 158, 11, 1)'
    ];

    chartRef.current = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.facets,
        datasets: [{
          label: 'Điểm số (%)',
          data: data.scores,
          backgroundColor: colors,
          borderColor: borderColors,
          borderWidth: 2,
          borderRadius: 8,
          borderSkipped: false
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: title,
            font: {
              size: 16,
              weight: 'bold'
            },
            color: '#374151'
          },
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#fff',
            bodyColor: '#fff',
            borderColor: 'rgba(59, 130, 246, 1)',
            borderWidth: 1,
            callbacks: {
              title: function(context) {
                return context[0].label;
              },
              label: function(context) {
                const value = context.parsed.y;
                return `Điểm số: ${value.toFixed(1)}%`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            },
            ticks: {
              color: '#374151',
              font: {
                size: 14,
                weight: 'bold'
              }
            }
          },
          y: {
            beginAtZero: true,
            min: 0,
            max: 100,
            ticks: {
              stepSize: 20,
              color: '#6B7280',
              font: {
                size: 12
              },
              callback: function(value) {
                return value + '%';
              }
            },
            grid: {
              color: 'rgba(107, 114, 128, 0.2)',
              lineWidth: 1
            }
          }
        },
        animation: {
          duration: 2000,
          easing: 'easeInOutQuart'
        },
        interaction: {
          intersect: false
        }
      }
    });

    // Cleanup function
    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
      }
    };
  }, [data, title]);

  // Calculate performance insights
  const getPerformanceInsights = () => {
    const maxScore = Math.max(...data.scores);
    const minScore = Math.min(...data.scores);
    const avgScore = data.scores.reduce((sum, score) => sum + score, 0) / data.scores.length;
    
    const maxIndex = data.scores.indexOf(maxScore);
    const minIndex = data.scores.indexOf(minScore);
    
    return {
      strongest: data.facets[maxIndex],
      strongestScore: maxScore,
      weakest: data.facets[minIndex],
      weakestScore: minScore,
      average: avgScore
    };
  };

  const insights = getPerformanceInsights();

  return (
    <div className={`facet-bars ${className}`}>
      <div className="facet-bars__container">
        <canvas
          ref={canvasRef}
          style={{ height: `${height}px` }}
          aria-label={title}
          role="img"
        />
      </div>
      
      <div className="facet-bars__insights">
        <div className="performance-insights">
          <h4 className="insights-title">Phân tích hiệu suất</h4>
          
          <div className="insight-item insight-item--strongest">
            <div className="insight-icon">🏆</div>
            <div className="insight-content">
              <span className="insight-label">Điểm mạnh nhất:</span>
              <span className="insight-value">{insights.strongest} ({insights.strongestScore.toFixed(1)}%)</span>
            </div>
          </div>
          
          <div className="insight-item insight-item--weakest">
            <div className="insight-icon">📈</div>
            <div className="insight-content">
              <span className="insight-label">Cần cải thiện:</span>
              <span className="insight-value">{insights.weakest} ({insights.weakestScore.toFixed(1)}%)</span>
            </div>
          </div>
          
          <div className="insight-item insight-item--average">
            <div className="insight-icon">📊</div>
            <div className="insight-content">
              <span className="insight-label">Điểm trung bình:</span>
              <span className="insight-value">{insights.average.toFixed(1)}%</span>
            </div>
          </div>
        </div>
        
        <div className="performance-recommendations">
          <h4 className="recommendations-title">Gợi ý phát triển</h4>
          <ul className="recommendations-list">
            {insights.weakestScore < 60 && (
              <li className="recommendation-item">
                <span className="recommendation-icon">💡</span>
                <span>Hãy tập trung phát triển kỹ năng {insights.weakest} để cân bằng hồ sơ năng lực</span>
              </li>
            )}
            {insights.average >= 80 && (
              <li className="recommendation-item">
                <span className="recommendation-icon">🎯</span>
                <span>Bạn có hồ sơ năng lực rất tốt! Hãy tận dụng điểm mạnh để phát triển sự nghiệp</span>
              </li>
            )}
            <li className="recommendation-item">
              <span className="recommendation-icon">🔄</span>
              <span>Thường xuyên đánh giá lại để theo dõi sự tiến bộ</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FacetBars;
