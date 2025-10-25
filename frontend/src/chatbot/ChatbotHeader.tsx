import React from 'react';

interface ChatbotHeaderProps {
  isConnected: boolean;
  sessionId: string;
  onMinimize?: () => void;
  onClose?: () => void;
}

const ChatbotHeader: React.FC<ChatbotHeaderProps> = ({
  isConnected,
  sessionId,
  onMinimize,
  onClose
}) => {
  const getConnectionStatus = () => {
    if (isConnected) {
      return {
        text: 'Đã kết nối',
        className: 'status--connected',
        icon: '🟢'
      };
    } else {
      return {
        text: 'Đang kết nối...',
        className: 'status--connecting',
        icon: '🟡'
      };
    }
  };

  const status = getConnectionStatus();

  return (
    <div className="chatbot-header">
      <div className="chatbot-header__info">
        <div className="chatbot-header__title">
          <span className="chatbot-header__icon">🤖</span>
          <span className="chatbot-header__name">MyWay Assistant</span>
        </div>
        
        <div className="chatbot-header__status">
          <span className={`status ${status.className}`}>
            <span className="status__icon">{status.icon}</span>
            <span className="status__text">{status.text}</span>
          </span>
        </div>
      </div>
      
      <div className="chatbot-header__actions">
        {onMinimize && (
          <button
            onClick={onMinimize}
            className="chatbot-header__action"
            title="Thu nhỏ"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </button>
        )}
        
        {onClose && (
          <button
            onClick={onClose}
            className="chatbot-header__action"
            title="Đóng"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

export default ChatbotHeader;
