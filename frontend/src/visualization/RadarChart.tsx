import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

interface RadarChartProps {
  data: {
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      backgroundColor?: string;
      borderColor?: string;
      borderWidth?: number;
    }[];
  };
  className?: string;
  title?: string;
  height?: number;
}

const RadarChart: React.FC<RadarChartProps> = ({
  data,
  className = '',
  title = 'Biểu đồ Radar - 4 Chỉ số',
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

    chartRef.current = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: data.labels,
        datasets: data.datasets.map(dataset => ({
          ...dataset,
          backgroundColor: dataset.backgroundColor || 'rgba(59, 130, 246, 0.2)',
          borderColor: dataset.borderColor || 'rgba(59, 130, 246, 1)',
          borderWidth: dataset.borderWidth || 2,
          pointBackgroundColor: 'rgba(59, 130, 246, 1)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(59, 130, 246, 1)',
          pointRadius: 4,
          pointHoverRadius: 6
        }))
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
            display: true,
            position: 'bottom',
            labels: {
              usePointStyle: true,
              padding: 20
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#fff',
            bodyColor: '#fff',
            borderColor: 'rgba(59, 130, 246, 1)',
            borderWidth: 1,
            callbacks: {
              label: function(context) {
                const label = context.dataset.label || '';
                const value = context.parsed.r;
                return `${label}: ${value.toFixed(1)}%`;
              }
            }
          }
        },
        scales: {
          r: {
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
            },
            angleLines: {
              color: 'rgba(107, 114, 128, 0.2)',
              lineWidth: 1
            },
            pointLabels: {
              color: '#374151',
              font: {
                size: 14,
                weight: 'bold'
              },
              padding: 10
            }
          }
        },
        elements: {
          line: {
            tension: 0.1
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

  return (
    <div className={`radar-chart ${className}`}>
      <div className="radar-chart__container">
        <canvas
          ref={canvasRef}
          style={{ height: `${height}px` }}
          aria-label={title}
          role="img"
        />
      </div>
      
      <div className="radar-chart__info">
        <div className="chart-info">
          <h4 className="chart-info__title">Giải thích biểu đồ</h4>
          <ul className="chart-info__list">
            <li>
              <span className="info-label">🧠 IQ (Trí thông minh):</span>
              <span>Khả năng tư duy logic và giải quyết vấn đề</span>
            </li>
            <li>
              <span className="info-label">❤️ EQ (Trí tuệ cảm xúc):</span>
              <span>Khả năng hiểu và quản lý cảm xúc</span>
            </li>
            <li>
              <span className="info-label">💻 DQ (Trí tuệ số):</span>
              <span>Khả năng sử dụng công nghệ và số hóa</span>
            </li>
            <li>
              <span className="info-label">🔄 AQ (Trí tuệ thích nghi):</span>
              <span>Khả năng thích nghi và học hỏi</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default RadarChart;
