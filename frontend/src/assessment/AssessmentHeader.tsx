import React from 'react';

interface AssessmentHeaderProps {
  module: string;
  onExit?: () => void;
  onMinimize?: () => void;
}

const AssessmentHeader: React.FC<AssessmentHeaderProps> = ({
  module,
  onExit,
  onMinimize
}) => {
  const getModuleInfo = (module: string) => {
    const moduleInfo = {
      IQ: {
        name: 'Trí thông minh (IQ)',
        description: 'Đánh giá khả năng tư duy logic và giải quyết vấn đề',
        icon: '🧠',
        color: '#3B82F6'
      },
      EQ: {
        name: 'Trí tuệ cảm xúc (EQ)',
        description: 'Đánh giá khả năng hiểu và quản lý cảm xúc',
        icon: '❤️',
        color: '#EF4444'
      },
      DQ: {
        name: 'Trí tuệ số (DQ)',
        description: 'Đánh giá khả năng sử dụng công nghệ và số hóa',
        icon: '💻',
        color: '#10B981'
      },
      AQ: {
        name: 'Trí tuệ thích nghi (AQ)',
        description: 'Đánh giá khả năng thích nghi và học hỏi',
        icon: '🔄',
        color: '#F59E0B'
      }
    };
    
    return moduleInfo[module as keyof typeof moduleInfo] || moduleInfo.IQ;
  };

  const moduleInfo = getModuleInfo(module);

  return (
    <div className="assessment-header" style={{ borderLeftColor: moduleInfo.color }}>
      <div className="assessment-header__content">
        <div className="assessment-header__module">
          <span className="assessment-header__icon">{moduleInfo.icon}</span>
          <div className="assessment-header__info">
            <h2 className="assessment-header__title">{moduleInfo.name}</h2>
            <p className="assessment-header__description">{moduleInfo.description}</p>
          </div>
        </div>
        
        <div className="assessment-header__actions">
          {onMinimize && (
            <button
              onClick={onMinimize}
              className="assessment-header__action"
              title="Thu nhỏ"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </button>
          )}
          
          {onExit && (
            <button
              onClick={onExit}
              className="assessment-header__action assessment-header__action--exit"
              title="Thoát đánh giá"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          )}
        </div>
      </div>
      
      <div className="assessment-header__instructions">
        <div className="instruction-item">
          <span className="instruction-icon">⏱️</span>
          <span>Không có giới hạn thời gian, hãy trả lời cẩn thận</span>
        </div>
        <div className="instruction-item">
          <span className="instruction-icon">📝</span>
          <span>Trả lời trung thực để có kết quả chính xác nhất</span>
        </div>
        <div className="instruction-item">
          <span className="instruction-icon">🔄</span>
          <span>Có thể quay lại sửa câu trả lời trước đó</span>
        </div>
      </div>
    </div>
  );
};

export default AssessmentHeader;
