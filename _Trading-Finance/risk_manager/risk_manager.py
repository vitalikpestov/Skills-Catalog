"""
Skill: Risk Manager
Validates risk limits and calculates position size (Kelly Criterion).
Implements logic described in skills/risk_manager/SKILL.md
"""

from __future__ import annotations
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import Optional, List, Dict
from models import Prediction, PositionSizing, Decision
from session_state import SessionState
import config


def calculate_var(
    positions: List[Dict], confidence: float = 0.95
) -> float:
    """
    STUB — future VaR calculation.
    Returns 0.0 for now. Will implement Monte Carlo or parametric VaR.
    """
    # TODO: implement
    return 0.0


def check_risk_and_size(
    prediction: Prediction,
    state: SessionState,
    cfg: Optional[config.BotConfig] = None,
) -> PositionSizing:
    """
    Main entry point for Skill Risk Manager.
    Returns PositionSizing with TRADE or NO_TRADE decision.
    """
    if cfg is None:
        cfg = config.BotConfig()

    checks: Dict[str, bool] = {}
    reasons: List[str] = []

    # ── Check 1: Kill switch ───────────────────────────────────────────────
    kill = state.check_kill_switch()
    checks["kill_switch"] = not kill
    if kill:
        reasons.append("Kill switch is ACTIVE")

    # ── Check 2: Minimum edge ─────────────────────────────────────────────
    edge_ok = prediction.edge >= cfg.min_edge
    checks["min_edge"] = edge_ok
    if not edge_ok:
        reasons.append(f"Edge {prediction.edge:.3f} < min {cfg.min_edge}")

    # ── Check 2b: Extreme price — требуем edge 15% вместо 4% ──────────────
    # При p_market < 0.05 или > 0.95 простая модель не имеет достаточно данных,
    # чтобы обоснованно спорить с рынком. Clamp + веса суб-моделей
    # систематически завышают p_model для аутсайдеров.
    EXTREME_THRESHOLD = 0.10
    EXTREME_MIN_EDGE  = 0.15
    p_mkt = prediction.p_market
    is_extreme = p_mkt < EXTREME_THRESHOLD or p_mkt > (1 - EXTREME_THRESHOLD)
    if is_extreme:
        extreme_ok = prediction.edge >= EXTREME_MIN_EDGE
        checks["extreme_price_edge"] = extreme_ok
        if not extreme_ok:
            reasons.append(
                f"Extreme price (p_market={p_mkt:.3f}): "
                f"edge {prediction.edge:.3f} < required {EXTREME_MIN_EDGE} for p<5¢ markets"
            )

    # ── Check 3: Session PnL ──────────────────────────────────────────────
    session_ok = state.session_pnl_pct >= cfg.session_loss_limit
    checks["session_pnl"] = session_ok
    if not session_ok:
        reasons.append(
            f"Session PnL {state.session_pnl_pct:.1%} breached limit {cfg.session_loss_limit:.1%}"
        )

    # ── Check 4: Weekly PnL ───────────────────────────────────────────────
    weekly_ok = state.weekly_pnl_pct >= cfg.weekly_loss_limit
    checks["weekly_pnl"] = weekly_ok
    if not weekly_ok:
        reasons.append(
            f"Weekly PnL {state.weekly_pnl_pct:.1%} breached limit {cfg.weekly_loss_limit:.1%}"
        )

    # ── Check 6: Max drawdown ─────────────────────────────────────────────
    # Approximate drawdown as (initial - current) / initial
    if state.initial_bankroll > 0:
        drawdown = (state.initial_bankroll - state.bankroll) / state.initial_bankroll
    else:
        drawdown = 0.0
    drawdown_ok = drawdown <= cfg.max_drawdown
    checks["max_drawdown"] = drawdown_ok
    if not drawdown_ok:
        reasons.append(f"Drawdown {drawdown:.1%} exceeds max {cfg.max_drawdown:.1%}")

    # ── Early exit if any check failed ─────────────────────────────────────
    if not all(checks.values()):
        return PositionSizing(
            market_id=prediction.market_id,
            decision=Decision.NO_TRADE,
            side=prediction.side,
            reason="; ".join(reasons),
            checks_passed=checks,
        )

    # ── Kelly Criterion sizing ─────────────────────────────────────────────
    if prediction.side == "YES":
        p = prediction.p_model
        cost = prediction.p_market
    else:
        p = 1.0 - prediction.p_model
        cost = 1.0 - prediction.p_market

    if cost <= 0 or cost >= 1:
        return PositionSizing(
            market_id=prediction.market_id,
            decision=Decision.NO_TRADE,
            side=prediction.side,
            reason="Invalid cost (price at 0 or 1)",
            checks_passed=checks,
        )

    b = (1.0 / cost) - 1.0  # net odds
    q = 1.0 - p

    if b <= 0:
        return PositionSizing(
            market_id=prediction.market_id,
            decision=Decision.NO_TRADE,
            side=prediction.side,
            reason="Non-positive odds",
            checks_passed=checks,
        )

    f_full = (p * b - q) / b
    f_frac = f_full * cfg.fractional_kelly

    if f_frac <= 0:
        checks["kelly_positive"] = False
        return PositionSizing(
            market_id=prediction.market_id,
            decision=Decision.NO_TRADE,
            side=prediction.side,
            kelly_full=round(f_full, 6),
            kelly_fractional=round(f_frac, 6),
            reason=f"Kelly fraction non-positive (f*={f_full:.4f})",
            checks_passed=checks,
        )

    checks["kelly_positive"] = True

    # Hard caps
    f_frac = min(f_frac, cfg.max_position_fraction)
    size_usdc = f_frac * state.bankroll
    size_usdc = min(size_usdc, cfg.max_position_usdc)

    # ── Check 5: Exposure limit ────────────────────────────────────────────
    max_exposure = cfg.max_exposure_fraction * state.bankroll
    new_total_exposure = state.total_exposure + size_usdc
    exposure_ok = new_total_exposure <= max_exposure
    checks["exposure_limit"] = exposure_ok
    if not exposure_ok:
        # Reduce size to fit
        available = max_exposure - state.total_exposure
        if available <= 0:
            return PositionSizing(
                market_id=prediction.market_id,
                decision=Decision.NO_TRADE,
                side=prediction.side,
                reason=f"Exposure limit reached ({state.total_exposure:.2f}/{max_exposure:.2f})",
                checks_passed=checks,
            )
        size_usdc = min(size_usdc, available)

    size_fraction = size_usdc / state.bankroll if state.bankroll > 0 else 0

    reason = (
        f"Kelly f*={f_full:.4f}, fractional={f_frac:.4f}, "
        f"size={size_usdc:.2f} USDC ({size_fraction:.1%}). "
        f"Edge={prediction.edge:.3f}, EV={prediction.ev:.4f}"
    )

    print(
        f"[risk] TRADE: {prediction.market_id[:8]} {prediction.side} "
        f"{size_usdc:.2f} USDC ({size_fraction:.1%})"
    )

    return PositionSizing(
        market_id=prediction.market_id,
        decision=Decision.TRADE,
        side=prediction.side,
        size_usdc=round(size_usdc, 2),
        size_fraction=round(size_fraction, 4),
        kelly_full=round(f_full, 6),
        kelly_fractional=round(f_frac, 6),
        reason=reason,
        checks_passed=checks,
    )
