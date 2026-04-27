---
name: trading-bot-monitor
description: Monitor Huperliquis trading bot — check status, positions, equity, regime per asset, recent trades
---

# Trading Bot Monitor

You help monitor and manage a live Hyperliquid trading bot.

## Bot Architecture
- Entry: `implement/bot.py` (CLI) or `implement/dashboard.py` (web on port 8000)
- Strategy: `implement/strategy_v3.py` — BULL/FLAT/BEAR per-asset regime
- Risk: `implement/risk.py` — portfolio exposure, circuit breaker, anti-squeeze
- Assets: BTC, ETH, SOL, HYPE, ADA, XRP, XLM
- Exchange: Hyperliquid (perps)

## Commands

### /bot-status
Check if the bot process is running, what port dashboard is on, and last cycle time.
```bash
ps aux | grep -E "dashboard.py|bot.py" | grep -v grep
curl -s http://localhost:8000/balance 2>/dev/null
```

### /bot-start
Start the dashboard (which includes the bot loop).
```bash
cd implement && python3 dashboard.py &
```

### /bot-stop
Stop the bot gracefully.
```bash
curl -s -X POST http://localhost:8000/stop
```

### /positions
Query current open positions on Hyperliquid.
```bash
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"clearinghouseState","user":"WALLET_ADDRESS"}'
```

### /equity
Get current account equity.
```bash
curl -s http://localhost:8000/balance
```

## Guidelines
- Always check bot health before suggesting changes
- Never modify strategy parameters without explicit user confirmation
- Log all actions taken
