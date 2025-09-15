"""
Image service for fetching real product images
"""
import requests
import hashlib
from typing import Dict, Optional

class ProductImageService:
    """Service for getting high-quality product images"""
    
    def __init__(self):
        # High-quality curated product images
        self.product_image_database = {
            # Kitchen Equipment
            'ninja mega kitchen system': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format&q=80',
            'instant pot': 'https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c?w=400&h=400&fit=crop&auto=format&q=80',
            'kitchen knife set': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=400&fit=crop&auto=format&q=80',
            'cuisinart food processor': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format&q=80',
            'oxo mixing bowl': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format&q=80',
            'stainless steel utensil': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format&q=80',
            
            # Electronics & Audio
            'apple airpods pro': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=400&fit=crop&auto=format&q=80',
            'sony wf-1000xm4': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format&q=80',
            'anker soundcore': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop&auto=format&q=80',
            'wireless earbuds': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop&auto=format&q=80',
            'bluetooth headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format&q=80',
            
            # Mobile Phones
            'iphone 15 pro': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format&q=80',
            'samsung galaxy': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format&q=80',
            'phone case': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format&q=80',
            
            # Fitness & Gym Equipment
            'resistance bands set': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format&q=80',
            'adjustable dumbbells': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format&q=80',
            'yoga mat premium': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop&auto=format&q=80',
            'foam roller': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format&q=80',
            'kettlebell set': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=400&fit=crop&auto=format&q=80',
            'pull-up bar': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format&q=80',
            
            # Generic categories
            'premium gym products': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format&q=80',
            'home gym equipment': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=400&fit=crop&auto=format&q=80',
            'professional workout gear': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format&q=80',
        }
        
        # Category fallbacks
        self.category_images = {
            'kitchen': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format&q=80',
            'gym': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format&q=80',
            'fitness': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format&q=80',
            'electronics': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop&auto=format&q=80',
            'phone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format&q=80',
            'audio': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format&q=80',
        }
    
    def get_product_image(self, product_name: str, search_query: str = '') -> str:
        """Get the best matching product image"""
        product_lower = product_name.lower()
        search_lower = search_query.lower()
        
        # First, try exact product matches
        for product_key, image_url in self.product_image_database.items():
            if product_key in product_lower:
                return image_url
        
        # Then try partial matches with search query
        for product_key, image_url in self.product_image_database.items():
            if any(word in product_key for word in product_lower.split()):
                return image_url
        
        # Try search query matches
        for product_key, image_url in self.product_image_database.items():
            if product_key in search_lower:
                return image_url
        
        # Fallback to category images
        for category, image_url in self.category_images.items():
            if category in search_lower or category in product_lower:
                return image_url
        
        # Default high-quality image
        return 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=400&h=400&fit=crop&auto=format&q=80'
    
    def get_category_image(self, category: str) -> str:
        """Get category-specific image"""
        category_lower = category.lower()
        return self.category_images.get(category_lower, self.category_images['electronics'])
    
    def validate_image_url(self, url: str) -> bool:
        """Validate if image URL is accessible"""
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False

# Global instance
image_service = ProductImageService()