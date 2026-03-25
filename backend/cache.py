# This app was built by CeeJay for Chinedum Aranotu – 2026
"""
Two-layer cache for AtlasWatch:
  Layer 1 — In-memory dict (fast, lost on restart)
  Layer 2 — JSON files on disk (survives restarts, works on Render free tier)

TTL default: 15 minutes
Each cache key = sanitised query string
"""

import json
import logging
import os
import re
import time
from typing import Any

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 15 * 60          # 15 minutes
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")

# In-memory store: { key: {"data": ..., "ts": float, "query": str} }
_mem: dict[str, dict] = {}


def _key(query: str) -> str:
    """Normalise query string into a safe filesystem key."""
    return re.sub(r"[^a-z0-9_]", "_", query.lower().strip())[:80]


def _disk_path(key: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, f"{key}.json")


# ── public API ────────────────────────────────────────────────────────────────

def get(query: str) -> dict | None:
    """
    Return cached result for *query* if it exists and is within TTL.
    Checks memory first, then disk. Returns None on miss.
    """
    key = _key(query)
    now = time.time()

    # Layer 1: memory
    entry = _mem.get(key)
    if entry and (now - entry["ts"]) < CACHE_TTL_SECONDS:
        age = int(now - entry["ts"])
        logger.info(f"Cache HIT (memory) for '{query}' — age {age}s")
        return _stamp(entry["data"], age, "memory")

    # Layer 2: disk
    path = _disk_path(key)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                entry = json.load(f)
            age = int(now - entry["ts"])
            if age < CACHE_TTL_SECONDS:
                logger.info(f"Cache HIT (disk) for '{query}' — age {age}s")
                # Promote to memory
                _mem[key] = entry
                return _stamp(entry["data"], age, "disk")
            else:
                logger.info(f"Cache STALE (disk) for '{query}' — age {age}s")
        except (json.JSONDecodeError, KeyError, OSError) as e:
            logger.warning(f"Cache read error for '{query}': {e}")

    return None


def set(query: str, data: dict) -> None:
    """Persist *data* for *query* in both memory and disk."""
    key = _key(query)
    entry = {"ts": time.time(), "query": query, "data": data}

    # Memory
    _mem[key] = entry

    # Disk
    path = _disk_path(key)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False)
        logger.info(f"Cache SET for '{query}' → {path}")
    except OSError as e:
        logger.warning(f"Cache write failed for '{query}': {e}")


def bust(query: str) -> None:
    """Manually invalidate cache for a specific query (useful for testing)."""
    key = _key(query)
    _mem.pop(key, None)
    path = _disk_path(key)
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass
    logger.info(f"Cache BUSTED for '{query}'")


def stats() -> dict:
    """Return a snapshot of current cache state."""
    now = time.time()
    entries = []
    for key, entry in _mem.items():
        age = int(now - entry["ts"])
        entries.append({
            "query": entry["query"],
            "age_seconds": age,
            "expires_in": max(0, CACHE_TTL_SECONDS - age),
            "fresh": age < CACHE_TTL_SECONDS,
        })
    return {
        "ttl_seconds": CACHE_TTL_SECONDS,
        "cached_queries": len(entries),
        "entries": sorted(entries, key=lambda e: e["age_seconds"]),
    }


def _stamp(data: dict, age: int, source: str) -> dict:
    """Attach cache metadata to the response payload."""
    return {
        **data,
        "_cache": {
            "hit": True,
            "source": source,
            "age_seconds": age,
            "expires_in": max(0, CACHE_TTL_SECONDS - age),
            "stale_at": CACHE_TTL_SECONDS,
        },
    }
