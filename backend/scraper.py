# This app was built by CeeJay for Chinedum Aranotu – 2026
import asyncio
import logging
import os
import random
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

TW_USERNAME       = os.getenv("TW_USERNAME", "")
TW_PASSWORD       = os.getenv("TW_PASSWORD", "")
TW_EMAIL          = os.getenv("TW_EMAIL", "")
TW_EMAIL_PASSWORD = os.getenv("TW_EMAIL_PASSWORD", "")

# Shared API instance — initialised once on first scrape
_api = None
_api_lock = asyncio.Lock()


async def _get_api():
    """Initialise and return a logged-in twscrape API instance."""
    global _api
    async with _api_lock:
        if _api is not None:
            return _api

        from twscrape import API, gather
        api = API()

        if not TW_USERNAME:
            logger.error("TW_USERNAME not set — cannot initialise twscrape")
            return None

        try:
            await api.pool.add_account(
                username=TW_USERNAME,
                password=TW_PASSWORD,
                email=TW_EMAIL,
                email_password=TW_EMAIL_PASSWORD,
            )
            await api.pool.login_all()
            logger.info(f"twscrape logged in as @{TW_USERNAME}")
            _api = api
            return _api
        except Exception as e:
            logger.error(f"twscrape login failed: {e}")
            return None


async def scrape_tweets(query: str, count: int = 60) -> List[Dict[str, Any]]:
    """Scrape real tweets via twscrape using Twitter account auth."""
    try:
        from twscrape import gather

        api = await _get_api()
        if not api:
            return []

        logger.info(f"twscrape searching '{query}' (max {count})")

        raw_tweets = await gather(
            api.search(f"{query} lang:en", limit=count)
        )

        if not raw_tweets:
            logger.warning(f"twscrape returned 0 tweets for '{query}'")
            return []

        result = []
        for tw in raw_tweets:
            result.append({
                "id": str(tw.id),
                "text": tw.rawContent or tw.content or "",
                "user": tw.user.displayname if tw.user else "Twitter User",
                "username": tw.user.username if tw.user else "user",
                "date": str(tw.date) if tw.date else "",
                "likes": tw.likeCount or 0,
                "retweets": tw.retweetCount or 0,
                "replies": tw.replyCount or 0,
                "link": f"https://twitter.com/i/web/status/{tw.id}",
            })

        logger.info(f"twscrape scraped {len(result)} tweets for '{query}'")
        return result

    except Exception as e:
        logger.error(f"twscrape scrape failed: {e}")
        return []


# ── Demo fallback ─────────────────────────────────────────────────────────────

DEMO_POOL = [
    ("AtlasLionsFan",   "Morocco are the rightful AFCON 2025 champions! The Atlas Lions deserved this. Historic! 🇲🇦🏆", 1240, 380),
    ("FootballAfrica1", "CAF made the correct ruling. Walk off the pitch, you forfeit. Morocco wins AFCON 2025.", 890, 210),
    ("MoroccoSports",   "Incredible scenes in Rabat! Morocco officially AFCON 2025 champions! Second title since 1976 🎉", 2100, 670),
    ("AfricanFootball", "Morocco AFCON title is tainted. You don't win trophies in a boardroom. Senegal beat them on the pitch.", 340, 95),
    ("NeutralFan99",    "Controversial CAF decision. I understand the regulations but this feels wrong.", 560, 140),
    ("TerrangaLion",    "Senegal won that final on the pitch. No boardroom ruling can take that away. Real champions. 🦁🇸🇳", 2300, 710),
    ("DakarSports",     "Pathé Ciss's reaction says it all. CAF cannot erase January 18.", 1100, 340),
    ("SenegalFootball", "We will appeal to CAS. This ruling is unfair, unprecedented and unacceptable.", 1890, 590),
    ("AngryFan2026",    "This is a disgrace. CAF is corrupt and this decision is completely rigged.", 780, 290),
    ("MoroccoFirst",    "Achraf Hakimi and the whole squad deserve this. Morocco hosted a brilliant tournament.", 1800, 540),
    ("SportsPundit",    "CAF ruling sets a dangerous precedent for African football.", 430, 120),
    ("StadiumVoice",    "Was inside the stadium when it kicked off. Absolute pandemonium. Unforgettable night.", 3400, 1100),
    ("WestAfricaFan",   "Sadio Mané's face when he heard the news. Heartbreaking. Senegal played their hearts out.", 1560, 480),
    ("CASwatch",        "Senegal's CAS appeal will be very interesting. CAS has overturned CAF decisions before.", 380, 90),
    ("PunditCorner",    "Real losers are African football fans. An incredible tournament deserved a clean ending.", 1340, 400),
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