import React from 'react';
import { Bot, User, Sparkles } from 'lucide-react';

const MessageBubble = ({ message }) => {
  const isAI = message.type === 'ai';
  const isTyping = message.isTyping;

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  if (isTyping) {
    return (
      <div className="flex items-start space-x-3 mb-4">
        <div className="flex-shrink-0">
          <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
            <Bot className="w-4 h-4 text-white" />
          </div>
        </div>
        <div className="flex-1">
          <div className="bg-gray-700 rounded-2xl rounded-tl-sm px-4 py-3 max-w-3xl">
            <div className="flex items-center space-x-1">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
              <span className="text-xs text-gray-400 ml-2">AI is thinking...</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-start space-x-3 mb-4 ${!isAI ? 'flex-row-reverse space-x-reverse message-user' : 'message-ai'}`}>
      {/* Avatar */}
      <div className="flex-shrink-0">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
          isAI ? 'bg-blue-600' : 'bg-gray-600'
        }`}>
          {isAI ? (
            <Bot className="w-4 h-4 text-white" />
          ) : (
            <User className="w-4 h-4 text-white" />
          )}
        </div>
      </div>

      {/* Message Content */}
      <div className="flex-1">
        <div className={`rounded-2xl px-4 py-3 max-w-3xl ${
          isAI 
            ? 'bg-gray-700 rounded-tl-sm text-gray-100' 
            : 'bg-blue-600 rounded-tr-sm text-white ml-auto'
        }`}>
          {/* AI Badge for AI messages */}
          {isAI && (
            <div className="flex items-center space-x-1 mb-2">
              <Sparkles className="w-3 h-3 text-blue-400" />
              <span className="text-xs text-blue-400 font-medium">MarketMiner AI</span>
            </div>
          )}
          
          {/* Message Text */}
          <div className="text-sm leading-relaxed whitespace-pre-wrap">
            {message.content}
          </div>
          
          {/* Timestamp */}
          {message.timestamp && (
            <div className={`text-xs mt-2 ${
              isAI ? 'text-gray-400' : 'text-blue-100'
            }`}>
              {formatTime(message.timestamp)}
            </div>
          )}
        </div>

        {/* Search Query Indicator */}
        {message.searchQuery && (
          <div className="mt-2 text-xs text-gray-400 flex items-center space-x-1">
            <Sparkles className="w-3 h-3" />
            <span>Searching for: "{message.searchQuery}"</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;