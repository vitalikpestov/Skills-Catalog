---
name: ci-cd-pipeline
description: GitHub Actions CI/CD for trading bot — lint, test, build Docker, deploy to VPS, health check
---

# CI/CD Pipeline for Huperliquis Bot

## GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy Trading Bot

on:
  push:
    branches: [main]
    paths:
      - 'implement/**'
      - 'Dockerfile'
      - 'docker-compose.yml'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.13' }
      - run: pip install -r requirements.txt
      - run: python -m pytest backtest/ -x --timeout=120

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /opt/huperliquis-bot
            git pull origin main
            docker compose down
            docker compose up -d --build
            sleep 10
            curl -sf http://localhost:8000/ || exit 1
            echo "Deploy OK"
```

## Pre-deploy Checklist
- All backtest files pass without error
- No .env or secrets in commit
- strategy_v3.py imports cleanly
- Dashboard responds on :8000

## Guidelines
- Never deploy on weekends (low liquidity)
- Always run backtests before deploy
- Keep rollback plan: `git revert HEAD && docker compose up -d --build`
- Monitor first 1 hour after deploy via Telegram alerts
