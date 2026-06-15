---
name: asomobile-api
description: >
  When the user wants to pull live App Store keyword data via ASOMobile API —
  traffic volume, KEI, competition index, ASA presence, top-ranking apps,
  autocomplete suggestions. Use for keyword research, competitor keyword footprints,
  and app ranking lookups. Trigger phrases: "pull ASOMobile data", "check keyword traffic",
  "ASOMobile keyword check", "что в ASOMobile по ключевику", "keyword-check".
metadata:
  version: 1.0.0
  updated: 2026-05-14
  author: App Store Optimizer
---

# ASOMobile API Skill

Pulls live App Store keyword intelligence from ASOMobile's public REST API.

---

## Setup

**Token:** stored in `.env` or Supabase secrets as `ASOMOBILE_TOKEN` — never hardcode in files.

**Docs:** https://asomobile.apidog.io/

**Base URL:** `https://app.asomobile.net/asomobile-public-api`

**Auth:** `Authorization: Bearer <token>`  
⚠️ **Важно:** `Bearer`, не `Token` — API возвращает 401 при `Token` схеме.

**SSL note:** API uses a self-signed cert chain — always bypass SSL verification in Python scripts:
```python
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
# pass context=ctx to urlopen()
```

**Flow:** All endpoints are async (ticket-based):
1. `GET /endpoint/?params` → `{"code": 201, "data": {"ticket_id": 12345}}`
2. `GET /endpoint/result?ticket_id=12345` → poll until `"code": 200`
   - `404` while processing = "not ready yet", keep polling
   - `200` = data ready

---

## Available Endpoints

| Group | Request | Result |
|-------|---------|--------|
| Keyword Check | `GET /keyword-check/` | `GET /keyword-check/result` |
| App Keywords | `GET /app-keywords/` | `GET /app-keywords/result` |
| App Keywords (multi-country) | `POST /app-keywords/multi-country/` | `GET /app-keywords/multi-country/result` |
| Keyword Monitor | `GET /keyword-monitor/` | `GET /keyword-monitor/result` |
| Keyword Rank | `GET /keyword-rank/` | `GET /keyword-rank/result` |
| App Profile | `GET /app-profile/` | `GET /app-profile/result` |
| App Competitors | `GET /app-competitors/` | `GET /app-competitors/result` |
| App Ranking | `GET /app-ranking/` | `GET /app-ranking/result` |
| Keyword Suggest | `POST /keyword-suggest/` | `GET /keyword-suggest/result` |
| Organic Downloads | `GET /organic-downloads/` | `GET /organic-downloads/result` |

---

## Endpoint Details

### Keyword Check — traffic, difficulty, top apps for a keyword

```
GET /keyword-check/?platform=IOS&ios_device=IPHONE&country=US&keyword=pill+reminder
```

**Params:**
- `platform`: `IOS` | `ANDROID`
- `ios_device`: `IPHONE` | `IPAD` (required for IOS)
- `country`: ISO 3166-2 code (`US`, `RU`, `DE`, `GB`…)
- `keyword`: search query (one keyword per request)

**Result fields:**
| Field | Description |
|-------|-------------|
| `traffic.value` | Relative search volume (0–1000+). Higher = more searches |
| `kei.value` | Keyword Effectiveness Index (0–100). Higher = easier to rank profitably |
| `ci.value` | Competition Index (0–100). Higher = harder to rank |
| `asa` | Apple Search Ads advertiser count. Low = uncrowded paid market |
| `apps_count` | Total apps indexed for this keyword |
| `suggestions[]` | Autocomplete suggestions (related keywords) |
| `top_apps[]` | App IDs ranked #1–28 for this keyword |

**Interpreting traffic:**
| Range | Meaning |
|-------|---------|
| 500+ | High volume — competitive, worth fighting for |
| 200–499 | Medium — good balance traffic/competition |
| 50–199 | Low-medium — niche, easier to rank |
| <50 | Very low — micro-niche or zero data |

### App Keywords — full keyword footprint of a competitor app

```
GET /app-keywords/?platform=IOS&country=US&app_id=573916946
```

**Params:**
- `app_id`: iTunes numeric app ID

**Result:** list of keywords the app ranks for + positions.

### Keyword Rank — who ranks where for a keyword

```
GET /keyword-rank/?platform=IOS&ios_device=IPHONE&country=US&keyword=pill+reminder
```

**Result:** ranked list of apps with positions.

---

## Reusable Python Script

```python
#!/usr/bin/env python3
"""
ASOMobile keyword check — reusable script.
Usage: set TOKEN and call keyword_check("your keyword")
"""
import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import time
import os

TOKEN = os.environ.get("ASOMOBILE_TOKEN", "")  # set in .env
BASE = "https://app.asomobile.net/asomobile-public-api"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def _get(path: str) -> dict:
    req = urllib.request.Request(f"{BASE}{path}", headers=HEADERS)
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
        return json.loads(r.read())


def _poll(endpoint_result: str, ticket_id: int, tries: int = 30, delay: int = 6) -> dict | None:
    for i in range(tries):
        time.sleep(delay)
        try:
            r = _get(f"{endpoint_result}?ticket_id={ticket_id}")
            if r.get("code") == 200:
                return r.get("data", {})
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise  # unexpected error
    return None  # timeout


def keyword_check(keyword: str, country: str = "US") -> dict | None:
    """Pull traffic, KEI, CI, ASA, suggestions, top apps for one keyword."""
    params = urllib.parse.urlencode({
        "platform": "IOS",
        "ios_device": "IPHONE",
        "country": country,
        "keyword": keyword,
    })
    resp = _get(f"/keyword-check/?{params}")
    ticket_id = resp.get("data", {}).get("ticket_id")
    if not ticket_id:
        return None
    time.sleep(10)  # initial wait before first poll
    return _poll("/keyword-check/result", ticket_id)


def app_keywords(app_id: str, country: str = "US") -> dict | None:
    """Pull full keyword footprint for a competitor app."""
    params = urllib.parse.urlencode({
        "platform": "IOS",
        "country": country,
        "app_id": app_id,
    })
    resp = _get(f"/app-keywords/?{params}")
    ticket_id = resp.get("data", {}).get("ticket_id")
    if not ticket_id:
        return None
    time.sleep(10)
    return _poll("/app-keywords/result", ticket_id)


def print_keyword_summary(keyword: str, data: dict | None):
    if not data:
        print(f"❌ {keyword}: no data (keyword not indexed or zero traffic)")
        return
    traffic = data.get("traffic", {}).get("value", 0)
    kei = data.get("kei", {}).get("value", 0)
    ci = data.get("ci", {}).get("value", 0)
    asa = data.get("asa", "?")
    apps = data.get("apps_count", "?")
    sugg = data.get("suggestions", [])[:5]
    top = [a["app_id"] for a in data.get("top_apps", [])[:5]]
    print(f"✅ {keyword}")
    print(f"   traffic={traffic:.0f}  KEI={kei:.0f}  CI={ci:.0f}  ASA={asa}  apps={apps}")
    print(f"   suggestions: {sugg}")
    print(f"   top 5 app IDs: {top}")


# --- Example usage ---
if __name__ == "__main__":
    keywords = ["pill reminder", "medication tracker"]
    for kw in keywords:
        data = keyword_check(kw)
        print_keyword_summary(kw, data)
        time.sleep(5)  # avoid rate limiting between requests
```

---

## Known Behaviors & Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| 404 on `/keyword-check/result` after 201 | Keyword not in ASOMobile index (too new, zero traffic, or rare) | Treat as "no data" — keyword probably zero-traffic |
| 404 on request itself | Rate limiting (burst > ~4 req/min) | Wait 30–60s between batches |
| HTTP 500 on all endpoints | ASOMobile server down | Check status, retry in 1–2h |
| SSL CERTIFICATE_VERIFY_FAILED | Self-signed cert in chain | Always use `ctx.verify_mode = ssl.CERT_NONE` |
| Only first of batch returns data | Don't batch requests — one at a time, sequential | One keyword → wait 10s → poll → next keyword |

**Critical rule:** Never fire multiple keyword requests simultaneously. Send one, poll to completion, then send next.

---

## Workflow: New App Keyword Research

```
1. SEED — identify 5–10 seed keywords (describe what the app does)
2. CHECK each via /keyword-check/:
   - traffic > 100 + CI < 40 + KEI > 40 = 🟢 opportunity
   - traffic > 100 + CI > 70 = 🔴 wall (established competition)
   - no data = ~0 traffic or too niche
3. EXPAND — use `suggestions[]` from results to find related keywords
4. COMPETITOR footprint — run /app-keywords/ on top 2–3 competitors
5. MAP — build keyword battle map (who owns what, where are gaps)
6. METADATA — assign winners to: App Name, Subtitle, Keywords field
```

## Workflow: Competitor Keyword Audit

```
1. Get competitor app ID from App Store URL or iTunes search
2. Run app_keywords(app_id) → get full keyword list
3. Cross-reference against your target keywords
4. Find: keywords they rank for that you don't (threats)
5. Find: keywords they miss entirely (your blue ocean)
```

---

## Quick Reference — Scoring Matrix

```
FIGHT NOW (blue ocean):
  traffic 50–200 + CI < 20 + ASA < 10 → own it at launch

FIGHT M3+ (when 500+ reviews):
  traffic 200–500 + CI 20–50 → plan for month 3

DO NOT FIGHT at launch:
  traffic 400+ + CI > 60 → top apps are fortified
```

---

## Related Skills

- `keyword-research` — keyword strategy from research to metadata
- `competitor-analysis` — full competitor deep dive
- `metadata-optimization` — apply keyword data to App Name / Subtitle / KF
- `aso-audit` — full 10-axis ASO health check
- `seasonal-aso` — seasonal keyword swaps calendar
