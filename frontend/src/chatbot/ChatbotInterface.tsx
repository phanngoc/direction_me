import React, { useState, useEffect, useRef } from 'react';
import { ChatbotMessage } from '../../shared/types';
import MessageDisplay from './MessageDisplay';
import MessageInput from './MessageInput';
import ChatbotHeader from './ChatbotHeader';
import { useChatbotWebSocket } from '../services/chatbot_ws';

interface ChatbotInterfaceProps {
  sessionId: string;
  userId: string;
  onAssessmentRedirect?: () => void;
  onResultsReady?: () => void;
}

const ChatbotInterface: React.FC<ChatbotInterfaceProps> = ({
  sessionId,
  userId,
  onAssessmentRedirect,
  onResultsReady
}) => {
  const [messages, setMessages] = useState<ChatbotMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { 
    isConnected, 
    sendMessage, 
    lastMessage 
  } = useChatbotWebSocket(sessionId);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle incoming messages
  useEffect(() => {
    if (lastMessage) {
      const newMessage: ChatbotMessage = {
        id: lastMessage.id || Date.now().toString(),
        session_id: sessionId,
        sender: lastMessage.sender || 'bot',
        message_type: lastMessage.message_type || 'text',
        content: lastMessage.content || lastMessage.message || '',
        intent: lastMessage.intent,
        entities: lastMessage.entities,
        confidence: lastMessage.confidence,
        created_at: new Date().toISOString()
      };

      setMessages(prev => [...prev, newMessage]);
      setIsTyping(false);

      // Handle special message types
      if (lastMessage.message_type === 'assessment_redirect' && onAssessmentRedirect) {
        onAssessmentRedirect();
      } else if (lastMessage.message_type === 'results' && onResultsReady) {
        onResultsReady();
      }
    }
  }, [lastMessage, sessionId, onAssessmentRedirect, onResultsReady]);

  const handleSendMessage = async (content: string, messageType: string = 'text') => {
    if (!content.trim()) return;

    // Add user message to UI immediately
    const userMessage: ChatbotMessage = {
      id: Date.now().toString(),
      session_id: sessionId,
      sender: 'user',
      message_type: messageType,
      content: content,
      created_at: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      await sendMessage(content, messageType);
    } catch (error) {
      console.error('Failed to send message:', error);
      setIsTyping(false);
      
      // Add error message
      const errorMessage: ChatbotMessage = {
        id: (Date.now() + 1).toString(),
        session_id: sessionId,
        sender: 'bot',
        message_type: 'text',
        content: 'Xin lỗi, có lỗi xảy ra. Vui lòng thử lại.',
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  return (
    <div className="chatbot-interface">
      <ChatbotHeader 
        isConnected={isConnected}
        sessionId={sessionId}
      />
      
      <div className="chatbot-messages">
        {messages.map((message) => (
          <MessageDisplay
            key={message.id}
            message={message}
          />
        ))}
        
        {isTyping && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={!isConnected}
      />
    </div>
  );
};

export default ChatbotInterface;
