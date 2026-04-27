"""
Skill: Predictor
Estimates true probability and calculates edge/EV.
Implements logic described in skills/predictor/SKILL.md
"""

from __future__ import annotations
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Optional
from models import Market, ResearchBrief, Prediction, Sentiment, save_json, load_json
import config


def _clamp(v: float, lo: float = 0.005, hi: float = 0.995) -> float:
    return max(lo, min(hi, v))


def _model_direction(p_market: float, price_change_pct: float) -> float:
    """Model A: Price momentum — follow the weekly price direction.

    If the market moved 5%+ in a week, informed money is moving it.
    We follow that direction. Full signal at 10%+ weekly move.
    Coefficient 0.15 → max ±15% adjustment to p_market.
    """
    if abs(price_change_pct) < 0.05:
        return p_market  # below noise threshold
    strength = min(abs(price_change_pct) / 0.10, 1.0)
    direction = strength * 0.15 * (1 if price_change_pct > 0 else -1)
    return _clamp(p_market + direction)


def _model_sentiment(p_market: float, sentiment: Sentiment) -> float:
    """Model B: Sentiment adjustment (±7%)."""
    if sentiment == Sentiment.BULLISH:
        return _clamp(p_market + 0.07)
    elif sentiment == Sentiment.BEARISH:
        return _clamp(p_market - 0.07)
    return p_market


def _model_volume_signal(
    p_market: float,
    volume_spike: bool,
    price_change_pct: float,
    sentiment: Sentiment,
) -> float:
    """Model C: Volume spike confirms the price direction.
    When there's an unusual volume spike AND price moved, amplify the signal.
    """
    if volume_spike and abs(price_change_pct) > 0.03:
        direction = 0.05 if price_change_pct > 0 else -0.05
        return _clamp(p_market + direction)
    return p_market


def _model_volume_recency(
    p_market: float,
    volume_24h: float,
    volume_7d_avg: float,
    price_change_pct: float,
) -> float:
    """Model D: Volume momentum — today vs 7-day average.

    If today's volume is 2x+ the weekly average AND price is moving:
    strong momentum signal. Without price direction: mild pull toward 0.5
    (market is active but uncertain).
    """
    if volume_7d_avg <= 0 or volume_24h <= 0:
        return p_market
    ratio = volume_24h / volume_7d_avg
    if ratio < 2.0:
        return p_market
    strength = min((ratio - 2.0) / 2.0, 1.0)  # 0..1 at ratio 2x..4x
    if abs(price_change_pct) > 0.02:
        # High volume + price move = strong confirmation
        direction = strength * 0.10 * (1 if price_change_pct > 0 else -1)
        return _clamp(p_market + direction)
    # High volume, no direction → mild uncertainty pull toward 0.5
    return _clamp(p_market + strength * 0.05 * (0.5 - p_market))


def _model_spread_fade(
    p_market: float,
    spread: float,
    price_change_pct: float,
) -> float:
    """Model E: Wide spread + large price move → partial fade (mean reversion).

    Wide spread means market makers are uncertain about the new price.
    A wide spread after a big move suggests possible overreaction.
    """
    if spread < 0.02:
        return p_market  # tight spread, no overreaction signal
    if abs(price_change_pct) < 0.05:
        return p_market  # no significant move to question
    fade_strength = min(spread / 0.08, 1.0) * min(abs(price_change_pct) / 0.15, 1.0)
    direction = -0.06 * fade_strength * (1 if price_change_pct > 0 else -1)
    return _clamp(p_market + direction)


def predict(
    market: Market,
    brief: ResearchBrief,
    cfg: Optional[config.BotConfig] = None,
) -> Prediction:
    """
    Main entry point for Skill Predictor.
    Returns a Prediction with p_model, edge, EV, etc.
    """
    if cfg is None:
        cfg = config.BotConfig()

    # Step 1 — p_market
    p_market = market.outcome_yes_price
    if p_market <= 0 or p_market >= 1:
        p_market = 0.50  # fallback

    # Step 2 — Sub-models
    p_a = _model_direction(p_market, market.price_change_pct)
    p_b = _model_sentiment(p_market, brief.sentiment)
    p_c = _model_volume_signal(
        p_market, market.flag_volume_spike, market.price_change_pct, brief.sentiment
    )
    p_d = _model_volume_recency(
        p_market, market.volume_24h, market.volume_7d_avg, market.price_change_pct
    )
    p_e = _model_spread_fade(p_market, market.spread, market.price_change_pct)

    sub_models = {
        "direction":      round(p_a, 4),
        "sentiment":      round(p_b, 4),
        "volume_signal":  round(p_c, 4),
        "volume_recency": round(p_d, 4),
        "spread_fade":    round(p_e, 4),
    }

    # Step 3 — Aggregate (weights sum to 1.0)
    p_model = _clamp(
        0.35 * p_a   # direction momentum (primary signal)
        + 0.15 * p_b  # sentiment
        + 0.15 * p_c  # volume spike confirmation
        + 0.25 * p_d  # volume recency (today vs weekly avg)
        + 0.10 * p_e  # spread fade (partial mean reversion)
    )

    # Step 4 — Determine side
    if p_model >= p_market:
        side = "YES"
    else:
        side = "NO"

    # Step 5 — Metrics
    edge = abs(p_model - p_market)

    # For the chosen side
    if side == "YES":
        p = p_model
        cost = p_market
    else:
        p = 1.0 - p_model
        cost = 1.0 - p_market

    if cost > 0 and cost < 1:
        b = (1.0 / cost) - 1.0  # decimal odds - 1
        ev = p * b - (1.0 - p)
    else:
        b = 0.0
        ev = 0.0

    std = cfg.prediction_std
    mispricing_score = (p_model - p_market) / std if std > 0 else 0.0

    # Step 6 — Confidence
    vol_factor = 0.5 + 0.5 * min(market.volume / 10000.0, 1.0)
    confidence = min(edge / 0.10, 1.0) * vol_factor
    confidence = round(_clamp(confidence, 0.0, 1.0), 3)

    prediction = Prediction(
        market_id=market.market_id,
        p_model=round(p_model, 4),
        p_market=round(p_market, 4),
        edge=round(edge, 4),
        ev=round(ev, 4),
        mispricing_score=round(mispricing_score, 2),
        confidence=confidence,
        side=side,
        sub_model_outputs=sub_models,
    )

    # Step 7 — Log prediction
    _log_prediction(prediction)

    print(
        f"[predictor] {market.market_id[:8]}: "
        f"p_model={prediction.p_model:.3f} p_market={prediction.p_market:.3f} "
        f"edge={prediction.edge:+.3f} side={prediction.side} conf={prediction.confidence:.2f}"
    )

    return prediction


def _log_prediction(pred: Prediction):
    """Append prediction to log file."""
    log = load_json(config.PREDICTIONS_LOG_FILE, default=[])
    if not isinstance(log, list):
        log = []
    log.append(pred.to_dict())
    save_json(config.PREDICTIONS_LOG_FILE, log)
