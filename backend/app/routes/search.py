from flask import Blueprint, request, jsonify
from app.services.scraper import MarketplaceScraper
from app.models.product import Product
import json


@search_bp.route('/products', methods=['POST'])
def search_products():
    """Search for products across marketplaces"""
    try:
        data = request.get_json()
        
        query = data.get('query', '').strip()
        platforms = data.get('platforms', ['Amazon', 'eBay'])
        max_results = data.get('max_results', 20)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        
        scraper = MarketplaceScraper()
        product_model = Product()
        all_products = []
        
        # Check cache first
        for platform in platforms:
            cached_results = product_model.get_cached_results(query, platform)
            if cached_results:
                cached_products = json.loads(cached_results)
                all_products.extend(cached_products)
                continue
            
            
            # Scrape fresh data
            if platform.lower() == 'amazon':
                products = scraper.search_amazon(query, max_results)
            elif platform.lower() == 'ebay':
                products = scraper.search_ebay(query, max_results)
            else:
                continue
            
            
            # Save to database and cache
            for product in products:
                try:
                    product_model.save_product(product)
                except Exception as e:
            
            try:
                product_model.cache_results(query, platform, json.dumps(products))
            except Exception as e:
                
            all_products.extend(products)
        
        
        return jsonify({
            'query': query,
            'total_results': len(all_products),
            'products': all_products,
            'platforms_searched': platforms
        })
        
    except Exception as e:
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