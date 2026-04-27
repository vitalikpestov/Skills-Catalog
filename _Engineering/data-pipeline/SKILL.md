---
name: data-pipeline
description: |
  Build data pipelines for prediction market trading bots — collect, clean, store, and serve
  market data from Polymarket APIs. Covers incremental extraction, schema design, snapshot
  scheduling, and historical data management. Use when implementing data collection, market
  snapshots, historical price storage, ETL pipelines, or database migrations for trading systems.
---

# Data Pipeline for Prediction Market Bots

## Overview

Design and implement data pipelines that collect market data from Polymarket (Gamma API, CLOB API, Data API), transform it, store in SQLite/PostgreSQL, and serve it to trading strategies, backtesting, and analytics.

## Pipeline Architecture

```
Sources               Extract           Transform         Load            Serve
──────               ───────           ─────────         ────            ─────
Gamma API ────┐                                      ┌── SQLite
  /markets    │   ┌───────────┐   ┌────────────┐     │   (dev)      ┌── Backtester
  /events     ├──>│ Extractor │──>│ Transformer│────>├── Postgres   ├── Predictor
CLOB API ─────┤   │ (incr/    │   │ (clean,    │     │   (prod)     ├── Risk Mgr
  /prices     │   │  snapshot)│   │  enrich,   │     └── JSON/CSV   └── Web UI
  /orderbook  │   └───────────┘   │  validate) │         (export)
Data API ─────┘                   └────────────┘
  /positions
```

## Schema Design

```sql
-- Market snapshots (collected every N minutes)
CREATE TABLE market_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT (datetime('now')),
    yes_price REAL NOT NULL,
    no_price REAL NOT NULL,
    spread REAL GENERATED ALWAYS AS (abs(yes_price - (1.0 - no_price))) STORED,
    volume_24h REAL,
    liquidity REAL,
    best_bid REAL,
    best_ask REAL,
    UNIQUE(market_id, timestamp)
);

CREATE INDEX idx_snapshots_market_time ON market_snapshots(market_id, timestamp);

-- Market metadata (updated daily)
CREATE TABLE markets (
    market_id TEXT PRIMARY KEY,
    event_id TEXT,
    question TEXT NOT NULL,
    category TEXT,
    end_date DATETIME,
    outcome TEXT,           -- NULL while active, YES/NO when resolved
    resolved_at DATETIME,
    first_seen DATETIME DEFAULT (datetime('now')),
    last_updated DATETIME DEFAULT (datetime('now'))
);

-- Trade history (from CLOB)
CREATE TABLE market_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    side TEXT NOT NULL,      -- BUY/SELL
    price REAL NOT NULL,
    size REAL NOT NULL,
    maker TEXT,
    taker TEXT
);
```

## Extraction Patterns

### Incremental Snapshots

```python
import sqlite3
import requests
from datetime import datetime

class MarketSnapshotCollector:
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)
        self.gamma_url = "https://gamma-api.polymarket.com"

    def collect_snapshot(self):
        """Fetch current prices for all active markets and store."""
        markets = requests.get(
            f"{self.gamma_url}/markets",
            params={"active": True, "limit": 200},
            timeout=30,
        ).json()

        rows = []
        for m in markets:
            rows.append((
                m["condition_id"],
                datetime.utcnow().isoformat(),
                float(m.get("outcomePrices", "[0.5,0.5]").strip("[]").split(",")[0]),
                float(m.get("outcomePrices", "[0.5,0.5]").strip("[]").split(",")[1]),
                float(m.get("volume24hr", 0)),
                float(m.get("liquidity", 0)),
                float(m.get("bestBid", 0)),
                float(m.get("bestAsk", 0)),
            ))

        self.db.executemany("""
            INSERT OR IGNORE INTO market_snapshots
            (market_id, timestamp, yes_price, no_price, volume_24h, liquidity, best_bid, best_ask)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, rows)
        self.db.commit()
        return len(rows)
```

### Scheduling

```python
import threading, time

def run_collector(db_path: str, interval_seconds: int = 300):
    """Background thread: snapshot every 5 minutes."""
    collector = MarketSnapshotCollector(db_path)
    while True:
        try:
            n = collector.collect_snapshot()
            print(f"[DataPipeline] Collected {n} snapshots")
        except Exception as e:
            print(f"[DataPipeline] Error: {e}")
        time.sleep(interval_seconds)

# Start as daemon thread
threading.Thread(target=run_collector, args=("data/markets.db",), daemon=True).start()
```

## Data Quality Checks

Run after each extraction:

```python
def validate_snapshot(db):
    """Basic quality checks on latest snapshot batch."""
    checks = {
        "price_range": "SELECT COUNT(*) FROM market_snapshots WHERE yes_price < 0 OR yes_price > 1",
        "null_prices": "SELECT COUNT(*) FROM market_snapshots WHERE yes_price IS NULL",
        "stale_data": """SELECT COUNT(*) FROM markets
                         WHERE last_updated < datetime('now', '-1 day')
                         AND outcome IS NULL""",
    }
    issues = {}
    for name, query in checks.items():
        count = db.execute(query).fetchone()[0]
        if count > 0:
            issues[name] = count
    return issues  # Empty dict = all good
```

## Query Patterns for Consumers

```python
# Price history for backtesting
def get_price_history(db, market_id: str, hours: int = 168):
    return db.execute("""
        SELECT timestamp, yes_price, volume_24h, liquidity
        FROM market_snapshots
        WHERE market_id = ? AND timestamp > datetime('now', ?)
        ORDER BY timestamp
    """, (market_id, f'-{hours} hours')).fetchall()

# Market resolution outcomes for Brier score
def get_resolved_markets(db, days: int = 30):
    return db.execute("""
        SELECT m.market_id, m.outcome,
               s.yes_price as final_price, s.timestamp
        FROM markets m
        JOIN market_snapshots s ON s.market_id = m.market_id
        WHERE m.resolved_at > datetime('now', ?)
        AND s.timestamp = (
            SELECT MAX(timestamp) FROM market_snapshots
            WHERE market_id = m.market_id AND timestamp < m.resolved_at
        )
    """, (f'-{days} days',)).fetchall()
```

## Migration Strategy

When moving from JSON files to SQLite:

1. Keep JSON exports as backup (`data/*.json`)
2. Run migration script to import existing `predictions_log.json` and `trades_log.json`
3. Update `web_app.py` endpoints to read from SQLite
4. Keep JSON write-through for backward compatibility during transition
