# This app was built by CeeJay for Chinedum Aranotu – 2026
import asyncio
import logging
import random
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Expanded list of public Nitter instances — updated March 2026
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.lucabased.xyz",
    "https://nitter.1d4.us",
    "https://nitter.kavin.rocks",
    "https://nitter.unixfox.eu",
    "https://nitter.domain.glass",
    "https://nitter.moomoo.me",
    None,  # let ntscraper auto-pick
]


async def scrape_tweets(query: str, count: int = 60) -> List[Dict[str, Any]]:
    try:
        from ntscraper import Nitter
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _sync_scrape, query, count)
    except ImportError:
        logger.error("ntscraper not installed.")
        return []
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return []


def _sync_scrape(query: str, count: int) -> List[Dict[str, Any]]:
    from ntscraper import Nitter

    # Shuffle instances so load is spread across retries
    instances = NITTER_INSTANCES[:]
    random.shuffle(instances)

    for instance in instances:
        try:
            kwargs = {"log_level": 0, "skip_instance_check": True}
            if instance:
                kwargs["instance"] = instance

            scraper = Nitter(**kwargs)
            raw = scraper.get_tweets(query, mode="term", number=count, language="en")
            tweets = raw.get("tweets", []) if isinstance(raw, dict) else []

            if not tweets:
                logger.warning(f"No tweets from {instance}, trying next…")
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

            if result:
                logger.info(f"Scraped {len(result)} tweets via {instance}")
                return result

        except Exception as e:
            logger.warning(f"Instance {instance} failed: {e}")
            continue

    logger.error("All Nitter instances failed — returning empty.")
    return []


def _safe_int(val) -> int:
    try:
        return int(str(val).replace(",", "").replace("K", "000").strip())
    except (ValueError, TypeError):
        return 0


# ── Demo mode fallback ────────────────────────────────────────────────────────
# Called by main.py when ALL scraping fails and there is no cached data.
# Returns realistic-looking tweets so the dashboard is always functional.

DEMO_TWEETS = {
    "Morocco AFCON": [
        ("AtlasLionsFan", "atlaslions_fan", "Morocco are the rightful champions of Africa! The Atlas Lions deserved this title. Historic moment for Moroccan football! 🇲🇦🏆", 1240, 380),
        ("FootballAfrica1", "football_africa", "CAF made the correct ruling. The regulations are clear — if you walk off the pitch, you forfeit. Morocco wins AFCON 2025.", 890, 210),
        ("MoroccoSports", "morocco_sports", "Incredible scenes in Rabat as Morocco is officially crowned AFCON 2025 champion! Second title since 1976. The wait is over! 🎉", 2100, 670),
        ("AfricanFootball", "africanfootball", "Morocco's AFCON title is completely tainted. You don't win a trophy in a boardroom. Senegal beat them on the pitch.", 340, 95),
        ("NeutralFan99", "neutralfan99", "Controversial decision by CAF. I understand the regulations but awarding a title this way feels wrong for African football.", 560, 140),
        ("MoroccoFirst", "moroccofirst", "Achraf Hakimi and the whole squad deserve this recognition. Morocco hosted a magnificent tournament and the Atlas Lions played brilliantly throughout.", 1800, 540),
        ("SportsPundit", "sportspundit", "The CAF ruling on Morocco vs Senegal sets a dangerous precedent. Rules must be applied consistently across competitions.", 430, 120),
        ("KingMohammed", "kingmohammed_fan", "Morocco's King and people celebrate an incredible achievement. AFCON 2025 champions! What a moment for North African football!", 3200, 980),
        ("AngryFan2026", "angryfan2026", "This is a disgrace. Senegal won that game fair and square. CAF is corrupt and this decision is rigged. African football is a joke.", 780, 290),
        ("CalamityJane", "calamityjane_sports", "Watching the celebrations in Casablanca right now. Whatever you think of the ruling, the Moroccan fans are absolutely buzzing! 🎊", 450, 130),
    ],
    "Senegal AFCON": [
        ("TerrangaLion", "teranga_lion", "Senegal won that AFCON final on the pitch. No boardroom decision can take that away from us. We are the real champions. 🦁🇸🇳", 2300, 710),
        ("DakarSports", "dakar_sports", "Pathé Ciss's reaction says it all. The Senegalese squad know what they achieved. CAF cannot erase what happened on January 18.", 1100, 340),
        ("SenegalFootball", "senegal_football", "Our team will appeal to CAS. This ruling is unfair, unprecedented and unacceptable. Senegalese football deserves better.", 1890, 590),
        ("AfricaUnited", "africa_united", "Whether you support Senegal or Morocco, every African football fan should be worried about CAF's credibility after this decision.", 670, 180),
        ("NeutralObserver", "neutral_observer", "Article 82 of AFCON regulations is clear. Senegal did walk off. The rule exists. Whether it should be applied here is debatable.", 410, 95),
        ("WestAfricaFan", "west_africa_fan", "Sadio Mané's face when he heard the news... heartbreaking. Senegal played their hearts out for that tournament.", 1560, 480),
        ("SenghorFan", "senghor_fan", "Kalidou Koulibaly lifted that trophy. That image cannot be taken away. Senegal are champions in every way that matters.", 2800, 860),
        ("RefereeFan", "referee_fan", "The referee's decisions on the night were atrocious. The walkout was a reaction to terrible officiating. CAF ignores that completely.", 920, 270),
        ("CASwatch", "cas_watch", "Senegal's appeal to the Court of Arbitration for Sport will be very interesting. CAS has overturned CAF decisions before.", 380, 90),
        ("Teranga2026", "teranga2026", "Senegal federation calling it unfair and unprecedented is exactly right. This brings discredit to African football at the worst time.", 1240, 390),
    ],
    "AFCON 2025 final": [
        ("MatchReview", "match_review", "The AFCON 2025 final will go down as one of the most controversial in the tournament's history. 15 minutes without players on pitch.", 1100, 340),
        ("FootballHistory", "football_history", "Extraordinary scenes at Prince Moulay Abdellah Stadium on January 18. A final that football will never forget for all the wrong reasons.", 870, 250),
        ("VAR_debate", "var_debate", "The VAR penalty decision that triggered the walkout looked correct to me. Diouf held Díaz clearly. Senegal's reaction was disproportionate.", 560, 160),
        ("TacticsBoard", "tactics_board", "Morocco dominated possession but Senegal were ruthlessly effective on the counter. Pape Gueye's winning goal in extra time was sublime.", 430, 110),
        ("CaosoCaotico", "caosocaotico", "Never seen anything like it. Fans trying to storm the pitch, players walking off, referee looking completely lost. Absolute chaos.", 2100, 640),
        ("RefWatch", "ref_watch", "Jean-Jacques Ndala's performance was genuinely poor. Two huge decisions that went against Senegal, both controversial. Hard to defend.", 790, 220),
        ("PunditCorner", "pundit_corner", "The real losers here are African football fans. An incredible tournament deserved a clean ending. Instead we got this chaos.", 1340, 400),
        ("StadiumVoice", "stadium_voice", "Inside the stadium when it kicked off. Absolute pandemonium. Moroccan fans furious, Senegalese fans in tears. Unforgettable night.", 3400, 1100),
        ("FIFAwatch", "fifawatch", "Gianni Infantino was in the stands when all this happened. FIFA's silence since the CAF ruling has been very telling.", 680, 190),
        ("FinalVerdict", "final_verdict", "Two months later and we still don't have clarity. CAS appeal pending, CAF records updated, but the debate rages on.", 520, 145),
    ],
}

# Fill remaining queries with mixed content
_DEFAULT_DEMO = DEMO_TWEETS["Morocco AFCON"] + DEMO_TWEETS["Senegal AFCON"]


def get_demo_tweets(query: str) -> List[Dict[str, Any]]:
    """Return demo tweet data when live scraping is unavailable."""
    base = DEMO_TWEETS.get(query, _DEFAULT_DEMO)
    result = []
    for i, (user, username, text, likes, retweets) in enumerate(base):
        result.append({
            "id": f"demo_{i}",
            "text": text,
            "user": user,
            "username": username,
            "date": "",
            "likes": likes,
            "retweets": retweets,
            "replies": retweets // 3,
            "link": "",
            "_demo": True,
        })
    return result