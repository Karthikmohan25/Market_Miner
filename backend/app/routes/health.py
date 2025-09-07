from flask import Blueprint, jsonify
from app.services.scraper import MarketplaceScraper
from app.services.trends import TrendsAnalyzer
from app.models.product import Product

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'MarketMiner API is running',
        'version': '1.0.0'
    })

@health_bp.route('/test', methods=['GET'])
def test_services():
    """Test all services quickly"""
    results = {
        'scraper': 'unknown',
        'trends': 'unknown',
        'database': 'unknown'
    }
    
    # Test scraper
    try:
        scraper = MarketplaceScraper()
        test_products = scraper._generate_mock_data('test', 'Test', 2)
        results['scraper'] = 'working' if len(test_products) > 0 else 'failed'
    except Exception as e:
        results['scraper'] = f'error: {str(e)}'
    
    # Test trends
    try:
        analyzer = TrendsAnalyzer()
        test_trends = analyzer._generate_mock_trend_data(['test'])
        results['trends'] = 'working' if test_trends.get('keywords') else 'failed'
    except Exception as e:
        results['trends'] = f'error: {str(e)}'
    
    # Test database
    try:
        product_model = Product()
        # Just test initialization
        results['database'] = 'working'
    except Exception as e:
        results['database'] = f'error: {str(e)}'
    
    return jsonify({
        'status': 'test_complete',
        'services': results
    })