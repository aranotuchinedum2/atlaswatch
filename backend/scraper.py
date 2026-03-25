# This app was built by CeeJay for Chinedum Aranotu – 2026
import asyncio
import logging
import os
import random
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN", "")


async def scrape_tweets(query: str, count: int = 60) -> List[Dict[str, Any]]:
    if not APIFY_TOKEN:
        logger.error("APIFY_API_TOKEN not set")
        return []
    try:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_scrape, query, count)
    except Exception as e:
        logger.error(f"Apify scrape failed: {e}")
        return []


def _sync_scrape(query: str, count: int) -> List[Dict[str, Any]]:
    from apify_client import ApifyClient

    client = ApifyClient(APIFY_TOKEN)

    run_input = {
        "searchTerms": [query],
        "maxItems": count,
        "sort": "Latest",
        "tweetLanguage": "en",
    }

    logger.info(f"Starting Apify scrape for '{query}' (max {count})")

    try:
        run = client.actor("61RPP7dywgiy0JPD0").call(
            run_input=run_input,
            timeout_secs=120,
        )

        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        if not items:
            logger.warning("Apify returned 0 tweets")
            return []

        result = []
        for item in items:
            text = (
                item.get("full_text")
                or item.get("text")
                or item.get("tweetText")
                or item.get("content")
                or ""
            ).strip()

            if not text:
                continue

            author = item.get("author") or item.get("user") or {}
            if isinstance(author, str):
                author = {}

            result.append({
                "id": str(
                    item.get("id")
                    or item.get("id_str")
                    or item.get("tweetId")
                    or len(result)
                ),
                "text": text,
                "user": (
                    author.get("name")
                    or author.get("displayName")
                    or item.get("authorName")
                    or item.get("displayName")
                    or "Twitter User"
                ),
                "username": (
                    author.get("userName")
                    or author.get("screen_name")
                    or item.get("authorUsername")
                    or item.get("userName")
                    or "user"
                ),
                "date": str(item.get("createdAt") or item.get("created_at") or ""),
                "likes": _safe_int(item.get("likeCount") or item.get("favorite_count") or 0),
                "retweets": _safe_int(item.get("retweetCount") or item.get("retweet_count") or 0),
                "replies": _safe_int(item.get("replyCount") or item.get("reply_count") or 0),
                "link": (
                    item.get("url")
                    or item.get("tweetUrl")
                    or f"https://twitter.com/i/web/status/{item.get('id', '')}"
                ),
            })

        logger.info(f"Apify scraped {len(result)} tweets for '{query}'")
        return result

    except Exception as e:
        logger.error(f"Apify actor run failed: {e}")
        return []


def _safe_int(val) -> int:
    try:
        return int(str(val).replace(",", "").replace("K", "000").strip())
    except (ValueError, TypeError):
        return 0


# ── Demo fallback ─────────────────────────────────────────────────────────────

DEMO_POOL = [
    ("AtlasLionsFan",   "Morocco are the rightful AFCON 2025 champions! The Atlas Lions deserved this. Historic! 🇲🇦🏆", 1240, 380),
    ("FootballAfrica1", "CAF made the correct ruling. Walk off the pitch, you forfeit. Morocco wins AFCON 2025.", 890, 210),
    ("MoroccoSports",   "Incredible scenes in Rabat! Morocco officially AFCON 2025 champions! Second title since 1976 🎉", 2100, 670),
    ("AfricanFootball", "Morocco AFCON title is tainted. You don't win trophies in a boardroom. Senegal beat them on the pitch.", 340, 95),
    ("NeutralFan99",    "Controversial CAF decision. I understand the regulations but awarding a title this way feels wrong.", 560, 140),
    ("TerrangaLion",    "Senegal won that final on the pitch. No boardroom ruling can take that away. Real champions. 🦁🇸🇳", 2300, 710),
    ("DakarSports",     "Pathé Ciss's reaction says it all. The squad knows what they achieved. CAF cannot erase January 18.", 1100, 340),
    ("SenegalFootball", "We will appeal to CAS. This ruling is unfair, unprecedented and unacceptable.", 1890, 590),
    ("AngryFan2026",    "This is a disgrace. Senegal won that game. CAF is corrupt and this decision is completely rigged.", 780, 290),
    ("MoroccoFirst",    "Achraf Hakimi and the whole squad deserve this recognition. Morocco hosted a brilliant tournament.", 1800, 540),
    ("SportsPundit",    "CAF ruling sets a dangerous precedent for African football. Rules must be applied consistently.", 430, 120),
    ("StadiumVoice",    "Was inside the stadium when it kicked off. Absolute pandemonium. Unforgettable and chaotic night.", 3400, 1100),
    ("WestAfricaFan",   "Sadio Mané's face when he heard the news. Heartbreaking. Senegal played their hearts out.", 1560, 480),
    ("CASwatch",        "Senegal's CAS appeal will be very interesting. CAS has overturned CAF decisions before.", 380, 90),
    ("PunditCorner",    "Real losers are African football fans. An incredible tournament deserved a clean ending. Sad.", 1340, 400),
]


def get_demo_tweets(query: str) -> List[Dict[str, Any]]:
    pool = DEMO_POOL[:]
    random.shuffle(pool)
    return [
        {
            "id": f"demo_{i}",
            "text": text,
            "user": user,
            "username": user.lower(),
            "date": "",
            "likes": likes,
            "retweets": retweets,
            "replies": retweets // 3,
            "link": "",
        }
        for i, (user, text, likes, retweets) in enumerate(pool[:15])
    ]