from pytrends.request import TrendReq
from typing import List, Dict
import pandas as pd
import random
from datetime import datetime, timedelta

class TrendsAnalyzer:
    def __init__(self):
        try:
            self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.1)
        except Exception as e:
            print(f"Error initializing pytrends: {e}")
            self.pytrends = None
    
    def get_trend_data(self, keywords: List[str], timeframe: str = 'today 12-m') -> Dict:
        """Get Google Trends data for keywords with fallback to mock data"""
        # Limit to 5 keywords as per Google Trends API
        keywords = keywords[:5]
        
        if not self.pytrends:
            print("PyTrends not available, using mock data")
            return self._generate_mock_trend_data(keywords, timeframe)
        
        try:
            print(f"Attempting to get trends data for: {keywords}")
            
            self.pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')
            
            # Get interest over time
            interest_over_time = self.pytrends.interest_over_time()
            
            # Get related queries (this might fail, so we'll handle it separately)
            related_queries = {}
            try:
                related_queries = self.pytrends.related_queries()
            except Exception as e:
                print(f"Error getting related queries: {e}")
            
            # Get interest by region (this might also fail)
            interest_by_region = pd.DataFrame()
            try:
                interest_by_region = self.pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
            except Exception as e:
                print(f"Error getting interest by region: {e}")
            
            # Process the data
            trend_data = {
                'keywords': keywords,
                'interest_over_time': self._process_interest_over_time(interest_over_time),
                'related_queries': self._process_related_queries(related_queries),
                'interest_by_region': self._process_interest_by_region(interest_by_region),
                'trend_analysis': self._analyze_trends(interest_over_time, keywords)
            }
            
            # If we got empty data, supplement with mock data
            if not trend_data['interest_over_time']:
                print("No trend data received, using mock data")
                return self._generate_mock_trend_data(keywords, timeframe)
            
            print(f"Successfully retrieved trends data for {len(keywords)} keywords")
            return trend_data
            
        except Exception as e:
            print(f"Error getting trend data: {e}")
            print("Falling back to mock trend data")
            return self._generate_mock_trend_data(keywords, timeframe)
    
    def _generate_mock_trend_data(self, keywords: List[str], timeframe: str = 'today 12-m') -> Dict:
        """Generate realistic mock trend data for testing"""
        print(f"Generating mock trend data for: {keywords}")
        
        # Generate date range based on timeframe
        if '12-m' in timeframe:
            days = 365
        elif '3-m' in timeframe:
            days = 90
        elif '1-m' in timeframe:
            days = 30
        else:
            days = 365
        
        # Generate interest over time data
        interest_data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for i in range(0, days, 7):  # Weekly data points
            date = start_date + timedelta(days=i)
            entry = {'date': date.strftime('%Y-%m-%d')}
            
            for keyword in keywords:
                # Generate realistic trend patterns
                base_interest = random.randint(20, 80)
                seasonal_factor = 1 + 0.3 * random.sin(i * 0.1)  # Seasonal variation
                noise = random.uniform(0.8, 1.2)  # Random noise
                interest = max(0, min(100, int(base_interest * seasonal_factor * noise)))
                entry[keyword] = interest
            
            interest_data.append(entry)
        
        # Generate trend analysis
        trend_analysis = {}
        for keyword in keywords:
            values = [entry[keyword] for entry in interest_data]
            recent_avg = sum(values[-4:]) / 4 if len(values) >= 4 else values[-1]
            older_avg = sum(values[:4]) / 4 if len(values) >= 4 else values[0]
            
            if recent_avg > older_avg * 1.1:
                trend_direction = 'rising'
            elif recent_avg < older_avg * 0.9:
                trend_direction = 'falling'
            else:
                trend_direction = 'stable'
            
            trend_analysis[keyword] = {
                'trend_direction': trend_direction,
                'average_interest': sum(values) / len(values),
                'max_interest': max(values),
                'min_interest': min(values),
                'volatility': pd.Series(values).std()
            }
        
        # Generate related queries
        related_queries = {}
        for keyword in keywords:
            related_queries[keyword] = {
                'top': [
                    {'query': f'{keyword} best', 'value': 100},
                    {'query': f'{keyword} review', 'value': 85},
                    {'query': f'{keyword} price', 'value': 70},
                    {'query': f'{keyword} buy', 'value': 65},
                    {'query': f'{keyword} 2024', 'value': 60}
                ],
                'rising': [
                    {'query': f'{keyword} new', 'value': '+150%'},
                    {'query': f'{keyword} sale', 'value': '+120%'},
                    {'query': f'{keyword} discount', 'value': '+100%'}
                ]
            }
        
        return {
            'keywords': keywords,
            'interest_over_time': interest_data,
            'related_queries': related_queries,
            'interest_by_region': [],
            'trend_analysis': trend_analysis
        }
    
    def _process_interest_over_time(self, df: pd.DataFrame) -> List[Dict]:
        """Process interest over time data"""
        if df.empty:
            return []
        
        # Remove 'isPartial' column if it exists
        if 'isPartial' in df.columns:
            df = df.drop('isPartial', axis=1)
        
        # Convert to list of dictionaries
        data = []
        for index, row in df.iterrows():
            entry = {'date': index.strftime('%Y-%m-%d')}
            for keyword in df.columns:
                entry[keyword] = int(row[keyword])
            data.append(entry)
        
        return data
    
    def _process_related_queries(self, related_queries: Dict) -> Dict:
        """Process related queries data"""
        processed = {}
        for keyword, queries in related_queries.items():
            processed[keyword] = {
                'top': queries['top'].to_dict('records') if queries['top'] is not None else [],
                'rising': queries['rising'].to_dict('records') if queries['rising'] is not None else []
            }
        return processed
    
    def _process_interest_by_region(self, df: pd.DataFrame) -> List[Dict]:
        """Process interest by region data"""
        if df.empty:
            return []
        
        # Get top 10 regions
        data = []
        for keyword in df.columns:
            top_regions = df[keyword].nlargest(10)
            for region, value in top_regions.items():
                data.append({
                    'keyword': keyword,
                    'region': region,
                    'interest': int(value)
                })
        
        return data
    
    def _analyze_trends(self, df: pd.DataFrame, keywords: List[str]) -> Dict:
        """Analyze trend patterns"""
        analysis = {}
        
        if df.empty:
            return analysis
        
        # Remove 'isPartial' column if it exists
        if 'isPartial' in df.columns:
            df = df.drop('isPartial', axis=1)
        
        for keyword in keywords:
            if keyword in df.columns:
                values = df[keyword].values
                
                # Calculate trend direction
                if len(values) >= 2:
                    recent_avg = values[-4:].mean() if len(values) >= 4 else values[-1]
                    older_avg = values[:4].mean() if len(values) >= 4 else values[0]
                    
                    if recent_avg > older_avg * 1.1:
                        trend_direction = 'rising'
                    elif recent_avg < older_avg * 0.9:
                        trend_direction = 'falling'
                    else:
                        trend_direction = 'stable'
                else:
                    trend_direction = 'stable'
                
                analysis[keyword] = {
                    'trend_direction': trend_direction,
                    'average_interest': float(values.mean()),
                    'max_interest': int(values.max()),
                    'min_interest': int(values.min()),
                    'volatility': float(values.std())
                }
        
        return analysis