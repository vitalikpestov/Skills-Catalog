---
name: grafana-trading
description: Grafana + Prometheus setup for trading bot monitoring — equity curves, trade metrics, regime tracking, alerting to Telegram
---

# Grafana Trading Bot Monitoring

## Architecture
```
Bot (Python) → prometheus_client → Prometheus → Grafana → Telegram alerts
Bot (Python) → JSON log files    → Loki       → Grafana log explorer
```

## Docker Compose Stack
```yaml
version: '3.8'
services:
  bot:
    build: ./implement
    env_file: .env
    restart: unless-stopped
    ports:
      - "8000:8000"   # dashboard
      - "9090:9090"   # prometheus metrics endpoint

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9091:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"

volumes:
  grafana-data:
```

## Bot Metrics (prometheus_client)
```python
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Metrics to expose
equity_gauge = Gauge('bot_equity_usd', 'Current equity in USD')
drawdown_gauge = Gauge('bot_drawdown_pct', 'Current drawdown percentage')
trades_total = Counter('bot_trades_total', 'Total trades', ['symbol', 'side', 'result'])
pnl_histogram = Histogram('bot_trade_pnl_pct', 'Trade PnL distribution', buckets=[-5,-3,-1,0,1,3,5,10])
regime_gauge = Gauge('bot_regime', 'Current regime per asset', ['symbol', 'regime'])
position_gauge = Gauge('bot_position_size', 'Position size', ['symbol'])
api_latency = Histogram('bot_api_latency_seconds', 'Hyperliquid API latency')
errors_total = Counter('bot_errors_total', 'Total errors', ['type'])

# Start metrics server
start_http_server(9090)
```

## Key Grafana Dashboards

### 1. Equity & Performance
- Equity curve (line, real-time)
- Daily PnL (bar chart, green/red)
- Drawdown gauge (threshold at 3%, 5%, 10%)
- Win rate (stat panel)
- Sharpe ratio (calculated)

### 2. Asset Overview
- 7 panels, one per asset
- Current price, regime (BULL/FLAT/BEAR color), position status
- Trade count per asset

### 3. Risk Monitor
- Portfolio exposure % (gauge, max 60%)
- Per-asset exposure
- Consecutive losses counter
- Circuit breaker status
- API error rate

## Grafana Alerts → Telegram
```
Alert rules:
- Equity drops > 3% in 24h → Telegram
- API errors > 5 in 10min → Telegram
- Position drawdown > 8% → Telegram
- No trades in 48h (bot may be stuck) → Telegram
- Circuit breaker triggered → Telegram
```

## Prometheus Config
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'trading-bot'
    static_configs:
      - targets: ['bot:9090']
```

## Guidelines
- Scrape interval 15s is enough for a 60s bot cycle
- Keep 30 days of metrics retention
- Use Grafana provisioning for reproducible dashboards
- Export dashboard JSON to version control
