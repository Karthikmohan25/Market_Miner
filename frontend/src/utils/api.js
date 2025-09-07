import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 429) {
      console.error('Rate limit exceeded. Please try again later.');
    }
    return Promise.reject(error);
  }
);

// API methods
export const searchProducts = (query, platforms = ['Amazon', 'eBay'], maxResults = 20) => {
  return api.post('/api/search/products', {
    query,
    platforms,
    max_results: maxResults
  });
};

export const searchShopifyStores = (query, maxResults = 10) => {
  return api.post('/api/search/shopify', {
    query,
    max_results: maxResults
  });
};

export const analyzeTrends = (keywords, timeframe = 'today 12-m') => {
  return api.post('/api/trends/analyze', {
    keywords,
    timeframe
  });
};

export const compareKeywords = (keywords, timeframe = 'today 12-m') => {
  return api.post('/api/trends/compare', {
    keywords,
    timeframe
  });
};

export const analyzeOpportunity = (query, platforms = ['Amazon', 'eBay'], includeTrends = true) => {
  return api.post('/api/analysis/opportunity', {
    query,
    platforms,
    include_trends: includeTrends
  });
};

export const calculateScore = (products, trendData = null) => {
  return api.post('/api/analysis/score', {
    products,
    trend_data: trendData
  });
};

export const processChatMessage = (message) => {
  return api.post('/api/chat/process', {
    message
  });
};

export default api;