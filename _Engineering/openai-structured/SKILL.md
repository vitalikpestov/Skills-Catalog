---
name: openai-structured
description: OpenAI GPT-4o patterns for trading bot — structured outputs, function calling, market analysis, trade review
---

# OpenAI Integration for Trading Bot

## Setup
```python
from openai import OpenAI
import json, os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

## Pattern: Structured Market Summary
```python
from pydantic import BaseModel
from typing import List, Literal

class MarketSummary(BaseModel):
    overall_sentiment: Literal["bullish", "bearish", "neutral"]
    risk_level: Literal["low", "medium", "high"]
    key_observations: List[str]  # 3-5 bullets
    assets_to_watch: List[str]

def get_market_summary(market_data: dict) -> MarketSummary:
    response = client.responses.parse(
        model="gpt-4o-mini",  # cheaper for summaries
        input=[{
            "role": "system",
            "content": "You are a quant analyst. Analyze the market data and provide a structured summary. Be concise."
        }, {
            "role": "user",
            "content": f"Market state:\n{json.dumps(market_data, indent=2)}"
        }],
        text_format=MarketSummary,
    )
    return response.output_parsed
```

## Pattern: Trade Review
```python
class TradeReview(BaseModel):
    grade: Literal["A", "B", "C", "D", "F"]
    what_went_well: str
    what_could_improve: str
    lesson: str

def review_trade(trade_data: dict) -> TradeReview:
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[{
            "role": "system",
            "content": "You are a trading coach. Review this completed trade and grade it."
        }, {
            "role": "user",
            "content": f"Trade:\n{json.dumps(trade_data, indent=2)}"
        }],
        text_format=TradeReview,
    )
    return response.output_parsed
```

## Pattern: Function Calling (bot queries)
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_portfolio_state",
        "description": "Get current portfolio: equity, open positions, daily PnL",
        "parameters": {"type": "object", "properties": {}}
    }
}, {
    "type": "function",
    "function": {
        "name": "get_asset_indicators",
        "description": "Get current indicators for an asset",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "enum": ["BTC","ETH","SOL","HYPE","ADA","XRP","XLM"]}
            },
            "required": ["symbol"]
        }
    }
}]
```

## Cost Control
```python
# Model selection by task:
# gpt-4o-mini  → Market summary, trade review (cheap, fast)
# gpt-4o       → Complex analysis requiring reasoning (rare)

# Rate limiting: max 10 calls/hour
# Caching: market summary cached 4 hours
# Batch API: end-of-day review of all trades (50% cheaper)
```

## Guidelines
- Always use structured outputs (Pydantic models) — never parse free text
- Use gpt-4o-mini by default, gpt-4o only when mini fails
- Fail-open: if API is down, bot continues without AI
- Never let AI make trading decisions — advisory only
- Log every AI call with input/output for audit
- Set timeout=10s on all API calls
