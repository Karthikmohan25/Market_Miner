import React, { useState } from 'react';
import { Sparkles, TrendingUp, BarChart3 } from 'lucide-react';
import ChatBox from '../components/ChatBox';

const ChatSearchPage = () => {
  const [searchResults, setSearchResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (query, filters = {}) => {
    setIsLoading(true);
    
    try {
      // Here you would make the API call to search for products
      // For now, we'll simulate the search
      console.log('Searching for:', query, 'with filters:', filters);
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock search results
      const mockResults = {
        query,
        total_results: Math.floor(Math.random() * 100) + 20,
        products: generateMockProducts(query, 10),
        platforms_searched: filters.platforms || ['Amazon', 'eBay']
      };
      
      setSearchResults(mockResults);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const generateMockProducts = (query, count) => {
    const products = [];
    const platforms = ['Amazon', 'eBay', 'Shopify'];
    
    for (let i = 0; i < count; i++) {
      products.push({
        id: `product-${i}`,
        title: `${query} - ${['Premium', 'Professional', 'Best', 'Top Rated', 'Popular'][Math.floor(Math.random() * 5)]} Quality`,
        price: Math.floor(Math.random() * 200) + 10,
        rating: (3.5 + Math.random() * 1.5).toFixed(1),
        reviews_count: Math.floor(Math.random() * 5000) + 100,
        platform: platforms[Math.floor(Math.random() * platforms.length)],
        url: `https://example.com/product/${i}`,
        search_query: query,
        seller: `Seller ${i + 1}`
      });
    }
    
    return products;
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="border-b border-gray-700 bg-gray-800">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">MarketMiner AI</h1>
                <p className="text-xs text-gray-400">Your AI Product Research Assistant</p>
              </div>
            </div>

            {/* Stats */}
            <div className="hidden md:flex items-center space-x-6 text-sm">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-4 h-4 text-green-400" />
                <span className="text-gray-300">Live Market Data</span>
              </div>
              <div className="flex items-center space-x-2">
                <BarChart3 className="w-4 h-4 text-blue-400" />
                <span className="text-gray-300">AI-Powered Analysis</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8 h-[calc(100vh-80px)]">
        {/* Welcome Section - Only show when no conversation started */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center">
              <Sparkles className="w-10 h-10 text-white" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Discover Your Next Winning Product
          </h1>
          <p className="text-xl text-gray-400 mb-8 max-w-3xl mx-auto">
            Chat with our AI assistant to find trending products, analyze market opportunities, 
            and get personalized recommendations based on real-time data.
          </p>
        </div>

        {/* Chat Interface */}
        <div className="bg-gray-800 rounded-2xl shadow-2xl h-[600px] flex flex-col">
          <ChatBox onSearch={handleSearch} isLoading={isLoading} />
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mt-12">
          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Natural Language Search</h3>
            <p className="text-gray-400 text-sm">
              Ask in plain English: "Find trending gym gear under $50" and get instant results
            </p>
          </div>

          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">AI Recommendations</h3>
            <p className="text-gray-400 text-sm">
              Get personalized product suggestions based on market trends and your preferences
            </p>
          </div>

          <div className="bg-gray-800 rounded-xl p-6 text-center">
            <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mx-auto mb-4">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Market Intelligence</h3>
            <p className="text-gray-400 text-sm">
              Real-time analysis of pricing, competition, and opportunity scores
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatSearchPage;