"""
Skill: Compound (Learn from History)
Records trades, updates metrics, classifies errors.
Implements logic described in skills/compound/SKILL.md
"""

from __future__ import annotations
import sys
import os
import math
from datetime import datetime
from typing import Optional, List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from models import (
    TradeRecord, Metrics, ErrorClass,
    save_json, load_json,
)
import config


def _compute_pnl(trade: TradeRecord) -> float:
    """Calculate PnL for a trade."""
    if trade.entry_price <= 0:
        return 0.0
    if trade.side == "YES":
        # Bought YES at entry_price, resolved/sold at exit_price
        return (trade.exit_price - trade.entry_price) * trade.size_usdc / trade.entry_price
    else:
        # Bought NO (= sold YES): profit if YES price goes down
        return (trade.entry_price - trade.exit_price) * trade.size_usdc / (1 - trade.entry_price + 0.001)


def _classify_error(trade: TradeRecord) -> Optional[ErrorClass]:
    """Heuristic error classification."""
    if trade.error_class:
        return trade.error_class

    if trade.pnl >= 0:
        return None  # winning trade

    if trade.actual_outcome is not None:
        gap = abs(trade.predicted_probability - trade.actual_outcome)
        if gap > 0.3:
            return ErrorClass.PREDICTION

    return ErrorClass.UNKNOWN


def record_trade(
    market_id: str,
    side: str,
    entry_price: float,
    exit_price: float,
    size_usdc: float,
    predicted_probability: float,
    actual_outcome: Optional[float] = None,
    error_class: Optional[str] = None,
    notes: str = "",
) -> Dict[str, Any]:
    """
    Main entry point for Skill Compound.
    Records a trade and updates all metrics.
    Returns a summary dict.
    """
    # Build trade record
    trade = TradeRecord(
        trade_id=f"{market_id[:8]}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        market_id=market_id,
        side=side.upper(),
        entry_price=entry_price,
        exit_price=exit_price,
        size_usdc=size_usdc,
        predicted_probability=predicted_probability,
        actual_outcome=actual_outcome,
        entry_time=datetime.utcnow().isoformat(),
        exit_time=datetime.utcnow().isoformat(),
        notes=notes,
    )

    if error_class:
        try:
            trade.error_class = ErrorClass(error_class)
        except ValueError:
            trade.error_class = ErrorClass.UNKNOWN

    # Calculate PnL
    trade.pnl = round(_compute_pnl(trade), 4)

    # Classify error if loss
    if trade.pnl < 0 and trade.error_class is None:
        trade.error_class = _classify_error(trade)

    # ── Save to trades log ─────────────────────────────────────────────────
    trades = load_json(config.TRADES_LOG_FILE, default=[])
    if not isinstance(trades, list):
        trades = []
    trades.append(trade.to_dict())
    save_json(config.TRADES_LOG_FILE, trades)

    # ── Update metrics ─────────────────────────────────────────────────────
    metrics = _recalculate_metrics(trades)

    # ── Save lesson if error ───────────────────────────────────────────────
    if trade.error_class and trade.pnl < 0:
        _save_lesson(trade)

    # ── Summary ────────────────────────────────────────────────────────────
    summary = {
        "trade_id": trade.trade_id,
        "market_id": trade.market_id,
        "side": trade.side,
        "pnl": trade.pnl,
        "error_class": trade.error_class.value if trade.error_class else None,
        "metrics": metrics.to_dict(),
    }

    print(
        f"[compound] Recorded: {trade.trade_id} "
        f"PnL={trade.pnl:+.2f} USDC "
        f"error={trade.error_class.value if trade.error_class else 'none'}"
    )

    return summary


def _recalculate_metrics(trades: List[Dict[str, Any]]) -> Metrics:
    """Recalculate all metrics from full trade history."""
    m = Metrics()
    m.total_trades = len(trades)

    gross_profit = 0.0
    gross_loss = 0.0
    cumulative_pnl = 0.0
    peak_pnl = 0.0
    max_dd = 0.0
    daily_returns: Dict[str, float] = {}
    brier_sum = 0.0
    brier_n = 0

    for t in trades:
        pnl = t.get("pnl", 0.0)
        if pnl > 0:
            m.wins += 1
            gross_profit += pnl
        elif pnl < 0:
            m.losses += 1
            gross_loss += abs(pnl)

        cumulative_pnl += pnl
        peak_pnl = max(peak_pnl, cumulative_pnl)
        dd = peak_pnl - cumulative_pnl
        max_dd = max(max_dd, dd)

        # Daily PnL
        exit_time = t.get("exit_time", "")
        if exit_time:
            day_key = exit_time[:10]
            daily_returns[day_key] = daily_returns.get(day_key, 0) + pnl

        # Brier score
        predicted = t.get("predicted_probability")
        outcome = t.get("actual_outcome")
        if predicted is not None and outcome is not None:
            brier_sum += (predicted - outcome) ** 2
            brier_n += 1

    m.total_pnl = round(cumulative_pnl, 4)
    m.max_drawdown = round(max_dd, 4)
    m.win_rate = round(m.wins / m.total_trades, 4) if m.total_trades > 0 else 0
    m.profit_factor = round(gross_profit / gross_loss, 4) if gross_loss > 0 else 999.0
    m.brier_score = round(brier_sum / brier_n, 4) if brier_n > 0 else 0.0

    # Sharpe ratio (annualized, approximate)
    if daily_returns:
        daily_vals = list(daily_returns.values())
        mean_r = sum(daily_vals) / len(daily_vals)
        if len(daily_vals) > 1:
            variance = sum((r - mean_r) ** 2 for r in daily_vals) / (len(daily_vals) - 1)
            std_r = math.sqrt(variance) if variance > 0 else 0.001
            m.sharpe_ratio = round((mean_r / std_r) * math.sqrt(252), 4)
        else:
            m.sharpe_ratio = 0.0

    m.daily_pnl = {k: round(v, 4) for k, v in daily_returns.items()}

    # Weekly PnL (ISO week key)
    weekly: Dict[str, float] = {}
    for t in trades:
        exit_time = t.get("exit_time", "")
        if exit_time:
            try:
                dt = datetime.fromisoformat(exit_time)
                week_key = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
                weekly[week_key] = weekly.get(week_key, 0) + t.get("pnl", 0)
            except Exception:
                pass
    m.weekly_pnl = {k: round(v, 4) for k, v in weekly.items()}

    save_json(config.METRICS_FILE, m.to_dict())
    return m


def _save_lesson(trade: TradeRecord):
    """Save a lesson from a losing trade."""
    lessons = load_json(config.LESSONS_FILE, default=[])
    if not isinstance(lessons, list):
        lessons = []

    lesson = {
        "market_id": trade.market_id,
        "error_class": trade.error_class.value if trade.error_class else "unknown",
        "lesson": (
            f"Lost {abs(trade.pnl):.2f} USDC on {trade.side} "
            f"(predicted={trade.predicted_probability:.2f}, "
            f"outcome={trade.actual_outcome}). "
            f"Class: {trade.error_class.value if trade.error_class else 'unknown'}. "
            f"{trade.notes}"
        ),
        "timestamp": datetime.utcnow().isoformat(),
    }
    lessons.append(lesson)
    save_json(config.LESSONS_FILE, lessons)


def get_metrics() -> Metrics:
    """Load current metrics from disk."""
    data = load_json(config.METRICS_FILE, default={})
    if data:
        return Metrics.from_dict(data)
    return Metrics()


def get_lessons() -> List[Dict[str, Any]]:
    """Load lessons from disk."""
    return load_json(config.LESSONS_FILE, default=[])
