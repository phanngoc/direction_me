import React from 'react';
import { ChatbotMessage } from '../../shared/types';

interface MessageDisplayProps {
  message: ChatbotMessage;
}

const MessageDisplay: React.FC<MessageDisplayProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  const isBot = message.sender === 'bot';
  const isSystem = message.sender === 'system';

  const formatMessage = (content: string) => {
    // Simple formatting for line breaks
    return content.split('\n').map((line, index) => (
      <span key={index}>
        {line}
        {index < content.split('\n').length - 1 && <br />}
      </span>
    ));
  };

  const getMessageClassName = () => {
    let className = 'message';
    
    if (isUser) className += ' message--user';
    if (isBot) className += ' message--bot';
    if (isSystem) className += ' message--system';
    
    if (message.message_type === 'assessment_redirect') {
      className += ' message--redirect';
    }
    
    if (message.message_type === 'results') {
      className += ' message--results';
    }
    
    return className;
  };

  const getSenderName = () => {
    if (isUser) return 'Bạn';
    if (isBot) return 'MyWay Assistant';
    if (isSystem) return 'Hệ thống';
    return 'Unknown';
  };

  const getMessageIcon = () => {
    if (isUser) return '👤';
    if (isBot) return '🤖';
    if (isSystem) return '⚙️';
    return '❓';
  };

  return (
    <div className={getMessageClassName()}>
      <div className="message__header">
        <span className="message__icon">{getMessageIcon()}</span>
        <span className="message__sender">{getSenderName()}</span>
        <span className="message__time">
          {new Date(message.created_at).toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </span>
      </div>
      
      <div className="message__content">
        {formatMessage(message.content)}
      </div>
      
      {message.intent && (
        <div className="message__metadata">
          <small>Intent: {message.intent}</small>
          {message.confidence && (
            <small>Confidence: {(message.confidence * 100).toFixed(1)}%</small>
          )}
        </div>
      )}
      
      {message.message_type === 'assessment_redirect' && (
        <div className="message__action">
          <button className="btn btn--primary">
            Bắt đầu đánh giá
          </button>
        </div>
      )}
      
      {message.message_type === 'results' && (
        <div className="message__action">
          <button className="btn btn--success">
            Xem kết quả chi tiết
          </button>
        </div>
      )}
    </div>
  );
};

export default MessageDisplay;
