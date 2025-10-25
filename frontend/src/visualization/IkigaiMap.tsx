import React, { useEffect, useRef } from 'react';

interface IkigaiMapProps {
  data: {
    intersections: {
      love_good_at: number;
      love_world_needs: number;
      good_at_paid_for: number;
      world_needs_paid_for: number;
    };
    dimensions: {
      love: number;
      good_at: number;
      world_needs: number;
      paid_for: number;
    };
  };
  className?: string;
  title?: string;
  height?: number;
}

const IkigaiMap: React.FC<IkigaiMapProps> = ({
  data,
  className = '',
  title = 'Bản đồ Ikigai - Tìm ra mục đích sống',
  height = 500
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = height;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Ikigai map
    drawIkigaiMap(ctx, canvas.width, canvas.height, data);
  }, [data, height]);

  const drawIkigaiMap = (
    ctx: CanvasRenderingContext2D, 
    width: number, 
    height: number, 
    data: any
  ) => {
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;

    // Draw outer circle
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.stroke();

    // Draw inner circle
    ctx.strokeStyle = '#6B7280';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 0.5, 0, 2 * Math.PI);
    ctx.stroke();

    // Draw axes
    ctx.strokeStyle = '#9CA3AF';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(centerX - radius, centerY);
    ctx.lineTo(centerX + radius, centerY);
    ctx.moveTo(centerX, centerY - radius);
    ctx.lineTo(centerX, centerY + radius);
    ctx.stroke();

    // Draw intersection areas
    drawIntersection(ctx, centerX, centerY, radius, data.intersections);

    // Draw dimension labels
    drawDimensionLabels(ctx, centerX, centerY, radius, data.dimensions);

    // Draw user position
    drawUserPosition(ctx, centerX, centerY, radius, data);
  };

  const drawIntersection = (
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    radius: number,
    intersections: any
  ) => {
    const innerRadius = radius * 0.5;
    const colors = {
      love_good_at: 'rgba(239, 68, 68, 0.3)',
      love_world_needs: 'rgba(16, 185, 129, 0.3)',
      good_at_paid_for: 'rgba(59, 130, 246, 0.3)',
      world_needs_paid_for: 'rgba(245, 158, 11, 0.3)'
    };

    // Draw each intersection
    Object.entries(intersections).forEach(([key, value], index) => {
      const angle = (index * Math.PI) / 2;
      const x = centerX + Math.cos(angle) * innerRadius;
      const y = centerY + Math.sin(angle) * innerRadius;
      
      ctx.fillStyle = colors[key as keyof typeof colors];
      ctx.beginPath();
      ctx.arc(x, y, (value / 100) * innerRadius * 0.3, 0, 2 * Math.PI);
      ctx.fill();
    });
  };

  const drawDimensionLabels = (
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    radius: number,
    dimensions: any
  ) => {
    const labels = [
      { text: 'Tôi yêu thích', key: 'love', angle: -Math.PI / 2, color: '#EF4444' },
      { text: 'Tôi giỏi', key: 'good_at', angle: 0, color: '#3B82F6' },
      { text: 'Thế giới cần', key: 'world_needs', angle: Math.PI / 2, color: '#10B981' },
      { text: 'Được trả lương', key: 'paid_for', angle: Math.PI, color: '#F59E0B' }
    ];

    labels.forEach((label, index) => {
      const x = centerX + Math.cos(label.angle) * (radius + 30);
      const y = centerY + Math.sin(label.angle) * (radius + 30);

      // Draw dimension score
      ctx.fillStyle = label.color;
      ctx.font = 'bold 14px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(`${label.text}: ${dimensions[label.key].toFixed(0)}%`, x, y);

      // Draw dimension line
      ctx.strokeStyle = label.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x - Math.cos(label.angle) * 20, y - Math.sin(label.angle) * 20);
      ctx.stroke();
    });
  };

  const drawUserPosition = (
    ctx: CanvasRenderingContext2D,
    centerX: number,
    centerY: number,
    radius: number,
    data: any
  ) => {
    // Calculate user position based on dimensions
    const x = centerX + ((data.dimensions.good_at - data.dimensions.love) / 100) * radius * 0.8;
    const y = centerY + ((data.dimensions.world_needs - data.dimensions.paid_for) / 100) * radius * 0.8;

    // Draw user position
    ctx.fillStyle = '#EF4444';
    ctx.beginPath();
    ctx.arc(x, y, 8, 0, 2 * Math.PI);
    ctx.fill();

    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, 8, 0, 2 * Math.PI);
    ctx.stroke();

    // Draw label
    ctx.fillStyle = '#374151';
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Vị trí của bạn', x, y - 15);
  };

  // Calculate Ikigai insights
  const getIkigaiInsights = () => {
    const { intersections, dimensions } = data;
    
    const maxIntersection = Math.max(...Object.values(intersections));
    const maxKey = Object.keys(intersections).find(
      key => intersections[key] === maxIntersection
    );
    
    const insights = {
      strongest_intersection: maxKey,
      strongest_score: maxIntersection,
      balance_score: Math.min(...Object.values(dimensions)),
      overall_score: Object.values(dimensions).reduce((sum, val) => sum + val, 0) / 4
    };
    
    return insights;
  };

  const insights = getIkigaiInsights();

  return (
    <div className={`ikigai-map ${className}`}>
      <div className="ikigai-map__container">
        <h3 className="ikigai-map__title">{title}</h3>
        <canvas
          ref={canvasRef}
          style={{ height: `${height}px`, width: '100%' }}
          aria-label={title}
          role="img"
        />
      </div>
      
      <div className="ikigai-map__insights">
        <div className="ikigai-insights">
          <h4 className="insights-title">Phân tích Ikigai</h4>
          
          <div className="insight-item">
            <div className="insight-icon">🎯</div>
            <div className="insight-content">
              <span className="insight-label">Giao điểm mạnh nhất:</span>
              <span className="insight-value">
                {insights.strongest_intersection?.replace('_', ' & ')} ({insights.strongest_score.toFixed(1)}%)
              </span>
            </div>
          </div>
          
          <div className="insight-item">
            <div className="insight-icon">⚖️</div>
            <div className="insight-content">
              <span className="insight-label">Điểm cân bằng:</span>
              <span className="insight-value">{insights.balance_score.toFixed(1)}%</span>
            </div>
          </div>
          
          <div className="insight-item">
            <div className="insight-icon">📊</div>
            <div className="insight-content">
              <span className="insight-label">Điểm tổng thể:</span>
              <span className="insight-value">{insights.overall_score.toFixed(1)}%</span>
            </div>
          </div>
        </div>
        
        <div className="ikigai-recommendations">
          <h4 className="recommendations-title">Gợi ý phát triển</h4>
          <ul className="recommendations-list">
            {insights.overall_score >= 80 && (
              <li className="recommendation-item">
                <span className="recommendation-icon">🌟</span>
                <span>Bạn đã tìm thấy Ikigai của mình! Hãy phát triển sâu hơn trong lĩnh vực này</span>
              </li>
            )}
            {insights.balance_score < 60 && (
              <li className="recommendation-item">
                <span className="recommendation-icon">⚖️</span>
                <span>Cần cân bằng hơn giữa các khía cạnh để tìm ra Ikigai hoàn hảo</span>
              </li>
            )}
            <li className="recommendation-item">
              <span className="recommendation-icon">🔄</span>
              <span>Ikigai là hành trình, hãy tiếp tục khám phá và phát triển</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default IkigaiMap;
