---
name: hyperliquid-api
description: Hyperliquid exchange API reference — REST endpoints, WebSocket subscriptions, order types, rate limits
---

# Hyperliquid API Reference

## Base URLs
- REST: `https://api.hyperliquid.xyz`
- WebSocket: `wss://api.hyperliquid.xyz/ws`
- Testnet: `https://api.hyperliquid-testnet.xyz`

## Key REST Endpoints (POST /info)

### Market Data
```json
{"type": "meta"}                              // All perpetual markets metadata
{"type": "metaAndAssetCtxs"}                  // Markets + current funding, OI, prices
{"type": "allMids"}                           // All mid prices
{"type": "candleSnapshot", "req": {           // OHLCV candles
  "coin": "BTC", "interval": "1h",
  "startTime": 1700000000000, "endTime": 1700100000000
}}
{"type": "l2Book", "coin": "BTC"}             // L2 orderbook
```

### Account Data
```json
{"type": "clearinghouseState", "user": "0x..."} // Positions, margin, equity
{"type": "openOrders", "user": "0x..."}          // Open orders
{"type": "userFills", "user": "0x..."}           // Trade fills
{"type": "userFunding", "user": "0x..."}         // Funding payments
{"type": "referral", "user": "0x..."}            // Referral info
```

## Order Placement (POST /exchange)
```json
{
  "action": {
    "type": "order",
    "orders": [{
      "a": 0,              // asset index (0=BTC, 1=ETH, ...)
      "b": true,           // true=buy, false=sell
      "p": "87000",        // price (string)
      "s": "0.001",        // size (string)
      "r": false,          // reduce_only
      "t": {"limit": {"tif": "Gtc"}}  // Good till cancelled
    }],
    "grouping": "na"
  },
  "nonce": 1700000000000,
  "signature": {"r": "...", "s": "...", "v": 27},
  "vaultAddress": null
}
```

### Order Types
- `{"limit": {"tif": "Gtc"}}` — Good till cancelled
- `{"limit": {"tif": "Ioc"}}` — Immediate or cancel
- `{"limit": {"tif": "Alo"}}` — Add liquidity only (maker)
- `{"trigger": {"triggerPx": "85000", "isMarket": true, "tpsl": "sl"}}` — Stop loss

## WebSocket Subscriptions
```json
{"method": "subscribe", "subscription": {"type": "trades", "coin": "BTC"}}
{"method": "subscribe", "subscription": {"type": "l2Book", "coin": "BTC"}}
{"method": "subscribe", "subscription": {"type": "candle", "coin": "BTC", "interval": "1m"}}
{"method": "subscribe", "subscription": {"type": "orderUpdates", "user": "0x..."}}
{"method": "subscribe", "subscription": {"type": "userFills", "user": "0x..."}}
```

## Rate Limits
- REST: 1200 requests/minute per IP
- WebSocket: 100 subscriptions per connection
- Orders: 100 per 10 seconds per user

## Python SDK
```python
from hyperliquid.info import Info
from hyperliquid.exchange import Exchange
from hyperliquid.utils import constants

info = Info(constants.MAINNET_API_URL, skip_ws=True)
exchange = Exchange(account, constants.MAINNET_API_URL)
```

## Asset Indices (partial)
BTC=0, ETH=1, ... (use `meta` endpoint to get full mapping)

## Guidelines
- Always use string types for price and size in orders
- Nonce must be current timestamp in ms
- Signature uses EIP-712 typed data
- Testnet has same API but different contracts
- Check `funding` field in metaAndAssetCtxs before shorting
