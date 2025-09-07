import React from 'react';
import { Star, ExternalLink, TrendingUp, Award } from 'lucide-react';

const ProductSuggestions = ({ products, title = "Recommended Products" }) => {
  if (!products || products.length === 0) return null;

  const formatPrice = (price) => {
    return typeof price === 'number' ? `$${price.toFixed(2)}` : price;
  };

  const getPlatformColor = (platform) => {
    switch (platform?.toLowerCase()) {
      case 'amazon':
        return 'bg-orange-600';
      case 'ebay':
        return 'bg-blue-600';
      case 'shopify':
        return 'bg-green-600';
      default:
        return 'bg-gray-600';
    }
  };

  return (
    <div className="mt-4 mb-6">
      {/* Header */}
      <div className="flex items-center space-x-2 mb-4">
        <Award className="w-5 h-5 text-yellow-400" />
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <div className="flex items-center space-x-1 px-2 py-1 bg-yellow-600 rounded-full">
          <TrendingUp className="w-3 h-3 text-white" />
          <span className="text-xs text-white font-medium">HOT</span>
        </div>
      </div>

      {/* Products Carousel */}
      <div className="flex space-x-4 overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
        {products.map((product, index) => (
          <div
            key={product.id || index}
            className="flex-shrink-0 w-72 bg-gray-800 rounded-xl p-4 border border-gray-700 hover:border-gray-600 transition-all duration-200 hover:shadow-lg group product-card"
          >
            {/* Product Image */}
            <div className="relative mb-3">
              <div className="w-full h-40 bg-gray-700 rounded-lg flex items-center justify-center overflow-hidden">
                {product.image ? (
                  <img 
                    src={product.image} 
                    alt={product.title}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="text-gray-400 text-center">
                    <div className="w-16 h-16 bg-gray-600 rounded-lg mx-auto mb-2 flex items-center justify-center">
                      <TrendingUp className="w-8 h-8" />
                    </div>
                    <span className="text-sm">Product Image</span>
                  </div>
                )}
              </div>
              
              {/* Platform Badge */}
              <div className={`absolute top-2 left-2 px-2 py-1 rounded-full text-xs text-white font-medium ${getPlatformColor(product.platform)}`}>
                {product.platform}
              </div>
              
              {/* Recommended Badge */}
              {product.isRecommended && (
                <div className="absolute top-2 right-2 px-2 py-1 bg-yellow-600 rounded-full text-xs text-white font-medium flex items-center space-x-1">
                  <Award className="w-3 h-3" />
                  <span>TOP</span>
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="space-y-2">
              {/* Title */}
              <h4 className="text-white font-medium text-sm line-clamp-2 group-hover:text-blue-400 transition-colors">
                {product.title}
              </h4>

              {/* Price and Rating */}
              <div className="flex items-center justify-between">
                <div className="text-green-400 font-bold text-lg">
                  {formatPrice(product.price)}
                </div>
                
                {product.rating && (
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="text-white text-sm">{product.rating}</span>
                    {product.reviews && (
                      <span className="text-gray-400 text-xs">({product.reviews})</span>
                    )}
                  </div>
                )}
              </div>

              {/* Features/Tags */}
              {product.features && (
                <div className="flex flex-wrap gap-1">
                  {product.features.slice(0, 2).map((feature, idx) => (
                    <span key={idx} className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded-full">
                      {feature}
                    </span>
                  ))}
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex space-x-2 pt-2">
                <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm py-2 px-3 rounded-lg transition-colors flex items-center justify-center space-x-1">
                  <span>View Details</span>
                </button>
                
                {product.url && (
                  <button className="p-2 bg-gray-700 hover:bg-gray-600 text-gray-300 rounded-lg transition-colors">
                    <ExternalLink className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* Quick Stats */}
              <div className="flex justify-between text-xs text-gray-400 pt-1">
                <span>Market Score: {Math.floor(Math.random() * 30) + 70}/100</span>
                <span>Trending: +{Math.floor(Math.random() * 50) + 10}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* View All Button */}
      <div className="text-center mt-4">
        <button className="px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors text-sm">
          View All Results →
        </button>
      </div>
    </div>
  );
};

export default ProductSuggestions;