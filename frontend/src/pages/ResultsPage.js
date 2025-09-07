import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Search, TrendingUp, Star, ExternalLink, Loader } from 'lucide-react';
import { searchProducts } from '../utils/api';

const ResultsPage = () => {
  const [searchParams] = useSearchParams();
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const query = searchParams.get('q');
  const platforms = searchParams.get('platforms')?.split(',') || ['Amazon', 'eBay'];

  useEffect(() => {
    if (query) {
      searchProductsData();
    }
  }, [query]);

  const searchProductsData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await searchProducts(query, platforms, 20);
      setResults(response.data);
    } catch (err) {
      setError('Failed to fetch results. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <Loader className="w-8 h-8 animate-spin text-blue-500 mx-auto mb-4" />
          <p className="text-gray-400">Analyzing market data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-400 mb-4">{error}</div>
        <button
          onClick={searchProductsData}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (!results || !results.products?.length) {
    return (
      <div className="text-center py-12">
        <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-white mb-2">No Results Found</h2>
        <p className="text-gray-400">Try adjusting your search terms or filters.</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">
          Search Results for "{query}"
        </h1>
        <p className="text-gray-400">
          Found {results.total_results} products across {results.platforms_searched.join(', ')}
        </p>
      </div>

      {/* Results Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.products.map((product, index) => (
          <div key={index} className="bg-gray-800 rounded-xl p-6 hover:bg-gray-750 transition-colors">
            <div className="flex items-start justify-between mb-4">
              <span className="px-2 py-1 bg-blue-600 text-white text-xs rounded-full">
                {product.platform}
              </span>
              {product.url && (
                <a
                  href={product.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-white"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
              )}
            </div>

            <h3 className="text-white font-semibold mb-2 line-clamp-2">
              {product.title}
            </h3>

            <div className="space-y-2">
              {product.price > 0 && (
                <div className="text-green-400 font-bold text-lg">
                  ${product.price.toFixed(2)}
                </div>
              )}

              {product.rating > 0 && (
                <div className="flex items-center space-x-2">
                  <div className="flex items-center">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="text-white ml-1">{product.rating}</span>
                  </div>
                  {product.reviews_count > 0 && (
                    <span className="text-gray-400 text-sm">
                      ({product.reviews_count} reviews)
                    </span>
                  )}
                </div>
              )}

              {product.seller && (
                <div className="text-gray-400 text-sm">
                  Seller: {product.seller}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Load More Button */}
      {results.products.length >= 20 && (
        <div className="text-center mt-8">
          <button className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg">
            Load More Results
          </button>
        </div>
      )}
    </div>
  );
};

export default ResultsPage;
