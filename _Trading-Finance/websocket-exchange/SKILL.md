---
name: websocket-exchange
description: WebSocket patterns for real-time exchange data — Hyperliquid price feeds, orderbook streaming, reconnection handling
---

# WebSocket Exchange Patterns

Patterns for connecting to Hyperliquid WebSocket feeds for real-time data.
Use `websockets` library (asyncio-based, v14+).

## Hyperliquid WebSocket Endpoint
```
wss://api.hyperliquid.xyz/ws
```

## Pattern: Subscribe to Real-time Trades
```python
import asyncio
import json
import websockets

async def stream_trades(symbol: str, callback):
    uri = "wss://api.hyperliquid.xyz/ws"

    async for ws in websockets.connect(uri):
        try:
            # Subscribe
            await ws.send(json.dumps({
                "method": "subscribe",
                "subscription": {"type": "trades", "coin": symbol}
            }))

            async for msg in ws:
                data = json.loads(msg)
                if data.get("channel") == "trades":
                    for trade in data.get("data", []):
                        await callback(symbol, trade)

        except websockets.ConnectionClosed:
            continue  # auto-reconnect via `async for`
```

## Pattern: Multi-Asset Parallel Streams
```python
async def stream_all(symbols: list, callback):
    """Connect to all symbols in parallel."""
    tasks = [stream_trades(sym, callback) for sym in symbols]
    await asyncio.gather(*tasks)

# Usage
ASSETS = ['BTC', 'ETH', 'SOL', 'HYPE', 'ADA', 'XRP', 'XLM']
asyncio.run(stream_all(ASSETS, handle_trade))
```

## Pattern: Reconnection with Backoff
```python
import websockets
from websockets.asyncio.client import connect

async def robust_stream(symbol, callback):
    backoff = 1
    while True:
        try:
            async with connect("wss://api.hyperliquid.xyz/ws") as ws:
                backoff = 1  # reset on success
                await ws.send(json.dumps({
                    "method": "subscribe",
                    "subscription": {"type": "trades", "coin": symbol}
                }))
                async for msg in ws:
                    data = json.loads(msg)
                    await callback(symbol, data)
        except (websockets.ConnectionClosed, OSError):
            await asyncio.sleep(min(backoff, 30))
            backoff *= 2
```

## Pattern: OrderBook Streaming
```python
await ws.send(json.dumps({
    "method": "subscribe",
    "subscription": {"type": "l2Book", "coin": symbol}
}))
```

## Pattern: User Fills (requires auth)
```python
await ws.send(json.dumps({
    "method": "subscribe",
    "subscription": {"type": "userFills", "user": wallet_address}
}))
```

## Guidelines
- Always use `websockets.asyncio` (not legacy `websockets.connect`)
- Use `async for ws in connect(uri)` for auto-reconnect
- Keep heartbeat alive — Hyperliquid drops idle connections after 30s
- Parse messages quickly — don't block the event loop
- For 7 assets: one connection with multiple subscriptions is better than 7 connections
