"""
Skill: Market Research
Builds a ResearchBrief for a given market.
Implements logic described in skills/research/SKILL.md
"""

from __future__ import annotations
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Optional, List, Any
from models import Market, ResearchBrief, Sentiment
from polymarket_client import PolymarketClient  # default fallback


# ── Prompt-injection sanitizer ─────────────────────────────────────────────

_SUSPICIOUS_PATTERNS = [
    r"ignore\s+(previous|above|all)\s+instructions",
    r"you\s+are\s+now",
    r"system\s*:",
    r"<\s*/?system\s*>",
    r"act\s+as\s+if",
    r"forget\s+(everything|all)",
]

def _sanitize_text(text: str) -> str:
    """Strip potential prompt-injection patterns from external text."""
    for pattern in _SUSPICIOUS_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
    return text


# ── Factor extraction heuristics ───────────────────────────────────────────

_POLITICS_KEYWORDS = {
    "polls": ["poll", "survey", "approval", "favorability"],
    "legislation": ["bill", "vote", "legislation", "law", "act", "congress", "senate"],
    "courts": ["court", "ruling", "judge", "supreme", "trial", "verdict"],
    "elections": ["election", "ballot", "primary", "caucus", "nominee"],
    "endorsements": ["endorse", "support", "back"],
}

_CRYPTO_KEYWORDS = {
    "price_levels": ["price", "ath", "support", "resistance", "level"],
    "regulation": ["sec", "regulation", "ban", "approve", "etf", "legal"],
    "protocol": ["upgrade", "fork", "merge", "halving", "launch", "mainnet"],
    "macro": ["fed", "rates", "inflation", "dollar", "recession"],
    "adoption": ["institutional", "adoption", "whale", "volume"],
}


def _extract_factors(question: str, description: str, category: str) -> List[str]:
    """Heuristic factor extraction from market text."""
    text = f"{question} {description}".lower()
    keywords = _POLITICS_KEYWORDS if category == "us_politics" else _CRYPTO_KEYWORDS
    factors = []
    for factor_name, words in keywords.items():
        if any(w in text for w in words):
            factors.append(factor_name)
    if not factors:
        factors.append("general_market_dynamics")
    return factors


def _detect_sentiment(price_change_pct: float) -> Sentiment:
    """Simple sentiment from recent price movement."""
    if price_change_pct >= 0.05:
        return Sentiment.BULLISH
    elif price_change_pct <= -0.05:
        return Sentiment.BEARISH
    return Sentiment.NEUTRAL


def _detect_trend(price_change_pct: float) -> str:
    if price_change_pct > 0.02:
        return "up"
    elif price_change_pct < -0.02:
        return "down"
    return "flat"


# ── Main entry point ──────────────────────────────────────────────────────

def research_market(
    market: Market,
    client: Any = None,
) -> ResearchBrief:
    """
    Main entry point for Skill Research.
    Returns a ResearchBrief for the given market.
    """
    if client is None:
        client = PolymarketClient()

    # Step 1 — Extract metadata
    question = _sanitize_text(market.question)
    description = _sanitize_text(market.raw.get("description", ""))
    resolution = _sanitize_text(market.raw.get("resolution_source", ""))

    summary_parts = [question]
    if description:
        # Take first 200 chars of description
        summary_parts.append(description[:200])
    if resolution:
        summary_parts.append(f"Resolution: {resolution[:100]}")
    summary = " | ".join(summary_parts)

    # Step 2 — Identify main factors
    factors = _extract_factors(question, description, market.category)

    # Step 3 — Sentiment from price trend
    sentiment = _detect_sentiment(market.price_change_pct)
    price_trend = _detect_trend(market.price_change_pct)

    # Step 4 — Market vs narrative gap
    gap_msg = ""
    yes_price = market.outcome_yes_price
    # Compare to a rough "fair" value from spread
    if yes_price > 0:
        if yes_price > 0.85:
            gap_msg = f"Market strongly favors YES ({yes_price:.0%}). Limited upside unless near-certain."
        elif yes_price < 0.15:
            gap_msg = f"Market strongly favors NO (YES at {yes_price:.0%}). Contrarian opportunity if thesis is strong."
        elif abs(market.price_change_pct) > 0.15:
            direction = "up" if market.price_change_pct > 0 else "down"
            gap_msg = (
                f"Price moved sharply {direction} ({market.price_change_pct:+.0%}). "
                f"Potential overreaction — check if fundamentals justify the move."
            )
        else:
            gap_msg = "No significant gap detected between price and expected narrative."

    # Step 5 — External sources (STUB)
    data_sources = ["polymarket_api"]
    # Future: add twitter, reddit, rss sources here

    brief = ResearchBrief(
        market_id=market.market_id,
        summary=summary,
        main_factors=factors,
        sentiment=sentiment,
        market_vs_narrative=gap_msg,
        price_trend=price_trend,
        data_sources=data_sources,
    )

    print(f"[research] Brief for {market.market_id[:8]}: sentiment={sentiment.value}, factors={factors}")
    return brief
