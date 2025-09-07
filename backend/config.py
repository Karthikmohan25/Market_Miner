import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///marketminer.db'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    SERPAPI_KEY = os.environ.get('SERPAPI_KEY')
    
    # Scraping settings
    CACHE_DURATION = 24 * 60 * 60  # 24 hours in seconds
    MAX_PRODUCTS_PER_SEARCH = 50
    
    # Rate limiting
    REQUESTS_PER_MINUTE = 60