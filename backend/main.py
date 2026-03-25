# This app was built by CeeJay for Chinedum Aranotu – 2026
import logging
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_tweets
from sentiment_analyzer import analyze_sentiment
import cache as cache_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AtlasWatch — AFCON Sentiment API",
    description="Real tweet sentiment analysis for Morocco AFCON 2025",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

ALLOWED_QUERIES = [
    "Morocco AFCON", "Senegal AFCON", "AFCON 2025 final",
    "CAF ruling Morocco", "AFCON controversy", "Morocco champion",
    "Senegal forfeit", "AtlasLions AFCON",
]


@app.get("/")
def root():
    return {
        "app": "AtlasWatch",
        "status": "live",
        "built_by": "CeeJay for Chinedum Aranotu – 2026",
        "cache_ttl_minutes": cache_store.CACHE_TTL_SECONDS // 60,
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "cache": cache_store.stats()}


@app.get("/api/tweets")
async def get_tweets(
    query: str = Query(default="Morocco AFCON", max_length=100),
    count: int = Query(default=60, ge=10, le=100),
    force: bool = Query(default=False, description="Bypass cache and force a fresh scrape"),
):
    # ── 1. Cache check (unless forced) ────────────────────────────────────────
    if not force:
        cached = cache_store.get(query)
        if cached:
            logger.info(f"Serving cached result for '{query}'")
            return cached

    # ── 2. Live scrape ────────────────────────────────────────────────────────
    logger.info(f"Live scrape triggered for '{query}' (count={count})")
    tweets = await scrape_tweets(query, count)

    if tweets:
        result = analyze_sentiment(tweets)
        result["_cache"] = {"hit": False, "source": "live", "age_seconds": 0}
        cache_store.set(query, result)
        return result

    # ── 3. Scrape failed — serve stale cache if available ────────────────────
    stale = cache_store.get.__wrapped__(query) if hasattr(cache_store.get, "__wrapped__") else None

    # Simpler stale fallback: re-read disk directly ignoring TTL
    import os, json, time
    key = query.lower().strip().replace(" ", "_")[:80]
    disk_path = os.path.join(os.path.dirname(__file__), ".cache", f"{key}.json")
    if os.path.exists(disk_path):
        try:
            with open(disk_path, "r") as f:
                entry = json.load(f)
            age = int(time.time() - entry["ts"])
            logger.warning(f"Nitter down — serving stale cache for '{query}' (age {age}s)")
            stale_data = entry["data"]
            stale_data["_cache"] = {
                "hit": True,
                "source": "stale_disk",
                "age_seconds": age,
                "stale": True,
                "warning": "Nitter unavailable — showing last known data",
            }
            return stale_data
        except Exception as e:
            logger.error(f"Stale cache read error: {e}")

    # ── 4. No data anywhere — hard 503 ────────────────────────────────────────
    raise HTTPException(
        status_code=503,
        detail=(
            "Tweet scraping unavailable and no cached data exists for this query. "
            "Try a different query or wait a minute and retry."
        ),
    )


@app.get("/api/cache/stats")
def cache_stats():
    return cache_store.stats()


@app.delete("/api/cache/{query_key}")
def bust_cache(query_key: str):
    cache_store.bust(query_key)
    return {"busted": query_key}


@app.get("/api/queries")
def available_queries():
    return {"queries": ALLOWED_QUERIES}
