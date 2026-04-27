---
name: env-secrets-manager
description: Environment secrets management — .env safety, leak detection, key rotation for trading bot
---

# Environment Secrets Manager

## Required Secrets for Huperliquis Bot
```bash
# .env (NEVER commit)
HYPER_LIQUID_KEY=0x...          # Hyperliquid private key
WALLET_ADDRESS=0x...            # Public wallet address
OPENAI_API_KEY=sk-...           # GPT-4o for AI signals
SENTRY_DSN=https://...          # Error tracking
TELEGRAM_BOT_TOKEN=...          # Alert bot
TELEGRAM_CHAT_ID=...            # Alert destination
```

## Safety Rules
1. `.env` MUST be in `.gitignore` (already is)
2. Never print secrets in logs — mask with `key[:8]...`
3. Never pass secrets as CLI arguments (visible in `ps aux`)
4. Use `os.getenv()` not hardcoded strings

## Leak Detection
```bash
# Check for leaked secrets in git history
git log --all -p | grep -iE "(private.?key|secret|password|sk-|0x[a-f0-9]{64})" | head -20

# Check current staged files
git diff --cached | grep -iE "(sk-|0x[a-f0-9]{64}|HYPER_LIQUID)"
```

## Key Rotation Checklist
1. Generate new Hyperliquid key
2. Update .env on all environments (local, VPS)
3. Restart bot: `docker compose restart bot`
4. Verify positions synced: check dashboard
5. Revoke old key if possible

## Guidelines
- Rotate keys every 90 days
- Use separate keys for testnet and mainnet
- Keep .env.example with placeholder values (committed)
- For VPS: use Docker secrets or environment variables, not .env file
