import openai
from textblob import TextBlob
from typing import List, Dict
import os

class AIAnalyzer:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if self.openai_key:
            openai.api_key = self.openai_key
    
    def analyze_products(self, products: List[Dict], trend_data: Dict = None) -> Dict:
        """Analyze products and generate insights"""
        try:
            if self.openai_key:
                return self._analyze_with_openai(products, trend_data)
            else:
                return self._analyze_with_textblob(products, trend_data)
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return self._fallback_analysis(products, trend_data)
    
    def _analyze_with_openai(self, products: List[Dict], trend_data: Dict = None) -> Dict:
        """Use OpenAI GPT for analysis"""
        # Prepare product summary
        product_summary = self._prepare_product_summary(products)
        trend_summary = self._prepare_trend_summary(trend_data) if trend_data else ""
        
        prompt = f"""
        Analyze the following product data and provide insights:
        
        Products found:
        {product_summary}
        
        Trend data:
        {trend_summary}
        
        Please provide:
        1. Market opportunity assessment
        2. Competition level analysis
        3. Price range insights
        4. Key recommendations for entrepreneurs
        5. Potential challenges or risks
        
        Format your response as a structured analysis.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a market research analyst specializing in e-commerce product opportunities."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'analysis_type': 'openai',
                'summary': analysis,
                'opportunity_score': self._calculate_opportunity_score(products, trend_data),
                'key_insights': self._extract_key_insights(analysis)
            }
            
        except Exception as e:
            print(f"OpenAI analysis failed: {e}")
            return self._analyze_with_textblob(products, trend_data)
    
    def _analyze_with_textblob(self, products: List[Dict], trend_data: Dict = None) -> Dict:
        """Fallback analysis using TextBlob"""
        insights = []
        
        if products:
            avg_price = sum(p.get('price', 0) for p in products) / len(products)
            avg_rating = sum(p.get('rating', 0) for p in products if p.get('rating', 0) > 0)
            avg_rating = avg_rating / len([p for p in products if p.get('rating', 0) > 0]) if avg_rating > 0 else 0
            
            insights.append(f"Average price: ${avg_price:.2f}")
            insights.append(f"Average rating: {avg_rating:.1f}/5.0")
            insights.append(f"Found {len(products)} products across platforms")
            
            # Price analysis
            prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
            if prices:
                price_range = max(prices) - min(prices)
                if price_range > avg_price * 0.5:
                    insights.append("High price variation suggests market opportunity")
                else:
                    insights.append("Consistent pricing indicates mature market")
        
        # Trend analysis
        if trend_data and 'trend_analysis' in trend_data:
            for keyword, analysis in trend_data['trend_analysis'].items():
                direction = analysis.get('trend_direction', 'stable')
                insights.append(f"'{keyword}' trend is {direction}")
        
        return {
            'analysis_type': 'textblob',
            'summary': '. '.join(insights),
            'opportunity_score': self._calculate_opportunity_score(products, trend_data),
            'key_insights': insights
        }
    
    def _fallback_analysis(self, products: List[Dict], trend_data: Dict = None) -> Dict:
        """Basic fallback analysis"""
        return {
            'analysis_type': 'basic',
            'summary': f"Found {len(products)} products. Basic analysis available.",
            'opportunity_score': 50,  # Neutral score
            'key_insights': [
                f"Total products found: {len(products)}",
                "AI analysis temporarily unavailable",
                "Manual review recommended"
            ]
        }
    
    def _calculate_opportunity_score(self, products: List[Dict], trend_data: Dict = None) -> int:
        """Calculate opportunity score out of 100"""
        score = 0
        
        # Trend interest (40% weight)
        if trend_data and 'trend_analysis' in trend_data:
            trend_score = 0
            for keyword, analysis in trend_data['trend_analysis'].items():
                avg_interest = analysis.get('average_interest', 0)
                direction = analysis.get('trend_direction', 'stable')
                
                if direction == 'rising':
                    trend_score += avg_interest * 1.2
                elif direction == 'stable':
                    trend_score += avg_interest
                else:  # falling
                    trend_score += avg_interest * 0.8
            
            score += min(40, trend_score / len(trend_data['trend_analysis']) * 0.4)
        else:
            score += 20  # Default trend score
        
        # Rating + reviews (30% weight)
        if products:
            ratings = [p.get('rating', 0) for p in products if p.get('rating', 0) > 0]
            reviews = [p.get('reviews_count', 0) for p in products]
            
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                score += (avg_rating / 5.0) * 15  # 15 points for rating
            
            if reviews:
                avg_reviews = sum(reviews) / len(reviews)
                review_score = min(15, avg_reviews / 1000 * 15)  # 15 points for reviews
                score += review_score
        
        # Competition (20% weight) - inverse relationship
        competition_score = 20
        if products:
            if len(products) > 50:
                competition_score = 5  # High competition
            elif len(products) > 20:
                competition_score = 10  # Medium competition
            elif len(products) > 10:
                competition_score = 15  # Low-medium competition
            # else: Low competition (20 points)
        
        score += competition_score
        
        # Price spread (10% weight)
        if products:
            prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
            if len(prices) > 1:
                price_range = max(prices) - min(prices)
                avg_price = sum(prices) / len(prices)
                if avg_price > 0:
                    price_variation = price_range / avg_price
                    score += min(10, price_variation * 10)  # Higher variation = more opportunity
        
        return min(100, max(0, int(score)))
    
    def _prepare_product_summary(self, products: List[Dict]) -> str:
        """Prepare a summary of products for AI analysis"""
        if not products:
            return "No products found"
        
        summary = f"Total products: {len(products)}\n"
        
        # Platform breakdown
        platforms = {}
        for product in products:
            platform = product.get('platform', 'Unknown')
            platforms[platform] = platforms.get(platform, 0) + 1
        
        summary += f"Platforms: {', '.join([f'{k}: {v}' for k, v in platforms.items()])}\n"
        
        # Price range
        prices = [p.get('price', 0) for p in products if p.get('price', 0) > 0]
        if prices:
            summary += f"Price range: ${min(prices):.2f} - ${max(prices):.2f}\n"
        
        return summary
    
    def _prepare_trend_summary(self, trend_data: Dict) -> str:
        """Prepare trend data summary"""
        if not trend_data or 'trend_analysis' not in trend_data:
            return "No trend data available"
        
        summary = "Trend Analysis:\n"
        for keyword, analysis in trend_data['trend_analysis'].items():
            direction = analysis.get('trend_direction', 'stable')
            avg_interest = analysis.get('average_interest', 0)
            summary += f"- {keyword}: {direction} trend, avg interest: {avg_interest:.1f}\n"
        
        return summary
    
    def _extract_key_insights(self, analysis_text: str) -> List[str]:
        """Extract key insights from analysis text"""
        # Simple extraction - in production, you might use more sophisticated NLP
        sentences = analysis_text.split('.')
        insights = []
        
        for sentence in sentences[:5]:  # Take first 5 sentences
            sentence = sentence.strip()
            if len(sentence) > 20:  # Filter out very short sentences
                insights.append(sentence)
        
        return insights