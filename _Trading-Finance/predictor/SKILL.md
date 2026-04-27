---
name: polymarket-predictor
description: >
  Estimate true probability of a market outcome and calculate edge/EV.
  Use when "predict", "estimate probability", "calculate edge".
metadata:
  version: 1.0.0
  pattern: context-aware
  tags: [predictor, probability, edge, ev, brier]
---

# Skill: Predictor

## Goal
Convert a ResearchBrief and market data into a probability estimate (`p_model`)
and calculate mispricing metrics (edge, EV, mispricing_score).

## Input
- `ResearchBrief`
- `Market` (current prices, volume, history)
- `config.prediction_std` (default 0.10)

## Output
`Prediction` with:
- `p_model` — model's estimated probability
- `p_market` — market-implied probability (YES price)
- `edge` — `p_model - p_market` (min 0.04 for trading)
- `ev` — `p * b - (1 - p)`
- `mispricing_score` — `(p_model - p_market) / std`
- `confidence` — 0..1
- `side` — "YES" or "NO"
- `sub_model_outputs` — dict of individual model estimates

## Algorithm

### Step 1 — Extract p_market
`p_market = market.outcome_yes_price` (the YES contract price IS the implied probability)

### Step 2 — Run sub-models
Ensemble of simple models (extensible):

**Model A — Mean reversion**
If price moved sharply recently, estimate a partial reversion:
`p_a = p_market + 0.3 * (0.50 - p_market) * |price_change_pct|`
Clamped to [0.01, 0.99]

**Model B — Sentiment adjustment**
Adjust based on ResearchBrief sentiment:
- bullish: `p_b = p_market + 0.05`
- bearish: `p_b = p_market - 0.05`
- neutral: `p_b = p_market`
Clamped to [0.01, 0.99]

**Model C — Liquidity/volume signal**
High volume + price movement = stronger signal:
- If volume_spike AND price moved in direction → amplify sentiment by 0.03
- Else → p_c = p_market

### Step 3 — Aggregate into p_model
Weighted average:
`p_model = 0.40 * p_a + 0.35 * p_b + 0.25 * p_c`
Clamped to [0.01, 0.99]

### Step 4 — Determine side
- If `p_model > p_market` → side = "YES" (buy YES, market underprices YES)
- If `p_model < p_market` → side = "NO"  (buy NO, market overprices YES)

### Step 5 — Calculate metrics
```
edge = abs(p_model - p_market)
# For the chosen side:
p = p_model if side == "YES" else (1 - p_model)
cost = p_market if side == "YES" else (1 - p_market)
b = (1 / cost) - 1    # decimal odds - 1
ev = p * b - (1 - p)
mispricing_score = (p_model - p_market) / std
```

### Step 6 — Confidence
`confidence = min(edge / 0.10, 1.0) * (0.5 + 0.5 * min(volume / 10000, 1.0))`

### Step 7 — Log prediction
Append to `predictions_log.json` for future Brier score calculation.

## Calibration (future)
Track all predictions and compute Brier Score:
`BS = (1/n) * Σ(predicted - outcome)²`
Target: BS < 0.25

## Logging
- Log all prediction fields + timestamp
- Log sub-model outputs separately for analysis
