---
name: python-trading-patterns
description: Python patterns for trading bots — async execution, retry logic, position sizing, risk calculations, data pipelines
---

# Python Trading Bot Patterns

## Pattern: Async Multi-Asset Fetch (7 assets parallel)
```python
import asyncio
import aiohttp

async def fetch_candles(session, symbol, start_ms, end_ms):
    async with session.post('https://api.hyperliquid.xyz/info', json={
        'type': 'candleSnapshot',
        'req': {'coin': symbol, 'interval': '1h',
                'startTime': start_ms, 'endTime': end_ms}
    }) as resp:
        return symbol, await resp.json()

async def fetch_all_assets(symbols, start_ms, end_ms):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_candles(session, s, start_ms, end_ms) for s in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {sym: data for sym, data in results if not isinstance(data, Exception)}
```

## Pattern: Retry with Exponential Backoff
```python
import asyncio
from functools import wraps

def retry(max_attempts=3, base_delay=1.0, max_delay=30.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3)
async def place_order(symbol, side, size, price):
    ...
```

## Pattern: Graceful Shutdown
```python
import signal

class Bot:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, signum, frame):
        self.running = False
        # Cancel open orders, close positions if needed
        print("Shutting down gracefully...")
```

## Pattern: Position Size with Kelly Criterion
```python
def kelly_size(win_rate, avg_win, avg_loss, fraction=0.25):
    """Quarter-Kelly for conservative sizing."""
    if avg_loss == 0:
        return 0
    b = avg_win / avg_loss  # win/loss ratio
    q = 1 - win_rate
    kelly = (win_rate * b - q) / b
    return max(0, kelly * fraction)
```

## Pattern: Thread-Safe State Updates
```python
import threading

class AtomicState:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}

    def update(self, key, value):
        with self._lock:
            self._data[key] = value

    def get(self, key, default=None):
        with self._lock:
            return self._data.get(key, default)
```

## Pattern: Rate Limiter
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls, period_seconds):
        self.max_calls = max_calls
        self.period = period_seconds
        self.calls = deque()

    def wait_if_needed(self):
        now = time.time()
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()
        if len(self.calls) >= self.max_calls:
            sleep_time = self.calls[0] + self.period - now
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.calls.append(time.time())

# Usage: max 1200 requests per 60 seconds (Hyperliquid limit)
limiter = RateLimiter(1200, 60)
```

## Guidelines
- Always use asyncio for multi-asset operations (7x speedup)
- Never block the event loop with time.sleep() in async code
- Use decimal.Decimal for financial calculations when precision matters
- Log every order placement and fill for audit trail
- Keep state immutable where possible — create new objects instead of mutating
