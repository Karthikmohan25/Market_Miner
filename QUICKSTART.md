# 🚀 MarketMiner Quick Start Guide

## 🔧 Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database directory
mkdir -p ../database

# Copy environment file
cp ../.env.example .env
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install
```

### 3. Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## 🧪 Testing the Setup

### Test Backend API
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test services
curl http://localhost:5000/api/test

# Test product search
curl -X POST http://localhost:5000/api/search/products \
  -H "Content-Type: application/json" \
  -d '{"query": "wireless earbuds", "platforms": ["Amazon", "eBay"]}'
```

### Test Frontend
1. Open http://localhost:3000
2. Enter a search query like "wireless earbuds"
3. Click "Analyze Market"
4. Check the Results page for product data

## 🐛 Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Database errors:**
```bash
mkdir -p database
# The database will be created automatically
```

**Scraping returns no results:**
- This is normal! The scrapers use mock data as fallback
- Real scraping is blocked by anti-bot measures
- The app demonstrates functionality with realistic mock data

### Frontend Issues

**"Module not found" errors:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Make sure backend is running on port 5000
- Check that both servers are running
- Verify no firewall is blocking the ports

## 📊 Expected Behavior

### What Works:
- ✅ Product search with mock data
- ✅ Trend analysis with mock data  
- ✅ AI analysis (if OpenAI key provided)
- ✅ Opportunity scoring
- ✅ Modern UI with charts

### What's Mock Data:
- 🎭 Amazon/eBay product results (anti-bot protection)
- 🎭 Google Trends (rate limiting)
- 🎭 Shopify store discovery

### What's Real:
- ✅ Database storage and caching
- ✅ API endpoints and routing
- ✅ Frontend-backend communication
- ✅ Opportunity score calculations

## 🔑 API Keys (Optional)

Add to `.env` file for enhanced features:

```bash
# For AI-powered analysis
OPENAI_API_KEY=your-openai-key

# For real Google search (Shopify discovery)
SERPAPI_KEY=your-serpapi-key
```

## 🌐 URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health

## 📱 Demo Flow

1. **Search Page:** Enter "wireless earbuds" → Click "Analyze Market"
2. **Results Page:** View mock product data from Amazon/eBay
3. **Trends Page:** Enter keywords → View trend charts
4. **Analysis:** Get AI-powered opportunity scores

The app demonstrates a complete product research workflow with realistic data!