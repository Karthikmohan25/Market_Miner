import React, { useState } from 'react';
import { Search, Filter, Sparkles } from 'lucide-react';

const SearchForm = ({ onSearch, isLoading, initialQuery = '', initialFilters = {} }) => {
  const [query, setQuery] = useState(initialQuery);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    platforms: ['Amazon', 'eBay'],
    priceRange: { min: '', max: '' },
    minRating: '',
    minReviews: '',
    ...initialFilters
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), filters);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handlePlatformToggle = (platform) => {
    setFilters(prev => ({
      ...prev,
      platforms: prev.platforms.includes(platform)
        ? prev.platforms.filter(p => p !== platform)
        : [...prev.platforms, platform]
    }));
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Main Search Input */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter product keywords or describe what you're looking for..."
            className="block w-full pl-10 pr-12 py-4 border border-gray-600 rounded-xl bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
          />
          <button
            type="button"
            onClick={() => setShowFilters(!showFilters)}
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <Filter className={`h-5 w-5 transition-colors ${showFilters ? 'text-blue-400' : 'text-gray-400 hover:text-gray-300'}`} />
          </button>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className="bg-gray-700 rounded-xl p-6 space-y-6">
            <h3 className="text-lg font-semibold text-white flex items-center">
              <Filter className="w-5 h-5 mr-2" />
              Filters
            </h3>

            {/* Platforms */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-3">
                Platforms
              </label>
              <div className="flex flex-wrap gap-3">
                {['Amazon', 'eBay', 'Shopify'].map((platform) => (
                  <button
                    key={platform}
                    type="button"
                    onClick={() => handlePlatformToggle(platform)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      filters.platforms.includes(platform)
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-600 text-gray-300 hover:bg-gray-500'
                    }`}
                  >
                    {platform}
                  </button>
                ))}
              </div>
            </div>

            {/* Price Range */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-3">
                Price Range
              </label>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <input
                    type="number"
                    placeholder="Min price"
                    value={filters.priceRange.min}
                    onChange={(e) => handleFilterChange('priceRange', { ...filters.priceRange, min: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-600 rounded-lg bg-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <input
                    type="number"
                    placeholder="Max price"
                    value={filters.priceRange.max}
                    onChange={(e) => handleFilterChange('priceRange', { ...filters.priceRange, max: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-600 rounded-lg bg-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Rating and Reviews */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Min Rating
                </label>
                <select
                  value={filters.minRating}
                  onChange={(e) => handleFilterChange('minRating', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-600 rounded-lg bg-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Any Rating</option>
                  <option value="4">4+ Stars</option>
                  <option value="3">3+ Stars</option>
                  <option value="2">2+ Stars</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Min Reviews
                </label>
                <input
                  type="number"
                  placeholder="Min reviews"
                  value={filters.minReviews}
                  onChange={(e) => handleFilterChange('minReviews', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-600 rounded-lg bg-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>
        )}

        {/* Search Button */}
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-xl transition-colors flex items-center justify-center space-x-2"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Analyzing Market...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              <span>Analyze Market</span>
            </>
          )}
        </button>
      </form>

      {/* Example Searches */}
      <div className="mt-6">
        <p className="text-sm text-gray-400 mb-3">Try these examples:</p>
        <div className="flex flex-wrap gap-2">
          {[
            'trending gym gear under $50',
            'wireless earbuds',
            'home office accessories',
            'pet toys for dogs'
          ].map((example) => (
            <button
              key={example}
              type="button"
              onClick={() => setQuery(example)}
              className="px-3 py-1 text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 rounded-full transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SearchForm;