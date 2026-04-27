---
name: alerting-system
description: |
  Build and configure trading alert systems for prediction market bots.
  Routes price, position, drawdown, and whale alerts to Telegram, email, or webhooks.
  Use when implementing alerts, notifications, price triggers, drawdown warnings,
  position monitoring alerts, or Telegram bot notifications for trading systems.
---

# Alerting System for Trading Bots

## Overview

Design and implement multi-channel alerting for prediction market trading bots. Covers alert rule definition, threshold configuration, notification routing (Telegram, email, webhooks), deduplication, cooldown, and escalation.

## Alert Categories

| Category | Triggers | Priority |
|----------|----------|----------|
| **Price** | Threshold cross, % change, spread widening | Medium |
| **Position** | PnL target hit, stop-loss approach, expiry warning | High |
| **Risk** | Drawdown limit, exposure limit, kill switch | Critical |
| **Whale** | Large trade detected, copy-trade signal | Medium |
| **System** | API error, connection lost, bot crash, stale data | Critical |
| **Signal** | New trade signal, exit recommendation, regime change | Low |

## Architecture

```
Alert Sources          Router              Channels
─────────────        ─────────           ──────────
price_monitor ──┐                     ┌── Telegram
position_watch ─┤    ┌───────────┐    ├── Email
risk_checker ───┼───>│ AlertRouter│───>├── Webhook
whale_watcher ──┤    │ (dedup,   │    ├── Console log
system_health ──┤    │  cooldown,│    └── Web UI toast
signal_engine ──┘    │  escalate)│
                     └───────────┘
```

## Implementation Pattern

```python
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

class AlertPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Alert:
    category: str
    message: str
    priority: AlertPriority
    market_id: str | None = None
    data: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

class AlertRouter:
    def __init__(self, config: dict):
        self.channels = config["channels"]  # {priority: [channel_list]}
        self.cooldowns = config.get("cooldowns", {})  # {category: seconds}
        self._last_sent: dict[str, datetime] = {}

    def send(self, alert: Alert) -> bool:
        key = f"{alert.category}:{alert.market_id or 'global'}"
        cooldown = self.cooldowns.get(alert.category, 0)
        if key in self._last_sent:
            if datetime.utcnow() - self._last_sent[key] < timedelta(seconds=cooldown):
                return False  # Deduplicated

        channels = self.channels.get(alert.priority.value, [])
        for channel in channels:
            channel.deliver(alert)
        self._last_sent[key] = datetime.utcnow()
        return True
```

## Telegram Channel

```python
import requests

class TelegramChannel:
    def __init__(self, bot_token: str, chat_id: str):
        self.url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        self.chat_id = chat_id

    def deliver(self, alert: Alert):
        icon = {"critical": "🚨", "high": "⚠️", "medium": "📊", "low": "ℹ️"}
        text = f"{icon.get(alert.priority.value, '•')} *{alert.category.upper()}*\n{alert.message}"
        requests.post(self.url, json={
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "Markdown",
        }, timeout=10)
```

## Configuration

```yaml
alerting:
  channels:
    critical: [telegram, email, console]
    high: [telegram, console]
    medium: [telegram]
    low: [console]

  cooldowns:
    price: 300        # 5 min between same-market price alerts
    position: 60      # 1 min for position alerts
    risk: 0           # No cooldown for risk alerts (always send)
    whale: 120        # 2 min for whale alerts
    system: 30        # 30s for system alerts
    signal: 600       # 10 min for signal alerts

  thresholds:
    price_change_pct: 5.0       # Alert on 5%+ price move
    drawdown_warn_pct: 10.0     # Warn at 10% drawdown
    drawdown_critical_pct: 15.0 # Critical at 15%
    position_pnl_target: 20.0   # Alert on +20% PnL
    expiry_hours: 24            # Alert 24h before expiry
    spread_widening_pct: 3.0    # Alert on 3%+ spread

  telegram:
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    chat_id: "${TELEGRAM_CHAT_ID}"
```

## Integration with Existing Bot

```python
# In web_app.py or exit_engine.py:
alert_router.send(Alert(
    category="position",
    message=f"🎯 Trailing stop triggered for {market_name}\nPnL: {pnl:+.1f}%",
    priority=AlertPriority.HIGH,
    market_id=market_id,
    data={"pnl": pnl, "action": "sell"},
))
```

## Alert Rule Examples

- **Price cross**: `abs(current_price - entry_price) / entry_price > threshold`
- **Drawdown**: `(peak_equity - current_equity) / peak_equity > threshold`
- **Stale data**: `datetime.utcnow() - last_update > timedelta(minutes=5)`
- **Whale copy**: `whale_trade.size > min_size and whale_score > min_score`
- **Expiry warning**: `market.expiry - datetime.utcnow() < timedelta(hours=24)`
