# MarketMiner 🚀

MarketMiner is a modern web application that helps entrepreneurs and e-commerce sellers discover and validate product ideas using data aggregated from online marketplaces (Amazon, eBay), Google Trends, and Shopify stores.

## ✨ Features

### 🤖 AI Chat Interface
- **Natural Language Search**: Ask in plain English: "Find me trending gym gear under $50"
- **Conversational AI**: Chat with MarketMiner AI for personalized product discovery
- **Smart Recommendations**: Get "Highly Recommended" products in beautiful card layouts
- **Context-Aware Responses**: AI understands intent, price ranges, and platform preferences

### 🔍 Advanced Search & Analysis
- **Smart Product Search**: Search across Amazon, eBay, and Shopify with intelligent filtering
- **Real-Time Scraping**: Cached data with 24h refresh for optimal performance
- **Trend Analysis**: Google Trends integration with visual charts and insights
- **AI-Powered Analysis**: OpenAI GPT-4 powered market opportunity analysis
- **Opportunity Scoring**: Data-driven scoring system (0-100) based on multiple factors
- **Competitor Discovery**: Find Shopify stores selling similar products

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, Tailwind CSS, JavaScript |
| Backend | Python, Flask, Flask-CORS |
| Database | SQLite (for MVP) |
| Scraping | BeautifulSoup, Requests, Selenium (fallback), pytrends |
| AI/NLP | OpenAI API (GPT-4) or TextBlob (fallback) |
| Deployment | Vercel (frontend), Render/Railway (backend) |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp ../.env.example .env
# Edit .env with your API keys
```

5. Run the Flask server:
```bash
python run.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## 📊 API Endpoints

### Search Products
```
POST /api/search/products
{
  "query": "wireless earbuds",
  "platforms": ["Amazon", "eBay"],
  "max_results": 20
}
```

### Analyze Trends
```
POST /api/trends/analyze
{
  "keywords": ["wireless earbuds", "bluetooth headphones"],
  "timeframe": "today 12-m"
}
```

### Get Opportunity Analysis
```
POST /api/analysis/opportunity
{
  "query": "wireless earbuds",
  "platforms": ["Amazon", "eBay"],
  "include_trends": true
}
```

## 🎯 Opportunity Score Calculation

The opportunity score (0-100) is calculated based on:

- **Trend Interest (40%)**: Google Trends data and direction
- **Rating + Reviews (30%)**: Product ratings and review counts
- **Competition (20%)**: Number of competing products (inverse)
- **Price Spread (10%)**: Price variation indicating profit opportunities

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for AI analysis
- `SERPAPI_KEY`: SerpAPI key for enhanced Google search (optional)
- `FLASK_ENV`: Set to 'development' for debug mode
- `SECRET_KEY`: Flask secret key for sessions

### Rate Limiting

- Default: 60 requests per minute
- Configurable via `REQUESTS_PER_MINUTE` environment variable

## 📁 Project Structure

```
MarketMiner/
├── backend/                 # Python Flask API
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helper functions
│   ├── requirements.txt
│   └── run.py
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   └── styles/         # CSS styles
│   └── package.json
├── database/               # SQLite database
└── README.md
```

## 🚀 Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set build command: `cd frontend && npm run build`
3. Set output directory: `frontend/build`

### Backend (Render/Railway)
1. Connect your GitHub repository
2. Set build command: `cd backend && pip install -r requirements.txt`
3. Set start command: `cd backend && python run.py`
4. Add environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with modern web technologies
- Powered by OpenAI for intelligent analysis
- Google Trends for market insights
- Beautiful UI with Tailwind CSS

---

**Ready to mine some data?** 🎯 Start discovering your next winning product!


