---
name: polymarket-scan
description: >
  Scan and rank Polymarket markets for trading opportunities.
  Use when "scan markets", "find opportunities", "scan us_politics", "scan crypto".
metadata:
  version: 1.0.0
  pattern: context-aware
  tags: [scan, polymarket, markets, discovery]
---

# Skill: Market Scanner

## Goal
Find and rank interesting Polymarket markets in the US politics and crypto
categories that have sufficient liquidity, volume, and potential mispricing.

## Input
- `category`: one of `us_politics`, `crypto`, or `all`
- Bot config (from `config.py`)

## Output
Sorted list of `Market` objects with:
- anomaly flags (`flag_price_jump`, `flag_wide_spread`, `flag_volume_spike`)
- `opportunity_score` (0..1)

## Algorithm

### Step 1 — Fetch markets
- Call Polymarket Gamma API to get active markets
- Parse each into a `Market` dataclass

### Step 2 — Filter
1. `volume >= config.scan_min_volume` (default 200)
2. `days_to_expiry <= config.scan_max_days` (default 30)
3. `best_bid > 0 AND best_ask > 0` (both sides of book)
4. Category matches requested filter

### Step 3 — Anomaly detection
For each surviving market:
- **Price jump**: `|price_change_pct| > 0.10` → `flag_price_jump = True`
- **Wide spread**: `spread > 0.05` → `flag_wide_spread = True`
- **Volume spike**: `volume_24h > volume_7d_avg * SCAN_VOLUME_SPIKE_MULT` → `flag_volume_spike = True`

### Step 4 — Opportunity score
```
score = (
    0.35 * norm(liquidity)
  + 0.25 * norm(volume)
  + 0.20 * (1.0 - norm(spread))       # tighter is better
  + 0.10 * abs(price_change_pct)
  + 0.10 * anomaly_bonus
)
```
Where `anomaly_bonus` = 0.33 per flag set.
`norm(x)` = `x / max(x across all markets)` (min-max within batch).

### Step 5 — Sort & return
Return markets sorted by `opportunity_score` descending.

## Risk Checks
- Never include markets with zero liquidity
- Never include expired markets

## Prompt-Injection Protection
- No external text is processed in this skill; only structured API data

## Logging
- Log number of markets fetched, filtered, and returned
- Log any API errors
