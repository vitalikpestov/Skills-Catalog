---
name: polymarket-risk-manager
description: >
  Validate risk constraints and calculate position size using Kelly Criterion.
  Use when "check risk", "size position", "kelly", "risk check".
metadata:
  version: 1.0.0
  pattern: context-aware
  tags: [risk, kelly, sizing, position]
---

# Skill: Risk Manager

## Goal
Check all risk limits and calculate recommended position size.
Output is either `PositionSizing(decision=TRADE)` or `PositionSizing(decision=NO_TRADE)`.
**No orders are executed** — this is semi-auto mode.

## Input
- `Prediction` (from predictor skill)
- `SessionState` (bankroll, session PnL, weekly PnL, open positions)
- `BotConfig` (risk parameters)

## Output
`PositionSizing`:
- `decision`: TRADE or NO_TRADE
- `side`: YES or NO
- `size_usdc`: recommended bet in USDC
- `size_fraction`: as fraction of bankroll
- `kelly_full`: full Kelly fraction
- `kelly_fractional`: fractional Kelly
- `reason`: human-readable explanation
- `checks_passed`: dict of check name → bool

## Risk Checks (ALL must pass)

### 1. Kill switch
If `STOP` file exists in data/ → NO_TRADE ("Kill switch active")

### 2. Edge check
`prediction.edge >= config.min_edge (0.04)` → must be True

### 3. Session PnL limit
`session_state.session_pnl_pct >= config.session_loss_limit (-5%)`

### 4. Weekly PnL limit
`session_state.weekly_pnl_pct >= config.weekly_loss_limit (-25%)`

### 5. Exposure limit
`session_state.total_exposure + new_size <= config.max_exposure_fraction * bankroll`

### 6. Max drawdown
If max drawdown exceeds `config.max_drawdown (8%)` → NO_TRADE

## Kelly Criterion Sizing

```
p = prediction.p_model (for chosen side)
q = 1 - p
b = (1 / cost) - 1       # net odds
f_full = (p * b - q) / b  # full Kelly
f_frac = f_full * config.fractional_kelly  # quarter-Kelly default
```

### Hard limits on f_frac:
- Must be > 0 (otherwise NO_TRADE)
- Capped at `config.max_position_fraction` (5% of bankroll)
- `size_usdc = f_frac * bankroll`
- Capped at `config.max_position_usdc` (50 USDC)

## VaR Interface (STUB)
Function signature exists for future VaR calculation:
```python
def calculate_var(positions, confidence=0.95) -> float:
    # TODO: implement Monte Carlo or parametric VaR
    return 0.0
```

## Kill Switch
A file `data/STOP` — if present, ALL decisions become NO_TRADE.
To resume trading, delete the file.

## Logging
- Log all checks (pass/fail) and final decision
- Log Kelly calculation details
