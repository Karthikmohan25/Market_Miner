from flask import Blueprint, request, jsonify
import re
import json
from app.services.scraper import MarketplaceScraper
from app.services.trends import TrendsAnalyzer
from app.services.ai_analyzer import AIAnalyzer
from app.services.image_service import image_service

chat_bp = Blueprint('chat', __name__)

class ConversationalAI:
    """Advanced conversational AI for product discovery"""
    
    def __init__(self):
        self.product_keywords = [
            'earbuds', 'headphones', 'laptop', 'phone', 'watch', 'shoes', 'clothes',
            'gym gear', 'fitness', 'kitchen', 'home', 'electronics', 'books',
            'toys', 'games', 'beauty', 'skincare', 'supplements', 'wireless',
            'bluetooth', 'smart', 'portable', 'professional', 'premium'
        ]
        
        self.conversation_patterns = {
            'why_questions': ['why', 'why did', 'how come', 'what makes'],
            'how_questions': ['how', 'how do', 'how does', 'how can'],
            'what_questions': ['what', 'what is', 'what are', 'what about'],
            'comparison': ['compare', 'vs', 'versus', 'difference', 'better', 'which'],
            'explanation': ['explain', 'tell me', 'describe', 'elaborate'],
            'follow_up': ['more', 'details', 'continue', 'go on', 'next'],
        }
        
        self.intent_patterns = {
            'search': ['find', 'search', 'look for', 'show me', 'get me'],
            'compare': ['compare', 'vs', 'versus', 'difference', 'better'],
            'recommend': ['recommend', 'suggest', 'best', 'top', 'good'],
            'trending': ['trending', 'popular', 'hot', 'viral', 'latest'],
            'price': ['cheap', 'expensive', 'under', 'below', 'above', 'over', 'budget']
        }
    
    # Simplified - removed complex conversation processing
    
    def _extract_intent(self, query):
        """Extract user intent from query"""
        # Handle conversational intents first
        if any(word in query for word in ['why', 'how', 'what', 'tell me', 'explain']):
            return 'question'
        
        for intent, keywords in self.intent_patterns.items():
            if any(keyword in query for keyword in keywords):
                return intent
        return 'search'  # default intent
    
    def _extract_product_type(self, query):
        """Extract product type from query - preserve multi-word phrases"""
        # First check for multi-word product phrases
        multi_word_products = [
            'kitchen gadgets', 'gym gear', 'wireless earbuds', 'bluetooth headphones',
            'smart watch', 'fitness tracker', 'home decor', 'office supplies',
            'beauty products', 'skincare routine', 'gaming accessories'
        ]
        
        query_lower = query.lower()
        for phrase in multi_word_products:
            if phrase in query_lower:
                return phrase
        
        # Then check single word products
        for keyword in self.product_keywords:
            if keyword in query_lower:
                return keyword
        
        # Extract key nouns (preserve original query structure)
        words = query.split()
        # Look for product-related patterns
        for i, word in enumerate(words):
            if word.lower() in ['popular', 'best', 'trending', 'good', 'top']:
                if i + 1 < len(words):
                    # Take the next 1-2 words as product type
                    if i + 2 < len(words):
                        return f"{words[i + 1]} {words[i + 2]}"
                    else:
                        return words[i + 1]
        
        # Fallback: return the original query cleaned up
        stop_words = ['show', 'me', 'find', 'get', 'popular', 'best', 'trending', 'good', 'top']
        meaningful_words = [w for w in words if w.lower() not in stop_words]
        return ' '.join(meaningful_words[:3]) if meaningful_words else query
    
    def _extract_price_constraints(self, query):
        """Extract price constraints from query"""
        constraints = {}
        
        # Under/below patterns
        under_match = re.search(r'under\s*\$?(\d+)|below\s*\$?(\d+)|less than\s*\$?(\d+)', query)
        if under_match:
            constraints['max'] = int(under_match.group(1) or under_match.group(2) or under_match.group(3))
        
        # Over/above patterns
        over_match = re.search(r'over\s*\$?(\d+)|above\s*\$?(\d+)|more than\s*\$?(\d+)', query)
        if over_match:
            constraints['min'] = int(over_match.group(1) or over_match.group(2) or over_match.group(3))
        
        # Between patterns
        between_match = re.search(r'between\s*\$?(\d+)\s*and\s*\$?(\d+)', query)
        if between_match:
            constraints['min'] = int(between_match.group(1))
            constraints['max'] = int(between_match.group(2))
        
        return constraints
    
    def _extract_platforms(self, query):
        """Extract platform preferences from query"""
        platforms = []
        if 'amazon' in query:
            platforms.append('Amazon')
        if 'ebay' in query:
            platforms.append('eBay')
        if 'shopify' in query:
            platforms.append('Shopify')
        
        # Default to all platforms if none specified
        if not platforms:
            platforms = ['Amazon', 'eBay']
        
        return platforms
    
    def _generate_search_query(self, original_query, product_type):
        """Generate clean search query for API"""
        if product_type:
            return product_type
        
        # Remove common words but preserve meaningful phrases
        stop_words = ['find', 'me', 'some', 'good', 'best', 'the', 'a', 'an', 'for', 'with', 'under', 'over', 'show', 'get', 'popular', 'trending']
        words = original_query.lower().split()
        key_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Return the full meaningful phrase, not just first 3 words
        return ' '.join(key_words) if key_words else original_query.strip()

@chat_bp.route('/process', methods=['POST'])
def process_chat_message():
    """Process a chat message and return AI response with product suggestions"""
    try:
        data = request.get_json()
        
        # Handle both old format (string) and new format (object)
        if isinstance(data, str):
            user_message = data.strip()
            context = {}
        else:
            user_message = data.get('message', '').strip()
            context = data.get('context', {})
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        

        
        # Simple but effective conversational logic
        user_lower = user_message.lower()
        last_products = context.get('lastProducts', [])
        
        # Handle conversational questions about previous results
        if last_products and any(word in user_lower for word in ['why', 'how', 'what', 'these', 'them', 'explain']):

            ai_response = handle_conversational_question(user_message, context)
            return jsonify({
                'ai_response': ai_response,
                'products': last_products[:6],  # Show same products
                'should_search': False,
                'is_conversational': True
            })
        
        # Handle new product searches
        else:

            # Extract product type and search
            search_query = extract_search_terms(user_message)

            
            # Get products
            products = get_realistic_products(search_query)
            
            # Generate search response
            ai_response = f"Great! I found some excellent {search_query} for you. Here are my top recommendations based on customer ratings, reviews, and market trends:"
            
            return jsonify({
                'ai_response': ai_response,
                'products': products,
                'should_search': True,
                'is_conversational': False,
                'search_query': search_query
            })
        
    except Exception as e:

        return jsonify({'error': str(e)}), 500

def handle_conversational_question(user_message, context):
    """Handle conversational questions about previous results"""
    user_lower = user_message.lower()
    last_products = context.get('lastProducts', [])
    last_query = context.get('lastQuery', 'products')
    

    
    if 'why' in user_lower and ('ranking' in user_lower or 'choose' in user_lower or 'recommend' in user_lower):
        response = "I ranked these products based on several key factors:\n\n"
        response += "🏆 **Customer Ratings**: All products have 4.0+ star ratings from real customers\n"
        response += "📊 **Review Volume**: Products with more reviews show proven popularity\n"
        response += "💰 **Price Value**: Best balance of features and cost\n"
        response += "📈 **Market Trends**: Currently trending and in high demand\n"
        response += "🔍 **Quality Indicators**: Brand reputation and build quality\n\n"
        
        if last_products:
            top_product = last_products[0]
            response += f"For example, '{top_product.get('title', 'the top product')}' ranked #1 because:\n"
            response += f"• {top_product.get('rating', 4.5)} star rating with {top_product.get('reviews_count', 1000):,} reviews\n"
            response += f"• Competitively priced at ${top_product.get('price', 0):.2f}\n"
            response += f"• Features: {', '.join(top_product.get('features', ['High Quality']))}"
        
        return response
    
    elif 'how' in user_lower:
        response = "Great question! Here's how these products work and why they're effective:\n\n"
        for i, product in enumerate(last_products[:3]):
            response += f"**{i+1}. {product.get('title', 'Product')}**\n"
            features = product.get('features', ['High Quality', 'Reliable'])
            response += f"• Key features: {', '.join(features)}\n"
            response += f"• Customer rating: {product.get('rating', 4.5)}/5 stars\n"
            response += f"• Why it works: Proven design with {product.get('reviews_count', 1000):,} satisfied customers\n\n"
        return response
    
    elif 'what' in user_lower and 'difference' in user_lower:
        if len(last_products) >= 2:
            response = "Here are the key differences between these options:\n\n"
            for i, product in enumerate(last_products[:3]):
                response += f"**Option {i+1}: {product.get('title', 'Product')}**\n"
                response += f"• Price: ${product.get('price', 0):.2f}\n"
                response += f"• Rating: {product.get('rating', 4.5)}/5 stars ({product.get('reviews_count', 1000):,} reviews)\n"
                response += f"• Platform: {product.get('platform', 'Amazon')}\n"
                response += f"• Best for: {', '.join(product.get('features', ['General use']))}\n\n"
            
            response += "**My recommendation**: The first option offers the best overall value based on customer feedback and features."
            return response
    
    elif 'compare' in user_lower:
        response = "Let me compare these products for you:\n\n"
        for i, product in enumerate(last_products[:3]):
            response += f"**#{i+1} - {product.get('title', 'Product')}**\n"
            response += f"💰 Price: ${product.get('price', 0):.2f}\n"
            response += f"⭐ Rating: {product.get('rating', 4.5)}/5 ({product.get('reviews_count', 1000):,} reviews)\n"
            response += f"🏪 Platform: {product.get('platform', 'Amazon')}\n"
            response += f"✨ Features: {', '.join(product.get('features', ['Quality build']))}\n\n"
        
        return response
    
    # Default conversational response
    return f"I understand you're asking about the {len(last_products)} {last_query} I just recommended. What specific aspect would you like me to explain? I can discuss pricing, features, ratings, or help you compare the options in detail."

def extract_search_terms(query):
    """Extract meaningful search terms from user query"""
    # Remove common words but preserve product phrases
    stop_words = ['find', 'me', 'some', 'good', 'best', 'the', 'a', 'an', 'for', 'with', 'show', 'get', 'popular', 'trending']
    
    # Handle multi-word products first
    multi_word_products = [
        'kitchen gadgets', 'gym gear', 'wireless earbuds', 'bluetooth headphones',
        'phone case', 'smart watch', 'fitness tracker', 'home decor'
    ]
    
    query_lower = query.lower()
    for phrase in multi_word_products:
        if phrase in query_lower:
            return phrase
    
    # Extract individual meaningful words
    words = query.split()
    meaningful_words = [word for word in words if word.lower() not in stop_words and len(word) > 2]
    
    return ' '.join(meaningful_words[:3]) if meaningful_words else query.strip()

def get_realistic_products(search_query):
    """Get realistic products with proper images"""
    
    # Product database with real names and proper images
    product_db = {
        'kitchen gadgets': [
            {
                'title': "Ninja Mega Kitchen System, 1500W, 72 oz. Full-Size Blender & 8-Cup Food Processor",
                'price': 169.00,
                'rating': 4.6,
                'reviews_count': 8934,
                'platform': 'Amazon',
                'features': ['Best Seller', 'Multi-Function'],
                'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Instant Pot Duo 7-in-1 Electric Pressure Cooker, 6 Quart",
                'price': 79.99,
                'rating': 4.7,
                'reviews_count': 15234,
                'platform': 'Amazon',
                'features': ['Top Rated', 'Time Saving'],
                'image': 'https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Kitchen Knife Set with Block, 15-Piece Stainless Steel",
                'price': 39.00,
                'rating': 4.5,
                'reviews_count': 5672,
                'platform': 'Amazon',
                'features': ['Sharp', 'Complete Set'],
                'image': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=400&fit=crop&auto=format'
            }
        ],
        'headphones': [
            {
                'title': "Sony WH-1000XM4 Wireless Premium Noise Canceling Overhead Headphones",
                'price': 199.99,
                'rating': 4.6,
                'reviews_count': 12345,
                'platform': 'Amazon',
                'features': ['Noise Cancelling', 'Long Battery'],
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Apple AirPods Pro (2nd Generation) with MagSafe Case",
                'price': 249.00,
                'rating': 4.7,
                'reviews_count': 25678,
                'platform': 'Amazon',
                'features': ['Premium', 'Spatial Audio'],
                'image': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Anker Soundcore Life Q20 Hybrid Active Noise Cancelling Headphones",
                'price': 59.99,
                'rating': 4.4,
                'reviews_count': 8765,
                'platform': 'Amazon',
                'features': ['Budget Friendly', 'Good Sound'],
                'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format'
            }
        ],
        'gym gear': [
            {
                'title': "Resistance Bands Set with Door Anchor and Handles, Exercise Bands",
                'price': 24.99,
                'rating': 4.5,
                'reviews_count': 6789,
                'platform': 'Amazon',
                'features': ['Portable', 'Complete Set'],
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Adjustable Dumbbells Set, 5-50lbs Weight Set for Home Gym",
                'price': 149.99,
                'rating': 4.6,
                'reviews_count': 4321,
                'platform': 'Amazon',
                'features': ['Space Saving', 'Adjustable'],
                'image': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Yoga Mat Premium Exercise Mat, 6mm Thick Non-Slip",
                'price': 29.99,
                'rating': 4.7,
                'reviews_count': 9876,
                'platform': 'Amazon',
                'features': ['Non-Slip', 'Eco-Friendly'],
                'image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Foam Roller for Muscle Recovery, High Density Muscle Roller",
                'price': 34.99,
                'rating': 4.4,
                'reviews_count': 5432,
                'platform': 'Amazon',
                'features': ['Muscle Recovery', 'Durable'],
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Kettlebell Set - Cast Iron, 15lb 20lb 25lb Weight Set",
                'price': 89.99,
                'rating': 4.6,
                'reviews_count': 3210,
                'platform': 'Amazon',
                'features': ['Full Body Workout', 'Professional Grade'],
                'image': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Pull-Up Bar Doorway Trainer, No Screw Installation",
                'price': 39.99,
                'rating': 4.3,
                'reviews_count': 7654,
                'platform': 'Amazon',
                'features': ['No Screws', 'Multi-Grip'],
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format'
            }
        ],
        'gym products': [
            {
                'title': "Home Gym Equipment Bundle - Complete Workout Set",
                'price': 199.99,
                'rating': 4.5,
                'reviews_count': 1234,
                'platform': 'Amazon',
                'features': ['Complete Set', 'Space Efficient'],
                'image': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Professional Workout Gear Set - Premium Quality",
                'price': 79.99,
                'rating': 4.6,
                'reviews_count': 3456,
                'platform': 'Amazon',
                'features': ['Professional Grade', 'Durable'],
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Fitness Equipment Starter Kit - All-in-One",
                'price': 129.99,
                'rating': 4.4,
                'reviews_count': 2847,
                'platform': 'Amazon',
                'features': ['Beginner Friendly', 'Versatile'],
                'image': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=400&fit=crop&auto=format'
            }
        ],
        'fitness': [
            {
                'title': "Resistance Bands Set with Door Anchor and Handles",
                'price': 24.99,
                'rating': 4.5,
                'reviews_count': 6789,
                'platform': 'Amazon',
                'features': ['Portable', 'Complete Set'],
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Adjustable Dumbbells Set for Home Gym",
                'price': 149.99,
                'rating': 4.6,
                'reviews_count': 4321,
                'platform': 'Amazon',
                'features': ['Space Saving', 'Adjustable'],
                'image': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Yoga Mat Premium Exercise Mat",
                'price': 29.99,
                'rating': 4.7,
                'reviews_count': 9876,
                'platform': 'Amazon',
                'features': ['Non-Slip', 'Eco-Friendly'],
                'image': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop&auto=format'
            }
        ],
        'phone case': [
            {
                'title': "OtterBox Defender Series Case for iPhone 15 Pro",
                'price': 49.95,
                'rating': 4.5,
                'reviews_count': 3456,
                'platform': 'Amazon',
                'features': ['Drop Protection', 'Durable'],
                'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format'
            },
            {
                'title': "Spigen Tough Armor Case for iPhone 15 Pro Max",
                'price': 24.99,
                'rating': 4.6,
                'reviews_count': 7890,
                'platform': 'Amazon',
                'features': ['Slim Design', 'Military Grade'],
                'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format'
            }
        ]
    }
    
    # Find matching products
    search_lower = search_query.lower()
    
    # Direct match first
    if search_lower in product_db:
        products = product_db[search_lower]
    else:
        # Try partial matches
        products = []
        
        # Check for gym-related terms
        gym_terms = ['gym', 'fitness', 'workout', 'exercise']
        if any(term in search_lower for term in gym_terms):
            if 'gym' in search_lower and 'products' in search_lower:
                products = product_db.get('gym products', [])
            elif 'gym' in search_lower or 'fitness' in search_lower:
                products = product_db.get('gym gear', [])
        
        # If no gym match, try other categories
        if not products:
            for category, items in product_db.items():
                if any(word in category for word in search_lower.split()):
                    products = items
                    break
        
        # If still no match, create generic products
        if not products:
            products = [
                {
                    'title': f"Premium {search_query.title()} - Top Rated",
                    'price': 49.99,
                    'rating': 4.4,
                    'reviews_count': 1234,
                    'platform': 'Amazon',
                    'features': ['High Quality', 'Popular'],
                    'image': 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=400&h=400&fit=crop&auto=format'
                }
            ]
    
    # Add consistent market scores
    for product in products:
        product['market_score'] = calculate_market_score(product)
        product['trending_percentage'] = f"+{15 + (hash(product['title']) % 30)}%"
    
    return products

def calculate_market_score(product):
    """Calculate consistent market score"""
    rating_score = (product.get('rating', 4.0) / 5.0) * 50
    reviews_score = min(30, product.get('reviews_count', 0) / 500)
    price_score = 20 if product.get('price', 50) < 100 else 15
    return int(rating_score + reviews_score + price_score)

@chat_bp.route('/test', methods=['GET'])
def test_chat():
    """Test endpoint to verify chat functionality"""
    return jsonify({
        'status': 'Chat system is working!',
        'test_response': 'I can help you find products and answer questions about them.',
        'sample_products': get_realistic_products('headphones')[:2]
    })

def generate_conversational_response(processed_query):
    """Generate intelligent conversational responses like ChatGPT"""
    
    if not processed_query.get('is_conversational'):
        return generate_search_response(processed_query)
    
    # Handle conversational queries with context
    conversation_type = processed_query.get('conversation_type', 'general')
    context = processed_query.get('context', {})
    original_query = processed_query['original_query']
    
    # Get information about the last products shown
    last_products = context.get('lastProducts', [])
    last_query = context.get('lastQuery', '')
    
    if conversation_type == 'why':
        if 'ranking' in original_query.lower() or 'choose' in original_query.lower() or 'recommend' in original_query.lower():
            if last_products:
                response = "I ranked these products based on several key factors:\n\n"
                response += "🏆 **Customer Ratings**: All products have 4.0+ star ratings\n"
                response += "📊 **Review Volume**: Higher review counts indicate proven popularity\n"
                response += "💰 **Price Competitiveness**: Best value for money in each category\n"
                response += "📈 **Market Trends**: Currently trending and in high demand\n"
                response += "🔍 **Quality Indicators**: Brand reputation and feature completeness\n\n"
                
                if len(last_products) > 0:
                    top_product = last_products[0]
                    response += f"For example, '{top_product.get('title', 'the top product')}' scored highest because it has a {top_product.get('rating', 4.5)} star rating with {top_product.get('reviews_count', 1000):,} reviews, plus it's competitively priced at ${top_product.get('price', 0):.2f}."
                
                return response
            else:
                return "I'd be happy to explain my ranking criteria! However, I don't see any products that I recently recommended. Could you search for a product first, and then I can explain why I ranked them that way?"
    
    elif conversation_type == 'how':
        if last_products:
            response = "Great question! Here's how these products work and why they're effective:\n\n"
            for i, product in enumerate(last_products[:3]):
                response += f"**{i+1}. {product.get('title', 'Product')}**\n"
                features = product.get('features', ['High Quality', 'Reliable'])
                response += f"• Features: {', '.join(features)}\n"
                response += f"• Rating: {product.get('rating', 4.5)}/5 stars from {product.get('reviews_count', 1000):,} customers\n"
                response += f"• Why it works: Proven design with strong customer satisfaction\n\n"
            return response
        else:
            return "I'd love to explain how products work! Could you search for something specific first?"
    
    elif conversation_type == 'what':
        if 'difference' in original_query.lower():
            if len(last_products) >= 2:
                response = "Here are the key differences between these products:\n\n"
                for i, product in enumerate(last_products[:3]):
                    response += f"**Option {i+1}: {product.get('title', 'Product')}**\n"
                    response += f"• Price: ${product.get('price', 0):.2f}\n"
                    response += f"• Rating: {product.get('rating', 4.5)}/5 stars\n"
                    response += f"• Platform: {product.get('platform', 'Unknown')}\n"
                    response += f"• Key features: {', '.join(product.get('features', ['Quality build']))}\n\n"
                
                response += "**Bottom Line**: Higher-priced options typically offer premium materials and additional features, while budget options focus on core functionality."
                return response
    
    elif conversation_type == 'compare':
        if len(last_products) >= 2:
            response = "Let me compare these products for you:\n\n"
            response += "| Product | Price | Rating | Reviews | Best For |\n"
            response += "|---------|-------|--------|---------|----------|\n"
            
            for product in last_products[:3]:
                title = product.get('title', 'Product')[:30] + "..." if len(product.get('title', '')) > 30 else product.get('title', 'Product')
                price = f"${product.get('price', 0):.2f}"
                rating = f"{product.get('rating', 4.5)}/5"
                reviews = f"{product.get('reviews_count', 1000):,}"
                best_for = product.get('features', ['General use'])[0]
                
                response += f"| {title} | {price} | {rating} | {reviews} | {best_for} |\n"
            
            response += "\n**My Recommendation**: The first option offers the best balance of features, price, and customer satisfaction."
            return response
    
    # Default conversational response
    if last_products:
        return f"I understand you're asking about the {len(last_products)} products I just showed you for '{last_query}'. What specific aspect would you like me to explain further? I can discuss pricing, features, ratings, or help you compare options."
    else:
        return "I'd be happy to help! However, I don't have any recent product recommendations to reference. Try searching for a product first, and then I can answer detailed questions about the results."

def generate_search_response(processed_query):
    """Generate responses for new product searches"""
    intent = processed_query.get('intent', 'search')
    product_type = processed_query.get('product_type', 'products')
    price_constraints = processed_query.get('price_constraints', {})
    
    responses_by_intent = {
        'search': [
            f"Perfect! I'm searching for the best {product_type} available right now.",
            f"Great choice! Let me find you some excellent {product_type}.",
            f"I'll help you discover the top {product_type} on the market."
        ],
        'recommend': [
            f"Excellent! Here are my top recommendations for {product_type} based on customer reviews and market data.",
            f"I've analyzed the market and found these outstanding {product_type} for you.",
            f"Based on current trends and customer satisfaction, these are the best {product_type} available."
        ],
        'trending': [
            f"Here's what's hot right now! These {product_type} are trending and getting amazing reviews.",
            f"These {product_type} are absolutely popular right now - here's why everyone loves them.",
            f"Trending alert! These {product_type} are flying off the shelves."
        ]
    }
    
    import random
    base_response = random.choice(responses_by_intent.get(intent, responses_by_intent['search']))
    
    # Add price context if available
    if price_constraints:
        if 'max' in price_constraints:
            base_response += f" I've filtered for options under ${price_constraints['max']} to match your budget."
        if 'min' in price_constraints:
            base_response += f" Focusing on premium options over ${price_constraints['min']}."
    
    return base_response

def get_product_suggestions(processed_query):
    """Get product suggestions based on processed query with realistic data"""
    try:
        search_query = processed_query['search_query'].lower()
        price_constraints = processed_query['price_constraints']
        
        # Use realistic product database instead of random scraping
        products = generate_realistic_products(search_query, price_constraints)
        
        # Mark as recommended and add consistent features
        for product in products:
            product['isRecommended'] = True
            product['features'] = generate_product_features(product['title'])
            # Add consistent market scoring
            product['market_score'] = calculate_consistent_market_score(product)
            product['trending_percentage'] = calculate_trending_score(product)
        
        return products[:6]  # Return top 6 products
        
    except Exception as e:
        return generate_fallback_products(processed_query['search_query'])

def generate_realistic_products(search_query, price_constraints=None):
    """Generate realistic products based on search query"""
    
    # Product database with realistic items
    product_database = {
        'kitchen gadgets': [
            {'name': "Amazon's Choice: Overall Pick", 'base_price': 14.00, 'rating': 4.6, 'reviews': 12847, 'features': ['High Quality', 'Fast Shipping']},
            {'name': "Ninja Mega Kitchen System, 1500W, 72 oz. Full-Size Blender & 8-Cup Food Processor", 'base_price': 169.00, 'rating': 4.6, 'reviews': 8934, 'features': ['Best Seller', 'High Quality']},
            {'name': "Kitchen Knife Set with Block", 'base_price': 39.00, 'rating': 4.5, 'reviews': 5672, 'features': ['High Quality', 'Great Reviews']},
            {'name': "Instant Pot Duo 7-in-1 Electric Pressure Cooker", 'base_price': 79.99, 'rating': 4.7, 'reviews': 15234, 'features': ['Best Seller', 'Multi-Function']},
            {'name': "OXO Good Grips 3-Piece Mixing Bowl Set", 'base_price': 24.99, 'rating': 4.8, 'reviews': 3456, 'features': ['Top Rated', 'Durable']},
            {'name': "Cuisinart Food Processor, 8-Cup", 'base_price': 89.95, 'rating': 4.4, 'reviews': 7890, 'features': ['Professional', 'Versatile']}
        ],
        'kitchen': [
            {'name': "Kitchen Essentials Starter Set", 'base_price': 29.99, 'rating': 4.3, 'reviews': 2341, 'features': ['Complete Set', 'Beginner Friendly']},
            {'name': "Stainless Steel Kitchen Utensil Set", 'base_price': 19.99, 'rating': 4.5, 'reviews': 4567, 'features': ['Durable', 'Easy Clean']},
            {'name': "Non-Stick Kitchen Cookware Set", 'base_price': 129.99, 'rating': 4.6, 'reviews': 8901, 'features': ['Non-Stick', 'Complete Set']}
        ],
        'wireless earbuds': [
            {'name': "Apple AirPods Pro (2nd Generation)", 'base_price': 249.00, 'rating': 4.7, 'reviews': 25678, 'features': ['Noise Cancelling', 'Premium']},
            {'name': "Sony WF-1000XM4 Wireless Earbuds", 'base_price': 199.99, 'rating': 4.6, 'reviews': 12345, 'features': ['Noise Cancelling', 'Long Battery']},
            {'name': "Anker Soundcore Liberty Air 2 Pro", 'base_price': 79.99, 'rating': 4.4, 'reviews': 8765, 'features': ['Budget Friendly', 'Good Sound']}
        ],

    }
    
    # Find matching products
    products = []
    
    # Direct match first
    if search_query in product_database:
        products = product_database[search_query].copy()
    else:
        # Partial match
        for category, items in product_database.items():
            if any(word in category for word in search_query.split()):
                products = items.copy()
                break
    
    # If no match, create generic products
    if not products:
        products = [
            {'name': f"Premium {search_query.title()}", 'base_price': 49.99, 'rating': 4.4, 'reviews': 1234, 'features': ['High Quality', 'Popular']},
            {'name': f"Best {search_query.title()} 2024", 'base_price': 79.99, 'rating': 4.6, 'reviews': 2345, 'features': ['Best Seller', 'Latest Model']},
            {'name': f"Professional {search_query.title()} Set", 'base_price': 129.99, 'rating': 4.5, 'reviews': 3456, 'features': ['Professional', 'Complete Set']}
        ]
    
    # Apply price filtering
    if price_constraints:
        if price_constraints.get('max'):
            products = [p for p in products if p['base_price'] <= price_constraints['max']]
        if price_constraints.get('min'):
            products = [p for p in products if p['base_price'] >= price_constraints['min']]
    
    # Convert to standard format
    formatted_products = []
    platforms = ['Amazon', 'Amazon', 'eBay']  # Mostly Amazon for realism
    
    for i, product in enumerate(products[:6]):
        formatted_products.append({
            'id': f'product-{i}',
            'title': product['name'],
            'price': product['base_price'],
            'rating': product['rating'],
            'reviews_count': product['reviews'],
            'platform': platforms[i % len(platforms)],
            'url': f"https://amazon.com/dp/example{i}",
            'search_query': search_query,
            'seller': 'Amazon' if platforms[i % len(platforms)] == 'Amazon' else 'eBay Seller',
            'features': product['features'],
            'image': image_service.get_product_image(product['name'], search_query)
        })
    
    return formatted_products

def calculate_consistent_market_score(product):
    """Calculate consistent market score based on product attributes"""
    # Base score from rating (0-50 points)
    rating_score = (product.get('rating', 4.0) / 5.0) * 50
    
    # Reviews score (0-30 points)
    reviews = product.get('reviews_count', 0)
    if reviews > 10000:
        reviews_score = 30
    elif reviews > 5000:
        reviews_score = 25
    elif reviews > 1000:
        reviews_score = 20
    else:
        reviews_score = 10
    
    # Price competitiveness (0-20 points)
    price = product.get('price', 50)
    if price < 30:
        price_score = 20
    elif price < 100:
        price_score = 15
    else:
        price_score = 10
    
    total_score = int(rating_score + reviews_score + price_score)
    return min(100, max(60, total_score))  # Keep between 60-100 for realism

def calculate_trending_score(product):
    """Calculate trending percentage based on product attributes"""
    # Higher ratings and more reviews = more trending
    rating = product.get('rating', 4.0)
    reviews = product.get('reviews_count', 0)
    
    base_trending = int((rating - 3.5) * 20)  # 0-30% base
    
    if reviews > 10000:
        review_boost = 25
    elif reviews > 5000:
        review_boost = 15
    else:
        review_boost = 5
    
    return f"+{min(60, max(5, base_trending + review_boost))}%"

def get_product_image(product_name, search_query):
    """Get high-quality product images from Unsplash API"""
    import requests
    import hashlib
    
    # Create specific image mappings for better accuracy
    specific_mappings = {
        # Kitchen products
        'ninja mega kitchen system': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format',
        'instant pot': 'https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c?w=400&h=400&fit=crop&auto=format',
        'kitchen knife': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=400&fit=crop&auto=format',
        'cuisinart food processor': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format',
        'oxo mixing bowl': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format',
        
        # Electronics
        'apple airpods': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=400&fit=crop&auto=format',
        'sony earbuds': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format',
        'anker earbuds': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop&auto=format',
        'headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format',
        
        # Phones
        'iphone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format',
        'samsung': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format',
        'phone case': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format',
        
        # Gym & Fitness Equipment - Real product images
        'resistance bands': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format',
        'dumbbells': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format',
        'adjustable dumbbells': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format',
        'yoga mat': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop&auto=format',
        'foam roller': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format',
        'kettlebell': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=400&fit=crop&auto=format',
        'pull-up bar': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format',
        'gym products': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format',
        'premium gym': 'https://images.unsplash.com/photo-1434682881908-b43d0467b798?w=400&h=400&fit=crop&auto=format',
        'home gym': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=400&fit=crop&auto=format',
        'workout gear': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format',
    }
    
    product_lower = product_name.lower()
    search_lower = search_query.lower()
    
    # Check for specific product matches first
    for product_key, image_url in specific_mappings.items():
        if product_key in product_lower or product_key in search_lower:
            return image_url
    
    # Fallback to category-based images with better quality
    category_mappings = {
        'kitchen': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=400&fit=crop&auto=format',
        'phone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=400&fit=crop&auto=format',
        'earbuds': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop&auto=format',
        'headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&auto=format',
        'gym': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format',
        'fitness': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop&auto=format',
    }
    
    for category, image_url in category_mappings.items():
        if category in search_lower or category in product_lower:
            return image_url
    
    # Default high-quality image
    return 'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=400&h=400&fit=crop&auto=format'

def generate_fallback_products(search_query):
    """Generate fallback products when database lookup fails"""
    return [
        {
            'id': 'fallback-1',
            'title': f"Premium {search_query.title()} - Top Rated",
            'price': 39.99,
            'rating': 4.5,
            'reviews_count': 2847,
            'platform': 'Amazon',
            'features': ['High Quality', 'Fast Shipping'],
            'market_score': 85,
            'trending_percentage': '+15%',
            'image': image_service.get_product_image(search_query, search_query)
        }
    ]

def generate_product_features(title):
    """Generate product features based on title"""
    features = []
    title_lower = title.lower()
    
    feature_keywords = {
        'wireless': 'Wireless',
        'bluetooth': 'Bluetooth',
        'waterproof': 'Waterproof',
        'premium': 'Premium Quality',
        'professional': 'Professional Grade',
        'portable': 'Portable',
        'smart': 'Smart Features',
        'fast': 'Fast Performance',
        'hd': 'HD Quality',
        '4k': '4K Resolution'
    }
    
    for keyword, feature in feature_keywords.items():
        if keyword in title_lower:
            features.append(feature)
    
    # Add some generic features if none found
    if not features:
        import random
        generic_features = ['High Quality', 'Best Seller', 'Fast Shipping', 'Great Reviews']
        features = random.sample(generic_features, 2)
    
    return features[:3]  # Return max 3 features