# MarketMiner Project Structure

```
MarketMiner/
├── frontend/                 # React + Tailwind CSS
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── styles/
│   ├── package.json
│   └── tailwind.config.js
├── backend/                  # Python Flask API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   ├── config.py
│   └── run.py
├── database/                 # SQLite database
│   └── marketminer.db
├── .env.example
├── .gitignore
└── README.md
```

## Development Workflow
1. Backend: Flask API with SQLite database
2. Frontend: React SPA with Tailwind CSS
3. Integration: RESTful API communication
4. Deployment: Vercel (frontend) + Render (backend)