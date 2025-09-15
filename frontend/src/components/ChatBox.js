import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader, Sparkles } from 'lucide-react';
import MessageBubble from './MessageBubble';
import ProductSuggestions from './ProductSuggestions';
import { processChatMessage } from '../utils/api';

const ChatBox = ({ onSearch, isLoading }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: "Hi! I'm your MarketMiner AI assistant. I can help you discover trending products, analyze market opportunities, and find the best deals. What are you looking for today?",
      timestamp: new Date()
    }
  ]);
  const [conversationContext, setConversationContext] = useState({
    lastQuery: '',
    lastProducts: [],
    conversationHistory: []
  });
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      console.log('🚀 Sending message:', inputValue.trim());
      console.log('📝 Context:', conversationContext);
      
      // Add conversation context to the request
      const requestData = {
        message: inputValue.trim(),
        context: conversationContext
      };
      
      // Process the natural language query via API
      const response = await processChatMessage(requestData);
      const data = response.data;
      
      console.log('✅ Received response:', data);
      
      // Add AI response
      setTimeout(() => {
        const aiMessage = {
          id: Date.now() + 1,
          type: 'ai',
          content: data.ai_response,
          timestamp: new Date(),
          products: data.products,
          searchQuery: data.search_query
        };
        
        setMessages(prev => [...prev, aiMessage]);
        setIsTyping(false);

        // Update conversation context with the actual products and query
        setConversationContext(prev => ({
          lastQuery: data.search_query || prev.lastQuery,
          lastProducts: data.products || prev.lastProducts,
          conversationHistory: [...prev.conversationHistory, {
            user: inputValue.trim(),
            ai: data.ai_response,
            timestamp: new Date()
          }].slice(-5) // Keep last 5 exchanges
        }));

        // Trigger search if needed (for external search functionality)
        if (data.should_search && data.search_query && onSearch) {
          onSearch(data.search_query, {
            platforms: ['Amazon', 'eBay'],
            priceRange: {}
          });
        }
      }, 800 + Math.random() * 800); // Simulate AI thinking time

    } catch (error) {
      setIsTyping(false);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: "I'm sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };



  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const suggestedQueries = [
    "Find me trending gym gear under $50",
    "What are the best wireless earbuds?",
    "Show me popular kitchen gadgets",
    "Compare laptop prices across platforms"
  ];

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <div key={message.id}>
            <MessageBubble message={message} />
            {message.products && message.products.length > 0 && (
              <ProductSuggestions 
                products={message.products} 
                title="Highly Recommended"
              />
            )}
          </div>
        ))}
        
        {isTyping && (
          <MessageBubble 
            message={{
              type: 'ai',
              content: '',
              isTyping: true
            }} 
          />
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Queries (show when no messages or few messages) */}
      {messages.length <= 2 && (
        <div className="px-6 pb-4">
          <p className="text-sm text-gray-400 mb-3">Try asking:</p>
          <div className="flex flex-wrap gap-2">
            {suggestedQueries.map((query, index) => (
              <button
                key={index}
                onClick={() => setInputValue(query)}
                className="px-3 py-2 text-sm bg-gray-700 hover:bg-gray-600 text-gray-300 rounded-full transition-colors"
              >
                {query}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-gray-700 p-6">
        <form onSubmit={handleSubmit} className="relative">
          <div className="flex items-end space-x-4">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything about products, trends, or market analysis..."
                className="w-full px-4 py-3 pr-12 border border-gray-600 rounded-xl bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[50px] max-h-32"
                rows={1}
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="absolute right-3 bottom-3 p-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
              >
                {isLoading ? (
                  <Loader className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
          
          <div className="flex items-center justify-between mt-2 text-xs text-gray-400">
            <span>Press Enter to send, Shift+Enter for new line</span>
            <div className="flex items-center space-x-1">
              <Sparkles className="w-3 h-3" />
              <span>Powered by AI</span>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatBox;