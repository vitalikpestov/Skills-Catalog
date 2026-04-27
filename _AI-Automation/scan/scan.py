"""
Skill: Market Scanner
Finds and ranks prediction market opportunities.
Works with any client that implements get_markets() and parse_market() — Polymarket, Kalshi, etc.
Implements logic described in skills/scan/SKILL.md
"""

from __future__ import annotations
import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import List, Optional, Any
from models import Market
from polymarket_client import PolymarketClient
import config


def _norm(values: List[float]) -> List[float]:
    """Min-max normalize a list of values to [0, 1]."""
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.5] * len(values)
    return [(v - lo) / (hi - lo) for v in values]


def scan_markets(
    category: str = "all",
    client: Any = None,
    cfg: Optional[config.BotConfig] = None,
    max_days_override: Optional[int] = None,
) -> List[Market]:
    """
    Main entry point for Skill Scan.
    Returns a sorted list of Market objects with anomaly flags and scores.
    Accepts any client with get_markets()/parse_market() interface (Polymarket, Kalshi, etc).
    """
    if client is None:
        client = PolymarketClient()
    if cfg is None:
        cfg = config.BotConfig()

    # ── Step 1: Fetch markets ──────────────────────────────────────────────
    # Single call with client-side category filter (more reliable than tag param)
    raw_markets: List[dict] = client.get_markets(category=category, limit=200)

    # Deduplicate by market_id
    seen = set()
    markets: List[Market] = []
    parse_errors = 0
    for raw in raw_markets:
        try:
            m = client.parse_market(raw)
            if m.market_id and m.market_id not in seen:
                seen.add(m.market_id)
                markets.append(m)
        except Exception as e:
            parse_errors += 1
            print(f"[scan] parse_market error: {e}")

    print(f"[scan] Fetched {len(markets)} unique markets (parse errors: {parse_errors})")

    # ── Step 2: Filter ─────────────────────────────────────────────────────
    filtered: List[Market] = []
    for m in markets:
        # Category filter
        if category != "all" and m.category != category:
            continue
        # Volume filter — use max(volume, liquidity) for platforms where volume may be 0
        effective_volume = max(m.volume, m.liquidity)
        if effective_volume < cfg.scan_min_volume:
            continue
        # Expiry filter
        max_days = max_days_override if max_days_override is not None else cfg.scan_max_days
        if m.days_to_expiry > max_days:
            continue
        # Liquidity filter — must have prices on both sides
        if m.outcome_yes_price <= 0 or m.outcome_no_price <= 0:
            continue
        # Skip expired
        if m.days_to_expiry <= 0:
            continue
        filtered.append(m)

    print(f"[scan] After filters: {len(filtered)} markets")

    if not filtered:
        return []

    # ── Step 3: Anomaly detection ──────────────────────────────────────────
    for m in filtered:
        if abs(m.price_change_pct) > config.SCAN_PRICE_JUMP_THRESHOLD:
            m.flag_price_jump = True
        if m.spread > config.SCAN_SPREAD_THRESHOLD:
            m.flag_wide_spread = True
        if m.volume_7d_avg > 0 and m.volume_24h > m.volume_7d_avg * config.SCAN_VOLUME_SPIKE_MULT:
            m.flag_volume_spike = True

    # ── Step 4: Opportunity score ──────────────────────────────────────────
    liq_vals = [m.liquidity for m in filtered]
    vol_vals = [m.volume for m in filtered]
    spread_vals = [m.spread for m in filtered]

    liq_norm = _norm(liq_vals)
    vol_norm = _norm(vol_vals)
    spread_norm = _norm(spread_vals)

    for i, m in enumerate(filtered):
        anomaly_count = sum([m.flag_price_jump, m.flag_wide_spread, m.flag_volume_spike])
        anomaly_bonus = anomaly_count * 0.33

        score = (
            0.35 * liq_norm[i]
            + 0.25 * vol_norm[i]
            + 0.20 * (1.0 - spread_norm[i])  # tighter spread = better
            + 0.10 * min(abs(m.price_change_pct), 1.0)
            + 0.10 * min(anomaly_bonus, 1.0)
        )
        m.opportunity_score = round(score, 4)

    # ── Step 5: Sort & return ──────────────────────────────────────────────
    # Сортируем по abs(price_change_pct) — рынки с движением цены первыми,
    # т.к. именно они генерируют сигналы предиктора.
    # opportunity_score остаётся в данных для отображения.
    filtered.sort(key=lambda m: abs(m.price_change_pct), reverse=True)
    print(f"[scan] Returning {len(filtered)} ranked markets")
    return filtered
