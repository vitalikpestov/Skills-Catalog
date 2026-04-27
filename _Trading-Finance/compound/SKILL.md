---
name: polymarket-compound
description: >
  Record trades, update performance metrics, and learn from history.
  Use when "record trade", "update metrics", "review performance", "lessons".
metadata:
  version: 1.0.0
  pattern: context-aware
  tags: [compound, learning, metrics, brier, review]
---

# Skill: Compound (Learn from History)

## Goal
Accumulate trade history and performance metrics so the system improves over
time. Every trade — especially every loss — generates a lesson.

## Input (via `record` command)
- `market_id`, `side`, `entry_price`, `exit_price`, `size_usdc`
- `predicted_probability`, `actual_outcome` (1.0 = YES won, 0.0 = NO won)
- Optional: `error_class` (prediction / timing / execution / external_shock)
- Optional: `notes`

## Output
- Updated `metrics.json`
- Updated `trades_log.json`
- Summary report for the new trade

## Entities Updated

### 1. Trade Journal (`trades_log.json`)
Append each TradeRecord with all fields.

### 2. PnL Tracking
- Per-trade PnL: `(exit_price - entry_price) * size_usdc / entry_price` for YES;
  inverted for NO
- Daily PnL aggregation (keyed by date)
- Weekly PnL aggregation (keyed by ISO week)

### 3. Brier Score
For all resolved predictions:
`BS = (1/n) * Σ(predicted_probability - actual_outcome)²`

### 4. Aggregated Metrics
- `win_rate` = wins / total
- `profit_factor` = gross_profit / gross_loss
- `max_drawdown` = largest peak-to-trough in cumulative PnL
- `sharpe_ratio` = mean(daily_returns) / std(daily_returns) * sqrt(252)
  (approximate — daily returns from PnL / bankroll)

## Error Classification
If `error_class` is not provided, use heuristic:
- If `|predicted_probability - actual_outcome| > 0.3` → "prediction"
- Else if PnL < 0 and entry was within 2h of news event → "timing" (stub)
- Else if PnL < 0 → "unknown"
- Else → None (winning trade)

## Lessons
Each classified error generates a lesson in `lessons.json`:
```json
{
  "market_id": "...",
  "error_class": "prediction",
  "lesson": "Overestimated probability on political market...",
  "timestamp": "..."
}
```
Scan and research skills can read `lessons.json` to avoid repeated mistakes.

## Logging
- Log every recorded trade
- Log updated metrics after each trade
