"""
Technical Indicators — RSI, MACD, Bollinger Bands, Stochastic, ATR, OBI.

Ported from Repo A (polymarket-prediction-system) TechnicalIndicators class.
All functions are stateless (pure) — take price series, return indicator values.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional, Tuple
import math


def rsi(prices: List[float], period: int = 14) -> float:
    """Relative Strength Index (0-100).

    > 70 = overbought, < 30 = oversold.
    """
    if len(prices) < period + 1:
        return 50.0  # neutral if not enough data

    gains = []
    losses = []
    for i in range(1, len(prices)):
        delta = prices[i] - prices[i - 1]
        if delta > 0:
            gains.append(delta)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(delta))

    # Use last `period` values
    recent_gains = gains[-period:]
    recent_losses = losses[-period:]

    avg_gain = sum(recent_gains) / period
    avg_loss = sum(recent_losses) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def macd(
    prices: List[float],
    fast: int = 12,
    slow: int = 26,
    signal_period: int = 9,
) -> Dict[str, float]:
    """MACD (Moving Average Convergence Divergence).

    Returns: {"macd": float, "signal": float, "histogram": float}
    """
    if len(prices) < slow + signal_period:
        return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}

    fast_ema = _ema(prices, fast)
    slow_ema = _ema(prices, slow)
    macd_line = fast_ema - slow_ema

    # Signal line: EMA of MACD values (approximate with single value)
    # For proper signal, need MACD series — use simplified version
    signal_val = macd_line * 0.8  # rough approximation
    histogram = macd_line - signal_val

    return {
        "macd": round(macd_line, 6),
        "signal": round(signal_val, 6),
        "histogram": round(histogram, 6),
    }


def bollinger_bands(
    prices: List[float],
    period: int = 20,
    num_std: float = 2.0,
) -> Dict[str, float]:
    """Bollinger Bands.

    Returns: {"upper": float, "middle": float, "lower": float, "bandwidth": float, "pct_b": float}
    """
    if len(prices) < period:
        p = prices[-1] if prices else 0.5
        return {"upper": p, "middle": p, "lower": p, "bandwidth": 0.0, "pct_b": 0.5}

    window = prices[-period:]
    middle = sum(window) / len(window)
    variance = sum((p - middle) ** 2 for p in window) / len(window)
    std = variance ** 0.5

    upper = middle + num_std * std
    lower = middle - num_std * std
    bandwidth = (upper - lower) / middle if middle > 0 else 0
    pct_b = (prices[-1] - lower) / (upper - lower) if upper != lower else 0.5

    return {
        "upper": round(upper, 4),
        "middle": round(middle, 4),
        "lower": round(lower, 4),
        "bandwidth": round(bandwidth, 4),
        "pct_b": round(pct_b, 4),
    }


def stochastic_oscillator(
    prices: List[float],
    period: int = 14,
) -> Dict[str, float]:
    """Stochastic Oscillator (%K, %D).

    Returns: {"k": float (0-100), "d": float (0-100)}
    """
    if len(prices) < period:
        return {"k": 50.0, "d": 50.0}

    window = prices[-period:]
    low = min(window)
    high = max(window)

    if high == low:
        k = 50.0
    else:
        k = ((prices[-1] - low) / (high - low)) * 100.0

    # %D = 3-period SMA of %K (approximated)
    d = k  # simplified
    return {"k": round(k, 2), "d": round(d, 2)}


def atr(
    highs: List[float],
    lows: List[float],
    closes: List[float],
    period: int = 14,
) -> float:
    """Average True Range — volatility indicator.

    For prediction markets without OHLC, approximate from price series.
    """
    if len(closes) < period + 1:
        return 0.0

    true_ranges = []
    for i in range(1, len(closes)):
        h = highs[i] if i < len(highs) else closes[i]
        l = lows[i] if i < len(lows) else closes[i]
        prev_c = closes[i - 1]
        tr = max(h - l, abs(h - prev_c), abs(l - prev_c))
        true_ranges.append(tr)

    if not true_ranges:
        return 0.0
    return sum(true_ranges[-period:]) / min(period, len(true_ranges))


def volatility(prices: List[float], period: int = 20) -> float:
    """Price volatility (std dev of returns)."""
    if len(prices) < 2:
        return 0.0
    returns = []
    for i in range(1, len(prices)):
        if prices[i - 1] > 0:
            returns.append((prices[i] - prices[i - 1]) / prices[i - 1])
    if len(returns) < 2:
        return 0.0
    window = returns[-period:]
    mean = sum(window) / len(window)
    var = sum((r - mean) ** 2 for r in window) / len(window)
    return round(var ** 0.5, 6)


def order_book_imbalance(
    bids: List[List],
    asks: List[List],
    levels: int = 3,
    decay: float = 0.7,
) -> Dict[str, float]:
    """Order Book Imbalance (OBI) with exponential decay weighting.

    From Repo A: measures buy/sell pressure across top N levels.

    Returns:
        {"obi": float (-1 to +1), "bid_pressure": float, "ask_pressure": float,
         "imbalance_level_1": float, ...}
    """
    bid_levels = []
    for entry in bids[:levels]:
        s = float(entry[1] if isinstance(entry, list) else entry.get("size", 0))
        bid_levels.append(s)

    ask_levels = []
    for entry in asks[:levels]:
        s = float(entry[1] if isinstance(entry, list) else entry.get("size", 0))
        ask_levels.append(s)

    # Weighted volumes with exponential decay
    bid_weighted = 0.0
    ask_weighted = 0.0
    for i in range(min(levels, len(bid_levels))):
        weight = decay ** i
        bid_weighted += bid_levels[i] * weight if i < len(bid_levels) else 0
    for i in range(min(levels, len(ask_levels))):
        weight = decay ** i
        ask_weighted += ask_levels[i] * weight if i < len(ask_levels) else 0

    total = bid_weighted + ask_weighted
    obi = (bid_weighted - ask_weighted) / total if total > 0 else 0.0

    result = {
        "obi": round(obi, 4),
        "bid_pressure": round(bid_weighted, 2),
        "ask_pressure": round(ask_weighted, 2),
    }
    # Per-level imbalance
    for i in range(levels):
        b = bid_levels[i] if i < len(bid_levels) else 0
        a = ask_levels[i] if i < len(ask_levels) else 0
        t = b + a
        result[f"imbalance_level_{i+1}"] = round((b - a) / t, 4) if t > 0 else 0.0

    return result


def compute_all(
    prices: List[float],
    orderbook: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Compute all technical indicators for a price series.

    Args:
        prices: list of historical YES prices (oldest → newest)
        orderbook: {"bids": [...], "asks": [...]} for OBI

    Returns:
        Dict with all indicator values.
    """
    result = {}

    # RSI
    result["rsi"] = round(rsi(prices), 2)
    result["rsi_signal"] = "overbought" if result["rsi"] > 70 else ("oversold" if result["rsi"] < 30 else "neutral")

    # MACD
    result["macd"] = macd(prices)

    # Bollinger Bands
    result["bollinger"] = bollinger_bands(prices)

    # Stochastic
    result["stochastic"] = stochastic_oscillator(prices)

    # Volatility
    result["volatility"] = volatility(prices)
    result["volatility_alert"] = result["volatility"] > 0.05

    # OBI (if orderbook provided)
    if orderbook:
        bids = orderbook.get("bids", [])
        asks = orderbook.get("asks", [])
        result["obi"] = order_book_imbalance(bids, asks)
    else:
        result["obi"] = {"obi": 0.0, "bid_pressure": 0.0, "ask_pressure": 0.0}

    return result


# ── Private helpers ───────────────────────────────────────────────────────

def _ema(prices: List[float], period: int) -> float:
    """Exponential Moving Average (last value)."""
    if not prices:
        return 0.0
    if len(prices) <= period:
        return sum(prices) / len(prices)

    multiplier = 2.0 / (period + 1)
    ema_val = sum(prices[:period]) / period

    for price in prices[period:]:
        ema_val = (price - ema_val) * multiplier + ema_val

    return ema_val
