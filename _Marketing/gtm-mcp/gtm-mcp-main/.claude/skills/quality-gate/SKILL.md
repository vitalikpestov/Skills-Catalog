# Quality Gate Skill

Define checkpoints that must PASS before pipeline advances. Prevents wasting credits on bad data.

## When to Use

- **Pre-flight**: Before pipeline starts (Checkpoint 0)
- After gathering phase (Checkpoint 1)
- After classification phase (Checkpoint 2)
- After people extraction (Checkpoint 3)
- When user asks "is this enough?" or "should I continue?"

## Checkpoint 0: Pre-Flight Validation

**Trigger**: Before ANY Apollo credits are spent. Called by `/launch` command.

ALL of these must be true before pipeline starts:

| Field | Check | If Missing |
|-------|-------|------------|
| offer_extracted | offer.yaml exists in project | ASK: "What's your website or what do you sell?" |
| segments | non-empty list | ASK: "What type of companies should I search for?" |
| geo | non-empty list | ASK: "Which locations should I target?" |
| email_accounts | non-empty list of SmartLead account IDs | ASK: "Which email accounts to use?" |
| sequence | GOD_SEQUENCE or user-provided steps | USE DEFAULT: GOD_SEQUENCE |
| kpi | target_contacts + contacts_per_company set | USE DEFAULT: 100 contacts, 3/company |
| cost_approved | user confirmed cost estimate | SHOW estimate, wait for "proceed" |

**Result**: `PASS` (all resolved) or `BLOCK` (report which field is missing).

**Rule**: Ask ONE missing field at a time. Never ask multiple questions in one response.

## Checkpoint 1: Post-Gather

**Trigger**: After Apollo search + blacklist filtering

| Metric | Threshold | Action if Failed |
|--------|-----------|------------------|
| Total companies gathered | >= 20 | WARN: "Only {N} companies found. Consider broader filters." |
| Blacklist rejection rate | < 50% | WARN: "High blacklist rate ({N}%). Many duplicates from previous campaigns." |
| Apollo pages returned | >= 1 with results | FAIL: "No results from Apollo. Check filters." |

**Output**: PASS or WARN with details.

**On WARN**: Present to user with options:
1. Continue anyway (accept lower quality)
2. Adjust filters (broader keywords, different location)
3. Stop pipeline

## Checkpoint 2: Post-Classification

**Trigger**: After all companies scraped + classified

| Metric | Threshold | Action if Failed |
|--------|-----------|------------------|
| Targets found | >= 10 | WARN: "Only {N} targets. Need ~34 for 100 contacts." |
| Target rate | > 15% | WARN: "Low target rate ({N}%). Filters may be too broad." |
| Scrape success rate | > 60% | WARN: "Many scrape failures ({N}%). May need proxy." |
| High confidence (>0.7) | > 50% of targets | WARN: "Low confidence scores. Consider exploration." |

**Additional checks**:
- Segment distribution: Are targets spread across segments or concentrated?
- segments_sufficient: Need targets in at least 1 segment
- contacts_estimate: targets * contacts_per_company (default 3)
- suggest_exploration: true if targets exist but rate < 50%

**Output format**:
```json
{
  "gate": "PASS" | "WARN",
  "targets_found": 45,
  "target_rate": 0.36,
  "segment_distribution": {"PAYMENTS": 20, "LENDING": 15, "BAAS": 10},
  "contacts_estimate": 135,
  "targets_sufficient": true,
  "suggest_exploration": false,
  "warnings": ["Target rate below 50%, exploration may improve accuracy"]
}
```

**On WARN**: Present next steps:
1. Approve → proceed to people extraction
2. Explore → enrich top targets, optimize filters (5 credits)
3. Re-analyze → apply user feedback, re-classify
4. Provide feedback → "exclude operators" → improve prompt → re-classify

## Checkpoint 3: Post-People

**Trigger**: After contact extraction

| Metric | Threshold | Action if Failed |
|--------|-----------|------------------|
| Total contacts | >= target_count (default 100) | WARN if not met |
| Contacts per company | Average >= 2 | WARN: "Low contact yield. May need different roles." |
| Verified emails | > 80% of extracted | WARN: "Low email verification rate." |
| Role match | > 70% match target roles | WARN: "Many contacts don't match target roles." |

## Pipeline Constants (CRITICAL)

| Constant | Value | Description |
|----------|-------|-------------|
| DEFAULT_TARGET_COUNT | 100 | People to gather before stopping |
| DEFAULT_CONTACTS_PER_COMPANY | 3 | People extracted per target company |
| MAX_PAGES_PER_KEYWORD | 5 | Max Apollo pages per single keyword stream |
| MAX_KEYWORD_REGENERATIONS | 5 | Max keyword regen cycles before giving up |
| LOW_YIELD_THRESHOLD | 10 | If <10 companies on page 1, stop this keyword |
| MAX_TOTAL_CREDITS | 200 | Safety cap — pipeline stops if exceeded |
| EFFECTIVE_PER_PAGE | 60 | Apollo returns ~60 unique per 100 requested |
| COMPANIES_PER_ROUND | 400 | Stop adding Apollo requests when this many unique companies |
| SCRAPE_CONCURRENCY | 100 | Max parallel website scrapes |
| CLASSIFY_CONCURRENCY | 100 | Max parallel LLM classifications |
| PEOPLE_CONCURRENCY | 20 | Max parallel people extraction calls |
| LOW_CONFIDENCE_THRESHOLD | 40 | Below this = low confidence, classify from Apollo data |
| BORDERLINE_CONFIDENCE | 40-70 | Triggers 2-pass re-evaluation with higher model |
| HIGH_CONFIDENCE_THRESHOLD | 70 | Above this = confident classification |
| MAX_REGEN_KEYWORDS_PER_CYCLE | 30-40 | Fresh keywords per regeneration angle |

## KPI Targets (User Can Override)

| KPI | Default | Example Override |
|-----|---------|-----------------|
| target_people | 100 | "I need 50 targets" / "I want 1000 contacts" |
| contacts_per_company | 3 | "5 contacts per company" |
| target_rate_expected | 0.35 | Calculated from actual results |
| max_apollo_credits | 200 | Safety cap |

## Typical Results (Benchmarks)

| Segment | Targets | People | Time | Cost |
|---------|---------|--------|------|------|
| Fashion Italy | 102 | 131 | 59s | $0.17 |
| Video London | 81 | 134 | 55s | $0.19 |
| IT Miami | 18 | 39 | 27s | $0.04 |

## Cost Transparency at Every Gate

**ALWAYS show costs before and after:**
- Before: "Estimated: 102 credits ($1.02) for 100 contacts"
- After: "Spent: 45 credits ($0.45). Remaining: 157 credits."
- Continue: "Next 4 pages: 4 credits. Estimated: +105 contacts."

**Never spend credits without user confirmation.**

### Per-Service Cost Model

| Service | Unit | Cost | Notes |
|---------|------|------|-------|
| **Apollo search** | 1 page (100 results) | 1 credit ($0.01) | Company search |
| **Apollo people search** | per request | FREE | `mixed_people/api_search` — no credits |
| **Apollo bulk_match** | 1 person enriched | 1 credit ($0.01) | Email verification |
| **Apollo org enrich** | 1 company enriched | 1 credit ($0.01) | For exploration |
| **Apollo probe** | 1 probe request | 1 credit ($0.01) | Preview phase |
| **Apify proxy** | per GB transferred | ~$8/GB | Residential proxy for scraping |
| **LLM classification** | per company classified | ~$0.003 | ~$0.07 per 300 companies |
| **LLM reply classification** | per reply (Tier 3 only) | ~$0.001 | Tier 1+2 are FREE |

### Cost Breakdown Format (show at every gate)

```
PIPELINE COST ESTIMATE:
  Apollo search:     ~15 credits ($0.15) — 15 keyword/industry streams × 1 page
  Apollo people:     ~100 credits ($1.00) — 100 contacts × 1 credit each
  Apollo probes:     6 credits ($0.06) — preview phase
  Apify scraping:    ~$0.02 — ~400 pages × ~5KB each
  LLM classify:      ~$0.07 — ~300 companies × $0.003
  ─────────────────────────────
  TOTAL:             ~121 credits ($1.21) + ~$0.09 LLM/proxy
```

### Running Cost Tracker

Track cumulative costs in the run file's `totals`:
```json
{
  "total_credits_search": 24,
  "total_credits_people": 91,
  "total_credits_probe": 6,
  "total_credits": 121,
  "total_usd_apollo": 1.21,
  "total_usd_llm": 0.07,
  "total_usd_proxy": 0.02,
  "total_usd": 1.30
}
```

After each credit-spending action, show: "Spent so far: {N} credits (${X}). Remaining budget: {200-N} credits."

## Pipeline KPI Loop

The autonomous pipeline checks KPIs continuously:

```
ROUND 1: All keywords + industries in parallel
  → Stop adding requests when 400 unique companies reached
  → Scrape + classify as they arrive
  → People extraction for each target
  
CHECK: total_people >= target_count?
  YES → DONE (push to SmartLead)
  NO  → ROUND 2: next batch of keywords
  
REPEAT until:
  - KPI met (100 people) → SUCCESS
  - All keywords exhausted + 5 regeneration cycles → INSUFFICIENT
  - 200 credits cap hit → STOP with warning
```

## Exhaustion Detection

**What counts as "empty"**: A page is empty when `new_unique == 0` (all returned companies already seen in dedup set). NOT `raw_returned == 0` — Apollo may return duplicates.

**Per-stream exhaustion**: Track consecutive empty pages PER keyword/industry stream independently:
- 10 consecutive pages with `new_unique == 0` → this stream is exhausted
- LOW_YIELD_THRESHOLD: if page 1 returns `new_unique < 10` → stop this keyword immediately (bad yield)
- MAX_PAGES_PER_KEYWORD = 5 → stop even if still yielding

**Funding exhaustion cascade**:
- Level 0 (funded): all streams with funding filter → 10 empty = drop funding
- Level 1 (unfunded): same keywords/industries WITHOUT funding → often hits sparse pagination (Apollo returns 0 despite large total_entries). If 3 consecutive empty → move on
- Level 2+: keyword regeneration with new angles
- Geo/size filters NEVER dropped (always mandatory)

**After dropping funding**: Continue the SAME keyword on unfunded stream. Don't stop the keyword just because its funded variant exhausted.

**After ALL initial keywords exhausted**: Regenerate keywords (up to 5 cycles max). Use the angle rotation above — one angle per cycle, 30-40 fresh keywords each.

## Keyword Regeneration

**Max cycles**: 5 regeneration cycles before giving up (status: "insufficient").

**Angle rotation** — use in this order (most productive first, from real pipeline results):
1. **PRODUCT/PLATFORM** names — specific tools, platforms in the space (highest yield)
2. **USE CASES** — what problems solved, buyer pain points
3. **TECHNOLOGY STACK** — protocols, standards, certifications
4. **ADJACENT NICHES** — sub-categories, crossover markets
5. **COMPETITOR/ALTERNATIVES** — comparison terms ("alternative to Deel")

If 5 cycles not enough (rare), the remaining 5 angles are available but pipeline should stop with "insufficient":
6. BUYER SEARCH LANGUAGE, 7. INDUSTRY JARGON, 8. JOB POSTING keywords, 9. INVESTOR/FUNDING keywords, 10. CONFERENCE/EVENT keywords

**Per cycle**: Generate 30-40 completely NEW keywords per angle.

**Dedup algorithm**: Before generating, collect ALL keywords from ALL parent filter snapshots (traverse parent_id chain). Pass this list to the LLM as "ALREADY USED — do not repeat any of these." The LLM generates fresh keywords informed by which target companies were found (their Apollo keywords/industries).

**Informed by found targets**: After each round, look at which companies ARE targets. Extract their Apollo `keywords` and `industry` fields. These inform the regeneration — "companies like {target} have keywords {kw1, kw2}" → generate similar but unexplored keywords.

## Per-Keyword / Per-Industry Performance Tracking

Track aggregated stats for each keyword and industry_tag_id:

```json
{
  "keyword_stats": {
    "payment gateway": {
      "pages_fetched": 5,
      "raw_companies": 500,
      "new_unique": 312,
      "targets_found": 89,
      "target_rate": 0.28,
      "credits_used": 5,
      "funded": false
    }
  },
  "industry_stats": {
    "financial services": {
      "pages_fetched": 5,
      "raw_companies": 500,
      "new_unique": 287,
      "targets_found": 112,
      "target_rate": 0.39,
      "credits_used": 5,
      "funded": false
    }
  },
  "pipeline_summary": {
    "rounds_completed": 2,
    "total_credits": 45,
    "keywords_used": 15,
    "keywords_available": 25,
    "total_unique_companies": 892,
    "total_targets": 201,
    "overall_target_rate": 0.22,
    "total_people": 103,
    "kpi_met": true
  }
}
```

## "Find More" / "Continue" Handling

When user says "find more contacts":
1. Show current count
2. Calculate next batch cost
3. "Current: 102 contacts. Next 4 pages: 4 credits. Estimated: +105 contacts."
4. User confirms → continue with page_offset (don't re-fetch existing)
5. Don't re-search already gathered companies
