'use client';

import React from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

interface RadarChartProps {
  data: {
    iq_score: number;
    eq_score: number;
    dq_score: number;
    aq_score: number;
  };
  className?: string;
}

export default function RadarChart({ data, className = '' }: RadarChartProps) {
  const chartData = {
    labels: ['IQ', 'EQ', 'DQ', 'AQ'],
    datasets: [
      {
        label: 'Điểm số',
        data: [data.iq_score, data.eq_score, data.dq_score, data.aq_score],
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(59, 130, 246, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(59, 130, 246, 1)',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
        min: 0,
        ticks: {
          stepSize: 20,
          color: '#6B7280',
          font: {
            size: 12,
          },
        },
        grid: {
          color: '#E5E7EB',
        },
        angleLines: {
          color: '#E5E7EB',
        },
        pointLabels: {
          color: '#374151',
          font: {
            size: 14,
            weight: 'bold' as const,
          },
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            const label = context.dataset.label || '';
            const value = context.parsed.r;
            return `${label}: ${value.toFixed(1)} điểm`;
          },
        },
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    },
    elements: {
      point: {
        radius: 6,
        hoverRadius: 8,
      },
    },
  };

  return (
    <div className={`w-full h-96 ${className}`}>
      <Radar data={chartData} options={options} />
    </div>
  );
}