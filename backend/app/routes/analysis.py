from flask import Blueprint, request, jsonify
from app.services.ai_analyzer import AIAnalyzer
from app.services.scraper import MarketplaceScraper
from app.services.trends import TrendsAnalyzer

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/opportunity', methods=['POST'])
def analyze_opportunity():
    """Comprehensive opportunity analysis"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        platforms = data.get('platforms', ['Amazon', 'eBay'])
        include_trends = data.get('include_trends', True)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Get product data
        scraper = MarketplaceScraper()
        all_products = []
        
        for platform in platforms:
            if platform.lower() == 'amazon':
                products = scraper.search_amazon(query, 20)
            elif platform.lower() == 'ebay':
                products = scraper.search_ebay(query, 20)
            else:
                continue
            all_products.extend(products)
        
        # Get trend data if requested
        trend_data = None
        if include_trends:
            analyzer = TrendsAnalyzer()
            keywords = [query] + query.split()[:4]  # Use query + individual words
            trend_data = analyzer.get_trend_data(keywords)
        
        # AI Analysis
        ai_analyzer = AIAnalyzer()
        analysis = ai_analyzer.analyze_products(all_products, trend_data)
        
        # Compile comprehensive report
        report = {
            'query': query,
            'timestamp': data.get('timestamp'),
            'product_data': {
                'total_products': len(all_products),
                'platforms': platforms,
                'products': all_products[:10]  # Return top 10 for display
            },
            'trend_data': trend_data,
            'ai_analysis': analysis,
            'opportunity_score': analysis.get('opportunity_score', 0),
            'recommendations': _generate_recommendations(all_products, trend_data, analysis)
        }
        
        return jsonify(report)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/score', methods=['POST'])
def calculate_score():
    """Calculate opportunity score for given data"""
    try:
        data = request.get_json()
        products = data.get('products', [])
        trend_data = data.get('trend_data')
        
        ai_analyzer = AIAnalyzer()
        score = ai_analyzer._calculate_opportunity_score(products, trend_data)
        
        return jsonify({
            'opportunity_score': score,
            'score_breakdown': _get_score_breakdown(products, trend_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _generate_recommendations(products, trend_data, analysis):
    """Generate actionable recommendations"""
    recommendations = []
    
    if not products:
        recommendations.append("No products found - consider different keywords or platforms")
        return recommendations
    
    # Price recommendations
    prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
    if prices:
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        if max_price - min_price > avg_price * 0.5:
            recommendations.append(f"High price variation (${min_price:.2f}-${max_price:.2f}) suggests pricing opportunities")
        
        if avg_price < 25:
            recommendations.append("Low average price point - consider volume-based strategy")
        elif avg_price > 100:
            recommendations.append("High price point - focus on quality and differentiation")
    
    # Competition recommendations
    if len(products) > 50:
        recommendations.append("High competition detected - focus on niche differentiation")
    elif len(products) < 10:
        recommendations.append("Low competition - potential blue ocean opportunity")
    
    # Trend recommendations
    if trend_data and 'trend_analysis' in trend_data:
        rising_trends = [k for k, v in trend_data['trend_analysis'].items() 
                        if v.get('trend_direction') == 'rising']
        if rising_trends:
            recommendations.append(f"Rising trends detected: {', '.join(rising_trends)}")
    
    # Platform recommendations
    platforms = {}
    for product in products:
        platform = product.get('platform', 'Unknown')
        platforms[platform] = platforms.get(platform, 0) + 1
    
    if len(platforms) == 1:
        recommendations.append("Consider expanding to additional platforms")
    
    return recommendations

def _get_score_breakdown(products, trend_data):
    """Get detailed score breakdown"""
    breakdown = {
        'trend_interest': 0,
        'rating_reviews': 0,
        'competition': 0,
        'price_spread': 0
    }
    
    # This would contain the detailed calculation logic
    # For brevity, returning basic structure
    
    return breakdown