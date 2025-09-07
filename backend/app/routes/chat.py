from flask import Blueprint, request, jsonify
import re
import json
from app.services.scraper import MarketplaceScraper
from app.services.trends import TrendsAnalyzer
from app.services.ai_analyzer import AIAnalyzer

chat_bp = Blueprint('chat', __name__)

class NLPProcessor:
    """Simple Natural Language Processing for product queries"""
    
    def __init__(self):
        self.product_keywords = [
            'earbuds', 'headphones', 'laptop', 'phone', 'watch', 'shoes', 'clothes',
            'gym gear', 'fitness', 'kitchen', 'home', 'electronics', 'books',
            'toys', 'games', 'beauty', 'skincare', 'supplements', 'wireless',
            'bluetooth', 'smart', 'portable', 'professional', 'premium'
        ]
        
        self.intent_patterns = {
            'search': ['find', 'search', 'look for', 'show me', 'get me'],
            'compare': ['compare', 'vs', 'versus', 'difference', 'better'],
            'recommend': ['recommend', 'suggest', 'best', 'top', 'good'],
            'trending': ['trending', 'popular', 'hot', 'viral', 'latest'],
            'price': ['cheap', 'expensive', 'under', 'below', 'above', 'over', 'budget']
        }
    
    def process_query(self, query):
        """Process natural language query and extract structured information"""
        query_lower = query.lower()
        
        # Extract intent
        intent = self._extract_intent(query_lower)
        
        # Extract product type
        product_type = self._extract_product_type(query_lower)
        
        # Extract price constraints
        price_constraints = self._extract_price_constraints(query_lower)
        
        # Extract platform preferences
        platforms = self._extract_platforms(query_lower)
        
        # Generate search query
        search_query = self._generate_search_query(query, product_type)
        
        return {
            'intent': intent,
            'product_type': product_type,
            'price_constraints': price_constraints,
            'platforms': platforms,
            'search_query': search_query,
            'original_query': query
        }
    
    def _extract_intent(self, query):
        """Extract user intent from query"""
        for intent, keywords in self.intent_patterns.items():
            if any(keyword in query for keyword in keywords):
                return intent
        return 'search'  # default intent
    
    def _extract_product_type(self, query):
        """Extract product type from query"""
        for keyword in self.product_keywords:
            if keyword in query:
                return keyword
        
        # Try to extract noun phrases (simple approach)
        words = query.split()
        for i, word in enumerate(words):
            if word in ['for', 'some', 'a', 'an']:
                if i + 1 < len(words):
                    return words[i + 1]
        
        return None
    
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
        
        # Remove common words and extract key terms
        stop_words = ['find', 'me', 'some', 'good', 'best', 'the', 'a', 'an', 'for', 'with', 'under', 'over', 'show', 'get']
        words = original_query.lower().split()
        key_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return ' '.join(key_words[:3])  # Take first 3 key words

@chat_bp.route('/process', methods=['POST'])
def process_chat_message():
    """Process a chat message and return AI response with product suggestions"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        print(f"Processing chat message: {user_message}")
        
        # Process the natural language query
        nlp = NLPProcessor()
        processed_query = nlp.process_query(user_message)
        
        print(f"Processed query: {processed_query}")
        
        # Generate AI response based on intent
        ai_response = generate_ai_response(processed_query)
        
        # Get product suggestions if applicable
        products = []
        if processed_query['search_query']:
            products = get_product_suggestions(processed_query)
        
        return jsonify({
            'ai_response': ai_response,
            'products': products,
            'processed_query': processed_query,
            'should_search': bool(processed_query['search_query'])
        })
        
    except Exception as e:
        print(f"Error processing chat message: {e}")
        return jsonify({'error': str(e)}), 500

def generate_ai_response(processed_query):
    """Generate contextual AI response based on processed query"""
    intent = processed_query['intent']
    product_type = processed_query['product_type']
    price_constraints = processed_query['price_constraints']
    
    responses = {
        'search': [
            f"I'll help you find {product_type or 'products'}! Let me search across multiple platforms.",
            f"Great choice! Searching for {product_type or 'products'} now.",
            f"Perfect! I'm looking for the best {product_type or 'products'} available."
        ],
        'recommend': [
            f"I'd be happy to recommend the best {product_type or 'products'} based on current market trends!",
            f"Here are my top recommendations for {product_type or 'products'} based on ratings and reviews.",
            f"Based on market analysis, here are the {product_type or 'products'} I highly recommend."
        ],
        'trending': [
            f"Let me show you what's trending in {product_type or 'products'} right now!",
            f"Here are the hottest {product_type or 'products'} that everyone's talking about.",
            f"These {product_type or 'products'} are absolutely viral right now!"
        ],
        'compare': [
            f"I'll help you compare different {product_type or 'products'} to find the best value.",
            f"Great idea! Let me analyze the top {product_type or 'products'} for you.",
            f"Comparing {product_type or 'products'} across platforms to find your perfect match."
        ],
        'price': [
            f"Looking for budget-friendly {product_type or 'products'}? I've got you covered!",
            f"I'll find the best {product_type or 'products'} within your price range.",
            f"Smart shopping! Let me find {product_type or 'products'} that offer great value."
        ]
    }
    
    import random
    base_response = random.choice(responses.get(intent, responses['search']))
    
    # Add price context if available
    if price_constraints:
        if 'max' in price_constraints:
            base_response += f" I'll focus on options under ${price_constraints['max']}."
        if 'min' in price_constraints:
            base_response += f" Looking at premium options over ${price_constraints['min']}."
    
    return base_response

def get_product_suggestions(processed_query):
    """Get product suggestions based on processed query"""
    try:
        scraper = MarketplaceScraper()
        search_query = processed_query['search_query']
        platforms = processed_query['platforms']
        
        all_products = []
        
        # Get products from each platform
        for platform in platforms[:2]:  # Limit to 2 platforms for quick response
            if platform.lower() == 'amazon':
                products = scraper.search_amazon(search_query, 3)
            elif platform.lower() == 'ebay':
                products = scraper.search_ebay(search_query, 3)
            else:
                continue
            
            # Mark as recommended and add platform-specific data
            for product in products:
                product['isRecommended'] = True
                product['features'] = generate_product_features(product['title'])
            
            all_products.extend(products)
        
        # Filter by price constraints if specified
        price_constraints = processed_query['price_constraints']
        if price_constraints:
            filtered_products = []
            for product in all_products:
                price = product.get('price', 0)
                if price_constraints.get('min') and price < price_constraints['min']:
                    continue
                if price_constraints.get('max') and price > price_constraints['max']:
                    continue
                filtered_products.append(product)
            all_products = filtered_products
        
        return all_products[:6]  # Return top 6 products
        
    except Exception as e:
        print(f"Error getting product suggestions: {e}")
        return []

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