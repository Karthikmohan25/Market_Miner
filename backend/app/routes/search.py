from flask import Blueprint, request, jsonify
from app.services.scraper import MarketplaceScraper
from app.models.product import Product
import json

search_bp = Blueprint('search', __name__)

@search_bp.route('/products', methods=['POST'])
def search_products():
    """Search for products across marketplaces"""
    try:
        data = request.get_json()
        print(f"Received search request: {data}")
        
        query = data.get('query', '').strip()
        platforms = data.get('platforms', ['Amazon', 'eBay'])
        max_results = data.get('max_results', 20)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        print(f"Searching for '{query}' on platforms: {platforms}")
        
        scraper = MarketplaceScraper()
        product_model = Product()
        all_products = []
        
        # Check cache first
        for platform in platforms:
            print(f"Checking cache for {platform}...")
            cached_results = product_model.get_cached_results(query, platform)
            if cached_results:
                print(f"Found cached results for {platform}")
                cached_products = json.loads(cached_results)
                all_products.extend(cached_products)
                continue
            
            print(f"No cache found, scraping {platform}...")
            
            # Scrape fresh data
            if platform.lower() == 'amazon':
                products = scraper.search_amazon(query, max_results)
            elif platform.lower() == 'ebay':
                products = scraper.search_ebay(query, max_results)
            else:
                print(f"Unknown platform: {platform}")
                continue
            
            print(f"Found {len(products)} products on {platform}")
            
            # Save to database and cache
            for product in products:
                try:
                    product_model.save_product(product)
                except Exception as e:
                    print(f"Error saving product: {e}")
            
            try:
                product_model.cache_results(query, platform, json.dumps(products))
            except Exception as e:
                print(f"Error caching results: {e}")
                
            all_products.extend(products)
        
        print(f"Total products found: {len(all_products)}")
        
        return jsonify({
            'query': query,
            'total_results': len(all_products),
            'products': all_products,
            'platforms_searched': platforms
        })
        
    except Exception as e:
        print(f"Error in search_products: {e}")
        return jsonify({'error': str(e)}), 500

@search_bp.route('/shopify', methods=['POST'])
def search_shopify():
    """Search for Shopify stores selling the product"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        scraper = MarketplaceScraper()
        stores = scraper.search_shopify_stores(query, max_results)
        
        return jsonify({
            'query': query,
            'total_stores': len(stores),
            'stores': stores
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500