import React, { useRef, useEffect } from 'react';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

interface ChartDataPoint {
  iq_score: number;
  eq_score: number;
  dq_score: number;
  aq_score: number;
  calculated_at: string;
}

interface ProgressChartProps {
  history: ChartDataPoint[];
}

const ProgressChart: React.FC<ProgressChartProps> = ({ history }) => {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    if (!chartRef.current || !history || history.length === 0) return;

    // Destroy existing chart
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = chartRef.current.getContext('2d');
    if (!ctx) return;

    // Prepare data (reverse to show oldest first)
    const sortedHistory = [...history].reverse();
    const labels = sortedHistory.map((h) => {
      const date = new Date(h.calculated_at);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });

    chartInstance.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'IQ',
            data: sortedHistory.map((h) => h.iq_score),
            borderColor: 'rgb(59, 130, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            tension: 0.3,
          },
          {
            label: 'EQ',
            data: sortedHistory.map((h) => h.eq_score),
            borderColor: 'rgb(16, 185, 129)',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            tension: 0.3,
          },
          {
            label: 'DQ',
            data: sortedHistory.map((h) => h.dq_score),
            borderColor: 'rgb(249, 115, 22)',
            backgroundColor: 'rgba(249, 115, 22, 0.1)',
            tension: 0.3,
          },
          {
            label: 'AQ',
            data: sortedHistory.map((h) => h.aq_score),
            borderColor: 'rgb(168, 85, 247)',
            backgroundColor: 'rgba(168, 85, 247, 0.1)',
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: false,
          },
          tooltip: {
            mode: 'index',
            intersect: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            title: {
              display: true,
              text: 'Score',
            },
          },
          x: {
            title: {
              display: true,
              text: 'Assessment Date',
            },
          },
        },
        interaction: {
          mode: 'nearest',
          axis: 'x',
          intersect: false,
        },
      },
    });

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [history]);

  if (!history || history.length === 0) {
    return (
      <div className="bg-gray-50 p-8 rounded-lg text-center text-gray-500">
        No assessment history available yet. Complete more assessments to see your progress chart.
      </div>
    );
  }

  return (
    <div className="w-full bg-white p-4 rounded-lg border border-gray-200">
      <div className="relative" style={{ height: '400px' }}>
        <canvas ref={chartRef}></canvas>
      </div>
    </div>
  );
};

export default ProgressChart;
