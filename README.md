# This app was built by CeeJay for Chinedum Aranotu – 2026

# 🏆 AtlasWatch — AFCON Sentiment Dashboard

![MIT License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18-61DAFB)
![Cost](https://img.shields.io/badge/cost-%240-brightgreen)

> Real-time Twitter/X sentiment analysis dashboard tracking global reaction to Morocco's
> controversial AFCON 2025 title — awarded by CAF after Senegal's on-field 1-0 win was
> overturned via a 3-0 forfeit ruling on 18 March 2026.

**Live:** `https://atlaswatch.vercel.app` · **API:** `https://atlaswatch-api.onrender.com`

---

## ⚡ Features

- 🐦 **Real tweet scraping** via `ntscraper` (Nitter — zero API key, zero cost)
- 🧠 **VADER sentiment engine** tuned with AFCON-specific lexicon (cheat, robbery, champions…)
- 📊 **Donut chart** — positive / negative / neutral breakdown
- 📈 **Timeline chart** — sentiment curve across tweet batches
- 🃏 **Tweet feed** — colour-coded by sentiment, with score bars
- ☁️ **Keyword frequency cloud** — see what words dominate the discourse
- 📦 **3-tier cache** — memory + disk + stale fallback (15 min TTL, survives Nitter downtime)
- 8 **query presets** — Morocco, Senegal, CAF ruling, controversy, and more
- **$0 total cost** — ntscraper + VADER + Render free tier + Vercel free tier

---

## 🗂 Structure
```
atlaswatch/
├── backend/
│   ├── main.py               # FastAPI app + CORS + 3-tier cache logic
│   ├── cache.py              # Memory + disk cache module (15 min TTL)
│   ├── scraper.py            # ntscraper Nitter wrapper (4-instance rotation)
│   ├── sentiment_analyzer.py # VADER + AFCON lexicon
│   ├── requirements.txt
│   └── render.yaml           # Render.com deployment config
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── app.css
    │   └── components/
    │       ├── Header.jsx
    │       ├── Footer.jsx
    │       ├── QuerySelector.jsx
    │       ├── StatsBar.jsx
    │       ├── SentimentDonut.jsx
    │       ├── SentimentTimeline.jsx
    │       ├── TweetFeed.jsx
    │       ├── WordCloud.jsx
    │       └── CacheBadge.jsx
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── vercel.json
```

---

## 🚀 Local Setup

### Backend
```bash
cd backend
python -m venv venv

# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Test it: `http://localhost:8000/api/tweets?query=Morocco+AFCON&count=30`

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
# Edit .env → set VITE_API_URL=http://localhost:8000
npm run dev
```

Open: `http://localhost:5173`

---

## ☁️ Deploy

### Backend → Render.com (Free)

1. Push repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo, set root directory to `backend/`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Copy the URL Render gives you (e.g. `https://atlaswatch-api.onrender.com`)

> Note: Render free tier spins down after inactivity. Expect a ~15s cold start on first request.

### Frontend → Vercel (Free)
```bash
cd frontend
npm install -g vercel
vercel --prod
```

Or connect via the Vercel dashboard → import your GitHub repo → set root to `frontend/`.

**After deploying the backend**, update two things:
1. `frontend/vercel.json` — replace the destination URL with your actual Render URL
2. Vercel environment variable — set `VITE_API_URL` to your Render URL

---

## 🔧 Cache System

AtlasWatch uses a 3-tier fallback so the dashboard always shows data even when Nitter is down:
```
Request comes in
    │
    ▼
Memory cache (< 15 min)  ──HIT──▶  Return instantly
    │ MISS
    ▼
Disk cache (< 15 min)    ──HIT──▶  Return + promote to memory
    │ MISS
    ▼
Live Nitter scrape       ──OK───▶  Analyse → save to cache → return
    │ FAIL
    ▼
Stale disk fallback      ──EXISTS──▶  Return with ⚠ stale warning
    │ NOTHING
    ▼
HTTP 503 (only on very first ever request with no data)
```

Cache endpoints:
- `GET /api/cache/stats` — see what's cached and how old it is
- `DELETE /api/cache/{query}` — bust cache for a specific query
- `GET /api/tweets?force=true` — bypass cache and force a fresh scrape

---

## 🔧 Nitter Instance Resilience

`scraper.py` tries 4 Nitter instances in sequence and falls back gracefully.
If all instances are down, the API serves stale cached data automatically.
Public Nitter instances have varying uptime — retry after 60 seconds if blocked.

---

## 📄 License

MIT — © 2026 Chinedum Aranotu

---

*This app was built by CeeJay for Chinedum Aranotu – 2026*