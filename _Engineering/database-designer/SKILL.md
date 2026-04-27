---
name: database-designer
description: PostgreSQL/Supabase schema for trading bot — trades, equity, regimes, positions, alerts
---

# Database Schema for Huperliquis Bot

## When to migrate from CSV to DB
- Trade count > 500
- Need real-time queries from dashboard
- Multiple bot instances sharing data
- Want Grafana direct DB connection

## Schema (Supabase/PostgreSQL)

```sql
-- Trade journal
CREATE TABLE trades (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('LONG', 'SHORT')),
    signal_type TEXT NOT NULL,
    regime TEXT NOT NULL CHECK (regime IN ('BULL', 'FLAT', 'BEAR')),
    entry_price NUMERIC(20, 8) NOT NULL,
    avg_entry NUMERIC(20, 8),
    exit_price NUMERIC(20, 8),
    size NUMERIC(20, 8) NOT NULL,
    pnl_usd NUMERIC(12, 2),
    pnl_pct NUMERIC(8, 4),
    fees_usd NUMERIC(8, 4),
    dca_levels_filled INT DEFAULT 1,
    exit_type TEXT CHECK (exit_type IN ('SL', 'TP', 'TIME', 'EMERGENCY', 'MANUAL')),
    entry_at TIMESTAMPTZ NOT NULL,
    exit_at TIMESTAMPTZ,
    duration_hours NUMERIC(8, 2),
    ai_review TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_trades_symbol ON trades(symbol);
CREATE INDEX idx_trades_entry_at ON trades(entry_at);
CREATE INDEX idx_trades_regime ON trades(regime);

-- Equity snapshots (every cycle)
CREATE TABLE equity_snapshots (
    id BIGSERIAL PRIMARY KEY,
    equity NUMERIC(12, 2) NOT NULL,
    drawdown_pct NUMERIC(8, 4),
    open_positions INT DEFAULT 0,
    daily_pnl NUMERIC(12, 2),
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_equity_recorded ON equity_snapshots(recorded_at);

-- Regime transitions per asset
CREATE TABLE regime_transitions (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    old_regime TEXT NOT NULL,
    new_regime TEXT NOT NULL,
    adx NUMERIC(8, 2),
    rsi NUMERIC(8, 2),
    ema50 NUMERIC(20, 8),
    ema200 NUMERIC(20, 8),
    transitioned_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_regime_symbol_time ON regime_transitions(symbol, transitioned_at);

-- Bot events (errors, circuit breaker, restarts)
CREATE TABLE bot_events (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    symbol TEXT,
    message TEXT,
    severity TEXT DEFAULT 'info' CHECK (severity IN ('info', 'warning', 'error', 'critical')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Query Patterns
```sql
-- Win rate by regime
SELECT regime, COUNT(*) as trades,
       ROUND(100.0 * SUM(CASE WHEN pnl_usd > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM trades GROUP BY regime;

-- Monthly equity curve
SELECT DATE_TRUNC('month', recorded_at) as month,
       MAX(equity) as peak, MIN(equity) as trough
FROM equity_snapshots GROUP BY month ORDER BY month;

-- Best/worst assets
SELECT symbol, SUM(pnl_usd) as total_pnl, COUNT(*) as trades
FROM trades GROUP BY symbol ORDER BY total_pnl DESC;
```

## Guidelines
- Record equity snapshot every bot cycle (60s)
- Partition equity_snapshots by month for performance
- Use NUMERIC not FLOAT for financial data
- Always include timezone (TIMESTAMPTZ)
- Keep CSV export as backup: `COPY trades TO '/tmp/trades.csv' CSV HEADER`
