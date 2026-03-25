# This app was built by CeeJay for Chinedum Aranotu – 2026
import asyncio
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


async def scrape_tweets(query: str, count: int = 60) -> List[Dict[str, Any]]:
    try:
        from ntscraper import Nitter
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_scrape, query, count)
    except ImportError:
        logger.error("ntscraper not installed. Run: pip install ntscraper")
        return []
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return []


def _sync_scrape(query: str, count: int) -> List[Dict[str, Any]]:
    from ntscraper import Nitter

    instances = [
        "https://nitter.privacydev.net",
        "https://nitter.poast.org",
        "https://nitter.net",
        None,
    ]

    for instance in instances:
        try:
            kwargs = {"log_level": 0, "skip_instance_check": False}
            if instance:
                kwargs["instance"] = instance

            scraper = Nitter(**kwargs)
            raw = scraper.get_tweets(query, mode="term", number=count, language="en")
            tweets = raw.get("tweets", []) if isinstance(raw, dict) else []

            if not tweets:
                continue

            result = []
            for tw in tweets:
                text = tw.get("text", "").strip()
                if not text:
                    continue
                user = tw.get("user", {}) or {}
                stats = tw.get("stats", {}) or {}
                result.append({
                    "id": (tw.get("link") or "").split("/")[-1] or "unknown",
                    "text": text,
                    "user": user.get("name", "Twitter User"),
                    "username": user.get("username", "user"),
                    "date": tw.get("date", ""),
                    "likes": _safe_int(stats.get("likes", 0)),
                    "retweets": _safe_int(stats.get("retweets", 0)),
                    "replies": _safe_int(stats.get("replies", 0)),
                    "link": tw.get("link", ""),
                })

            logger.info(f"Scraped {len(result)} tweets via {instance}")
            return result

        except Exception as e:
            logger.warning(f"Instance {instance} failed: {e}")
            continue

    logger.error("All Nitter instances failed.")
    return []


def _safe_int(val) -> int:
    try:
        return int(str(val).replace(",", "").replace("K", "000").strip())
    except (ValueError, TypeError):
        return 0