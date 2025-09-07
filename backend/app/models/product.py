import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Product:
    def __init__(self, db_path: str = 'database/marketminer.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL,
                rating REAL,
                reviews_count INTEGER,
                platform TEXT NOT NULL,
                seller TEXT,
                url TEXT,
                image_url TEXT,
                search_query TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                platform TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_product(self, product_data: Dict) -> int:
        """Save a product to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (title, price, rating, reviews_count, platform, seller, url, image_url, search_query)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product_data.get('title'),
            product_data.get('price'),
            product_data.get('rating'),
            product_data.get('reviews_count'),
            product_data.get('platform'),
            product_data.get('seller'),
            product_data.get('url'),
            product_data.get('image_url'),
            product_data.get('search_query')
        ))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_cached_results(self, query: str, platform: str) -> Optional[str]:
        """Get cached search results if they exist and are fresh"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for results within the last 24 hours
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        cursor.execute('''
            SELECT results FROM search_cache 
            WHERE query = ? AND platform = ? AND created_at > ?
            ORDER BY created_at DESC LIMIT 1
        ''', (query, platform, cutoff_time))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def cache_results(self, query: str, platform: str, results: str):
        """Cache search results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO search_cache (query, platform, results)
            VALUES (?, ?, ?)
        ''', (query, platform, results))
        
        conn.commit()
        conn.close()