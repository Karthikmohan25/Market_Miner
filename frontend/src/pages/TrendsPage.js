import React, { useState } from 'react';
import { TrendingUp, Search, BarChart3, Loader } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { analyzeTrends } from '../utils/api';

const TrendsPage = () => {
  const [keywords, setKeywords] = useState(['']);
  const [trendData, setTrendData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const addKeyword = () => {
    if (keywords.length < 5) {
      setKeywords([...keywords, '']);
    }
  };

  const updateKeyword = (index, value) => {
    const newKeywords = [...keywords];
    newKeywords[index] = value;
    setKeywords(newKeywords);
  };

  const removeKeyword = (index) => {
    if (keywords.length > 1) {
      const newKeywords = keywords.filter((_, i) => i !== index);
      setKeywords(newKeywords);
    }
  };

  const analyzeTrendsData = async () => {
    const validKeywords = keywords.filter(k => k.trim());
    if (validKeywords.length === 0) return;

    setLoading(true);
    setError(null);

    try {
      const response = await analyzeTrends(validKeywords, 'today 12-m');
      setTrendData(response.data);
    } catch (err) {
      setError('Failed to fetch trend data. Please try again.');
      console.error('Trends error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center">
            <TrendingUp className="w-8 h-8 text-white" />
          </div>
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">
          Google Trends Analysis
        </h1>
        <p className="text-xl text-gray-400">
          Compare keyword trends and discover market opportunities
        </p>
      </div>

      {/* Search Form */}
      <div className="bg-gray-800 rounded-2xl p-8 mb-8">
        <h2 className="text-xl font-semibold text-white mb-6">Compare Keywords</h2>
        
        <div className="space-y-4 mb-6">
          {keywords.map((keyword, index) => (
            <div key={index} className="flex items-center space-x-4">
              <div className="flex-1">
                <input
                  type="text"
                  value={keyword}
                  onChange={(e) => updateKeyword(index, e.target.value)}
                  placeholder={`Keyword ${index + 1}`}
                  className="w-full px-4 py-3 border border-gray-600 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
              {keywords.length > 1 && (
                <button
                  onClick={() => removeKeyword(index)}
                  className="text-red-400 hover:text-red-300 px-3 py-3"
                >
                  ×
                </button>
              )}
            </div>
          ))}
        </div>

        <div className="flex items-center justify-between">
          <div className="flex space-x-4">
            {keywords.length < 5 && (
              <button
                onClick={addKeyword}
                className="text-green-400 hover:text-green-300 text-sm"
              >
                + Add Keyword
              </button>
            )}
            <span className="text-gray-400 text-sm">
              {keywords.length}/5 keywords
            </span>
          </div>

          <button
            onClick={analyzeTrendsData}
            disabled={loading || keywords.filter(k => k.trim()).length === 0}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center space-x-2"
          >
            {loading ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <BarChart3 className="w-5 h-5" />
                <span>Analyze Trends</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-900 border border-red-700 rounded-lg p-4 mb-8">
          <p className="text-red-200">{error}</p>
        </div>
      )}

      {/* Results */}
      {trendData && (
        <div className="space-y-8">
          {/* Trend Chart */}
          {trendData.interest_over_time && trendData.interest_over_time.length > 0 && (
            <div className="bg-gray-800 rounded-2xl p-8">
              <h3 className="text-xl font-semibold text-white mb-6">Interest Over Time</h3>
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trendData.interest_over_time}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis 
                      dataKey="date" 
                      stroke="#9CA3AF"
                      fontSize={12}
                    />
                    <YAxis stroke="#9CA3AF" fontSize={12} />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1F2937', 
                        border: '1px solid #374151',
                        borderRadius: '8px'
                      }}
                    />
                    {trendData.keywords.map((keyword, index) => (
                      <Line
                        key={keyword}
                        type="monotone"
                        dataKey={keyword}
                        stroke={`hsl(${index * 60}, 70%, 50%)`}
                        strokeWidth={2}
                        dot={false}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Trend Analysis */}
          {trendData.trend_analysis && (
            <div className="bg-gray-800 rounded-2xl p-8">
              <h3 className="text-xl font-semibold text-white mb-6">Trend Analysis</h3>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Object.entries(trendData.trend_analysis).map(([keyword, analysis]) => (
                  <div key={keyword} className="bg-gray-700 rounded-lg p-6">
                    <h4 className="font-semibold text-white mb-4">{keyword}</h4>
                    <div className="space-y-3">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Trend:</span>
                        <span className={`font-medium ${
                          analysis.trend_direction === 'rising' ? 'text-green-400' :
                          analysis.trend_direction === 'falling' ? 'text-red-400' :
                          'text-yellow-400'
                        }`}>
                          {analysis.trend_direction}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Avg Interest:</span>
                        <span className="text-white">{analysis.average_interest?.toFixed(1)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Peak:</span>
                        <span className="text-white">{analysis.max_interest}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Related Queries */}
          {trendData.related_queries && Object.keys(trendData.related_queries).length > 0 && (
            <div className="bg-gray-800 rounded-2xl p-8">
              <h3 className="text-xl font-semibold text-white mb-6">Related Queries</h3>
              <div className="grid md:grid-cols-2 gap-8">
                {Object.entries(trendData.related_queries).map(([keyword, queries]) => (
                  <div key={keyword}>
                    <h4 className="font-semibold text-white mb-4">{keyword}</h4>
                    {queries.top && queries.top.length > 0 && (
                      <div className="mb-4">
                        <h5 className="text-sm font-medium text-gray-300 mb-2">Top Queries</h5>
                        <div className="space-y-2">
                          {queries.top.slice(0, 5).map((query, index) => (
                            <div key={index} className="flex justify-between text-sm">
                              <span className="text-gray-400">{query.query}</span>
                              <span className="text-white">{query.value}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!trendData && !loading && (
        <div className="text-center py-12">
          <TrendingUp className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">Ready to Analyze Trends</h2>
          <p className="text-gray-400">Enter keywords above to see Google Trends data and insights.</p>
        </div>
      )}
    </div>
  );
};

export default TrendsPage;
