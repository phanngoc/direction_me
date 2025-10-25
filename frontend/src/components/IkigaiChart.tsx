/**
 * Ikigai Chart Component for MyWay Career Assessment System.
 * Displays Ikigai scores in a radar chart format.
 */
import React, { useEffect, useRef } from 'react';
import { Chart, registerables } from 'chart.js';

// Register Chart.js components
Chart.register(...registerables);

interface IkigaiScores {
  ikigai_love: number;
  ikigai_good_at: number;
  ikigai_world_needs: number;
  ikigai_paid_for: number;
  ikigai_harmonic: number;
  ikigai_geometric: number;
}

interface IkigaiChartProps {
  scores: IkigaiScores;
  width?: number;
  height?: number;
  className?: string;
}

const IkigaiChart: React.FC<IkigaiChartProps> = ({
  scores,
  width = 400,
  height = 400,
  className = ''
}) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstanceRef = useRef<Chart | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    // Destroy existing chart
    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');
    if (!ctx) return;

    // Prepare data for radar chart
    const data = {
      labels: [
        'Đam mê (Love)',
        'Tài năng (Good at)',
        'Nhu cầu xã hội (World needs)',
        'Khả năng kiếm tiền (Paid for)'
      ],
      datasets: [
        {
          label: 'Điểm Ikigai',
          data: [
            scores.ikigai_love,
            scores.ikigai_good_at,
            scores.ikigai_world_needs,
            scores.ikigai_paid_for
          ],
          backgroundColor: 'rgba(99, 102, 241, 0.2)',
          borderColor: 'rgba(99, 102, 241, 1)',
          borderWidth: 2,
          pointBackgroundColor: 'rgba(99, 102, 241, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8
        }
      ]
    };

    const config = {
      type: 'radar' as const,
      data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Phân tích Ikigai của bạn',
            font: {
              size: 18,
              weight: 'bold' as const
            },
            color: '#1f2937'
          },
          legend: {
            display: true,
            position: 'bottom' as const,
            labels: {
              font: {
                size: 12
              },
              color: '#6b7280'
            }
          },
          tooltip: {
            callbacks: {
              label: function(context: any) {
                const label = context.dataset.label || '';
                const value = context.parsed.r;
                return `${label}: ${value.toFixed(1)}/100`;
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
              font: {
                size: 11
              },
              color: '#6b7280'
            },
            grid: {
              color: 'rgba(107, 114, 128, 0.2)'
            },
            angleLines: {
              color: 'rgba(107, 114, 128, 0.2)'
            },
            pointLabels: {
              font: {
                size: 12,
                weight: 'bold' as const
              },
              color: '#374151'
            }
          }
        },
        elements: {
          line: {
            tension: 0.1
          }
        }
      }
    };

    chartInstanceRef.current = new Chart(ctx, config);

    // Cleanup function
    return () => {
      if (chartInstanceRef.current) {
        chartInstanceRef.current.destroy();
      }
    };
  }, [scores]);

  return (
    <div className={`ikigai-chart-container ${className}`}>
      <div className="relative">
        <canvas
          ref={chartRef}
          width={width}
          height={height}
          className="max-w-full h-auto"
        />
      </div>
      
      {/* Ikigai Summary */}
      <div className="mt-6 grid grid-cols-2 gap-4 text-sm">
        <div className="bg-blue-50 p-3 rounded-lg">
          <div className="font-semibold text-blue-900">Harmonic Mean</div>
          <div className="text-2xl font-bold text-blue-600">
            {scores.ikigai_harmonic.toFixed(1)}
          </div>
          <div className="text-blue-700 text-xs">
            Cân bằng tổng thể
          </div>
        </div>
        
        <div className="bg-green-50 p-3 rounded-lg">
          <div className="font-semibold text-green-900">Geometric Mean</div>
          <div className="text-2xl font-bold text-green-600">
            {scores.ikigai_geometric.toFixed(1)}
          </div>
          <div className="text-green-700 text-xs">
            Phát triển đồng đều
          </div>
        </div>
      </div>

      {/* Individual Scores */}
      <div className="mt-4 grid grid-cols-2 gap-3 text-xs">
        <div className="flex justify-between items-center p-2 bg-red-50 rounded">
          <span className="text-red-700 font-medium">Đam mê</span>
          <span className="text-red-900 font-bold">{scores.ikigai_love.toFixed(1)}</span>
        </div>
        
        <div className="flex justify-between items-center p-2 bg-blue-50 rounded">
          <span className="text-blue-700 font-medium">Tài năng</span>
          <span className="text-blue-900 font-bold">{scores.ikigai_good_at.toFixed(1)}</span>
        </div>
        
        <div className="flex justify-between items-center p-2 bg-green-50 rounded">
          <span className="text-green-700 font-medium">Nhu cầu xã hội</span>
          <span className="text-green-900 font-bold">{scores.ikigai_world_needs.toFixed(1)}</span>
        </div>
        
        <div className="flex justify-between items-center p-2 bg-yellow-50 rounded">
          <span className="text-yellow-700 font-medium">Khả năng kiếm tiền</span>
          <span className="text-yellow-900 font-bold">{scores.ikigai_paid_for.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};

export default IkigaiChart;