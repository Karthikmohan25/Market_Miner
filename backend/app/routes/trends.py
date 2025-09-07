from flask import Blueprint, request, jsonify
from app.services.trends import TrendsAnalyzer

# keep same blueprint name to avoid changing route registration elsewhere
trends_bp = Blueprint('trends', __name__)

@trends_bp.route('/analyze', methods=['POST'])
def analyze_trends():
    """Analyze Google Trends for keywords"""
    try:
        data = request.get_json(silent=True) or {}
        keywords = data.get('keywords', [])
        timeframe = data.get('timeframe', 'today 12-m')
        
        # normalize keywords to a list of non-empty strings
        if isinstance(keywords, str):
            keywords = [keywords]
        if not isinstance(keywords, list):
            return jsonify({'error': 'Keywords must be a list or string'}), 400

        keywords = [k.strip() for k in keywords if isinstance(k, str) and k.strip()]
        if not keywords:
            return jsonify({'error': 'Keywords are required'}), 400
        
        # Limit to 5 keywords
        keywords = keywords[:5]
        
        analyzer = TrendsAnalyzer()
        trend_data = analyzer.get_trend_data(keywords, timeframe)
        
        return jsonify(trend_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@trends_bp.route('/compare', methods=['POST'])
def compare_keywords():
    """Compare multiple keywords trends"""
    try:
        data = request.get_json(silent=True) or {}
        keywords = data.get('keywords', [])
        timeframe = data.get('timeframe', 'today 12-m')
        
        # normalize keywords
        if isinstance(keywords, str):
            keywords = [keywords]
        if not isinstance(keywords, list):
            return jsonify({'error': 'Keywords must be a list or string'}), 400

        keywords = [k.strip() for k in keywords if isinstance(k, str) and k.strip()]

        if len(keywords) < 2:
            return jsonify({'error': 'At least 2 keywords required for comparison'}), 400
        
        # optional: limit keywords to a manageable number
        keywords = keywords[:10]
        
        analyzer = TrendsAnalyzer()
        trend_data = analyzer.get_trend_data(keywords, timeframe)
        
        # Add comparison insights
        comparison = {
            'winner': None,
            'insights': []
        }
        
        if isinstance(trend_data, dict) and 'trend_analysis' in trend_data:
            # Find keyword with highest average interest (safe access)
            try:
                best_keyword = max(
                    trend_data['trend_analysis'].items(),
                    key=lambda x: x[1].get('average_interest', 0)
                )
                comparison['winner'] = best_keyword[0]
            except Exception:
                comparison['winner'] = None
            
            # Generate insights
            for keyword, analysis in trend_data['trend_analysis'].items():
                direction = analysis.get('trend_direction', 'stable')
                avg_interest = analysis.get('average_interest', 0)
                comparison['insights'].append(
                    f"{keyword}: {direction} trend with {avg_interest:.1f} average interest"
                )
        
        trend_data['comparison'] = comparison
        
        return jsonify(trend_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
