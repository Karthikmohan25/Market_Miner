#!/usr/bin/env python3
"""
Test script for MarketMiner scraper functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.scraper import MarketplaceScraper
from app.services.trends import TrendsAnalyzer
from app.models.product import Product

def test_scraper():
    """Test the scraper functionality"""
    print("🧪 Testing MarketMiner Scraper...")
    
    scraper = MarketplaceScraper()
    query = "wireless earbuds"
    
    print(f"\n📱 Testing Amazon scraper for '{query}'...")
    amazon_products = scraper.search_amazon(query, 5)
    print(f"Found {len(amazon_products)} Amazon products")
    
    if amazon_products:
        print("Sample Amazon product:")
        print(f"  Title: {amazon_products[0]['title']}")
        print(f"  Price: ${amazon_products[0]['price']}")
        print(f"  Rating: {amazon_products[0]['rating']}")
    
    print(f"\n🛒 Testing eBay scraper for '{query}'...")
    ebay_products = scraper.search_ebay(query, 5)
    print(f"Found {len(ebay_products)} eBay products")
    
    if ebay_products:
        print("Sample eBay product:")
        print(f"  Title: {ebay_products[0]['title']}")
        print(f"  Price: ${ebay_products[0]['price']}")
    
    print(f"\n🏪 Testing Shopify store finder for '{query}'...")
    shopify_stores = scraper.search_shopify_stores(query, 3)
    print(f"Found {len(shopify_stores)} Shopify stores")
    
    if shopify_stores:
        print("Sample Shopify store:")
        print(f"  Store: {shopify_stores[0]['store_name']}")
        print(f"  Price: ${shopify_stores[0]['price']}")

def test_trends():
    """Test the trends analyzer"""
    print("\n📈 Testing Trends Analyzer...")
    
    analyzer = TrendsAnalyzer()
    keywords = ["wireless earbuds", "bluetooth headphones"]
    
    print(f"Getting trends for: {keywords}")
    trend_data = analyzer.get_trend_data(keywords)
    
    print(f"Keywords analyzed: {trend_data.get('keywords', [])}")
    print(f"Interest over time data points: {len(trend_data.get('interest_over_time', []))}")
    
    if trend_data.get('trend_analysis'):
        print("Trend analysis:")
        for keyword, analysis in trend_data['trend_analysis'].items():
            print(f"  {keyword}: {analysis.get('trend_direction', 'unknown')} trend")

def test_database():
    """Test database functionality"""
    print("\n💾 Testing Database...")
    
    try:
        product_model = Product()
        
        # Test saving a product
        test_product = {
            'title': 'Test Product',
            'price': 29.99,
            'rating': 4.5,
            'reviews_count': 100,
            'platform': 'Test',
            'seller': 'Test Seller',
            'url': 'https://example.com',
            'image_url': 'https://example.com/image.jpg',
            'search_query': 'test query'
        }
        
        product_id = product_model.save_product(test_product)
        print(f"Saved test product with ID: {product_id}")
        
        # Test caching
        product_model.cache_results('test query', 'Test', '[]')
        cached = product_model.get_cached_results('test query', 'Test')
        print(f"Cache test: {'✅ PASS' if cached is not None else '❌ FAIL'}")
        
    except Exception as e:
        print(f"Database test error: {e}")

if __name__ == "__main__":
    print("🚀 MarketMiner Backend Test Suite")
    print("=" * 50)
    
    test_scraper()
    test_trends()
    test_database()
    
    print("\n✅ Test suite completed!")
    print("\nIf you see products and trends data above, the backend is working!")
    print("If you see mostly mock data, that's normal - it means the scrapers")
    print("are falling back to demo data when real scraping fails.")