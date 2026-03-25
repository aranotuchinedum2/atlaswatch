import re
from collections import Counter
from typing import List, Dict, Any

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

AFCON_LEXICON = {
    "cheat": -2.5, "cheated": -2.5, "robbery": -3.0, "scandal": -2.5,
    "unfair": -2.0, "controversial": -1.0, "rigged": -3.0, "corrupt": -2.8,
    "disgrace": -3.0, "deserve": 1.5, "champions": 2.0, "celebrate": 2.0,
    "proud": 2.0, "historic": 1.8, "rightful": 1.5, "justice": 1.5,
}
for word, score in AFCON_LEXICON.items():
    _analyzer.lexicon[word] = score

STOP_WORDS = {
    "the","a","an","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","was","are","were","be","been","being","have","has",
    "had","do","does","did","will","would","could","should","may","might",
    "shall","can","that","this","it","its","i","you","he","she","we","they",
    "my","your","his","her","our","their","rt","https","http","amp","com",
    "twitter","just","like","get","got","also","said","about","after","who",
    "what","how","when","if","so","not","no","morocco","senegal","afcon",
}


def _label(compound: float) -> str:
    if compound >= 0.05:
        return "positive"
    if compound <= -0.05:
        return "negative"
    return "neutral"


def analyze_sentiment(tweets: List[Dict[str, Any]]) -> Dict[str, Any]:
    analyzed = []
    for tw in tweets:
        scores = _analyzer.polarity_scores(tw["text"])
        tw["sentiment"] = {
            "compound": round(scores["compound"], 4),
            "pos": round(scores["pos"], 4),
            "neg": round(scores["neg"], 4),
            "neu": round(scores["neu"], 4),
            "label": _label(scores["compound"]),
        }
        analyzed.append(tw)

    total = len(analyzed) or 1
    label_counts = Counter(t["sentiment"]["label"] for t in analyzed)
    pos = label_counts.get("positive", 0)
    neg = label_counts.get("negative", 0)
    neu = label_counts.get("neutral", 0)
    avg = round(sum(t["sentiment"]["compound"] for t in analyzed) / total, 4)

    if avg >= 0.15:
        overall = "🟢 Celebratory"
    elif avg >= 0.0:
        overall = "🟡 Mixed–Positive"
    elif avg >= -0.15:
        overall = "🟠 Mixed–Negative"
    else:
        overall = "🔴 Outrage"

    return {
        "tweets": analyzed,
        "stats": {
            "total": len(analyzed),
            "positive": pos, "negative": neg, "neutral": neu,
            "positive_pct": round(pos / total * 100),
            "negative_pct": round(neg / total * 100),
            "neutral_pct": round(neu / total * 100),
            "avg_compound": avg,
            "overall": overall,
        },
        "keywords": _top_keywords([t["text"] for t in analyzed]),
        "timeline": _build_timeline(analyzed),
    }


def _top_keywords(texts: List[str]) -> List[Dict[str, Any]]:
    words = []
    for text in texts:
        clean = re.sub(r"http\S+|@\w+|#", "", text.lower())
        words.extend(w for w in re.findall(r"\b[a-zA-Z]{4,}\b", clean) if w not in STOP_WORDS)
    counter = Counter(words)
    return [{"word": w, "count": c} for w, c in counter.most_common(25)]


def _build_timeline(tweets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    chunk = 5
    timeline = []
    for i in range(0, len(tweets), chunk):
        batch = tweets[i: i + chunk]
        avg = sum(t["sentiment"]["compound"] for t in batch) / len(batch)
        timeline.append({
            "batch": i // chunk + 1,
            "avg": round(avg, 3),
            "label": _label(avg),
            "count": len(batch),
        })
    return timeline