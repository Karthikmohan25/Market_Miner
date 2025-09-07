import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter, Sparkles, TrendingUp } from 'lucide-react';
import SearchForm from '../components/SearchForm';

const SearchPage = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    platforms: ['Amazon', 'eBay'],
    priceRange: { min: '', max: '' },
    minRating: '',
    minReviews: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (query, searchFilters) => {
    setIsLoading(true);
    try {
      // Navigate to results page with search parameters
      const searchParams = new URLSearchParams({
        q: query,
        platforms: searchFilters.platforms.join(','),
        ...(searchFilters.priceRange.min && { minPrice: searchFilters.priceRange.min }),
        ...(searchFilters.priceRange.max && { maxPrice: searchFilters.priceRange.max }),
        ...(searchFilters.minRating && { minRating: searchFilters.minRating }),
        ...(searchFilters.minReviews && { minReviews: searchFilters.minReviews })
      });
      
      navigate(`/results?${searchParams.toString()}`);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
        </div>
        <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
          Discover Your Next Winning Product
        </h1>
        <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
          Analyze market trends, competitor data, and customer sentiment to make 
          data-driven product decisions
        </p>
      </div>

      {/* Search Section */}
      <div className="bg-gray-800 rounded-2xl p-8 mb-8">
        <SearchForm
          onSearch={handleSearch}
          isLoading={isLoading}
          initialQuery={searchQuery}
          initialFilters={filters}
        />
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="bg-gray-800 rounded-xl p-6">
          <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mb-4">
            <Search className="w-6 h-6 text-white" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-2">Smart Product Search</h3>
          <p className="text-gray-400">
            Search across Amazon, eBay, and Shopify stores with intelligent filtering
          </p>
        </div>

        <div className="bg-gray-800 rounded-xl p-6">
          <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mb-4">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-2">Trend Analysis</h3>
          <p className="text-gray-400">
            Real-time Google Trends data with visual charts and insights
          </p>
        </div>

        <div className="bg-gray-800 rounded-xl p-6">
          <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mb-4">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-2">AI-Powered Insights</h3>
          <p className="text-gray-400">
            Get opportunity scores and market analysis powered by AI
          </p>
        </div>
      </div>

      {/* Ready to Mine Section */}
      <div className="text-center bg-gray-800 rounded-2xl p-12">
        <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-6">
          <TrendingUp className="w-8 h-8 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-white mb-4">Ready to Mine Some Data?</h2>
        <p className="text-gray-400 mb-6">
          Start by entering a product keyword or describing what you're looking for
        </p>
        <div className="text-sm text-gray-500">
          Built with ❤️ by Lovable
        </div>
      </div>
    </div>
  );
};

export default SearchPage;