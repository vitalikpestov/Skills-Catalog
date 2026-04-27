# Pipeline State Skill

Defines the entity model, run file format, round loop algorithm, and cross-run intelligence protocol. This skill tells the agent HOW to structure and track every piece of data throughout the pipeline.

## When to Use

- During /leadgen command (create and maintain run file)
- During /qualify command (create iterations)
- After any pipeline run completes (update filter_intelligence.json)
- When "find more" resumes an existing run

## The Run File

Every pipeline execution produces ONE file: `runs/run-{id}.json`. This is the complete, self-contained record. All 6 entities live inside it.

```
~/.gtm-mcp/projects/{project}/
├── project.yaml
├── runs/
│   ├── run-001.json          ← Everything for this pipeline execution
│   ├── run-002.json          ← "Find more" or new segment
│   └── latest.json
├── feedback.json             ← User corrections (across runs)
├── sequences.json
└── campaigns.json
```

Create the run file with `save_data(project, "runs/run-{id}.json", data)` at pipeline start. Update it with `save_data(project, "runs/run-{id}.json", data, mode="merge")` as phases complete.

Generate run IDs as `run-{NNN}` where NNN is zero-padded sequential (run-001, run-002, ...).

## Entity 1: FilterSnapshot

Immutable record of exact filters at a point in time. NEVER modify — create a new snapshot when filters change.

```json
{
  "id": "fs-001",
  "created_at": "2026-04-04T10:15:00Z",
  "trigger": "initial_generation",
  "parent_id": null,
  "filters": {
    "keywords": ["employer of record", "EOR platform", "...85 total"],
    "industry_tag_ids": ["5567cd82a1e38c..."],
    "industry_names": ["human resources"],
    "locations": ["United States"],
    "employee_ranges": ["11,50", "51,200"],
    "funding_stages": ["series_a", "series_b"]
  },
  "generation_details": {
    "query": "EOR clients in the US",
    "strategy": "keywords_first",
    "keywords_from_seed": 8,
    "keywords_from_generation": 16,
    "keywords_from_expansion": 61,
    "total_keywords": 85,
    "industries_classification": {"human resources": "SPECIFIC"}
  }
}
```

**Create new snapshot when:**

| Trigger | parent_id | What Changed |
|---------|-----------|---|
| `initial_generation` | null | First filter set from query + offer |
| `exploration_improved` | previous | After enriching top 5 targets — new keywords/industries discovered |
| `keyword_regeneration_{N}` | previous | After round exhausted — fresh keywords from specific angle |
| `user_adjustment` | previous | User said "also add management consulting" |

## Entity 2: APIRequest

Every single Apollo API call. One keyword OR one industry_tag_id per request.

```json
{
  "id": "req-017",
  "filter_snapshot_id": "fs-001",
  "round_id": "round-001",
  "is_probe": false,
  "created_at": "2026-04-04T10:20:03Z",
  "type": "keyword",
  "filter_value": "employer of record",
  "funded": true,
  "page": 1,
  "result": {
    "raw_returned": 100,
    "new_unique": 72,
    "duplicates": 28,
    "credits_used": 1,
    "apollo_total_entries": 1933
  }
}
```

For industry requests, add `filter_tag_id` field with the hex tag ID.

Generate request IDs as `req-{NNN}` sequential within the run.

## Entity 3: Round

One gather-scrape-classify-people cycle.

```json
{
  "id": "round-001",
  "filter_snapshot_id": "fs-001",
  "started_at": "2026-04-04T10:20:00Z",
  "completed_at": "2026-04-04T10:28:00Z",
  "status": "completed",
  "gather_phase": {
    "started_at": "10:20:00",
    "completed_at": "10:24:00",
    "keywords_used": ["employer of record", "EOR platform", "...10 total"],
    "industries_used": ["human resources"],
    "funded_streams": true,
    "request_ids": ["req-001", "req-002", "..."],
    "total_api_calls": 24,
    "unique_companies_gathered": 387,
    "credits_used": 24,
    "stopped_reason": "reached_400_cap"
  },
  "scrape_phase": {
    "started_at": "10:20:05",
    "completed_at": "10:25:00",
    "total": 375,
    "success": 334,
    "failed": 29,
    "timeout": 12,
    "success_rate": 0.89
  },
  "classify_phase": {
    "started_at": "10:20:30",
    "completed_at": "10:27:00",
    "total_classified": 334,
    "targets": 89,
    "rejected": 245,
    "target_rate": 0.27,
    "segment_distribution": {"EOR_CLIENTS": 62, "CONTRACTOR_PAYROLL": 27},
    "avg_confidence": 78,
    "iteration": 1
  },
  "people_phase": {
    "started_at": "10:27:00",
    "completed_at": "10:28:00",
    "targets_processed": 34,
    "contacts_extracted": 98,
    "contacts_verified": 91,
    "credits_used": 91,
    "avg_per_company": 2.68
  },
  "kpi_check": {
    "target_people": 100,
    "current_people": 91,
    "kpi_met": false,
    "decision": "continue_to_round_2",
    "people_needed": 9
  }
}
```

**Phases overlap (streaming):** Scrape starts the MOMENT first company arrives from Apollo. Classify starts when first scrape finishes. People starts when first target confirmed. All run concurrently. Round completes when ALL phases finish and KPI is checked.

## Entity 4: Company

Keyed by domain. References request IDs that found it.

```json
{
  "domain": "fastgrowthstartup.com",
  "name": "FastGrowth",
  "apollo_id": "abc123",
  "discovery": {
    "first_seen_at": "2026-04-04T10:20:05Z",
    "found_by_requests": ["req-003", "req-017"],
    "found_in_round": "round-001",
    "funded_stream": true,
    "apollo_data": {
      "industry": "computer software",
      "industry_tag_id": "5567cd82a1e4f...",
      "employee_count": 150,
      "country": "United States",
      "city": "Austin",
      "founded_year": 2020,
      "keywords": ["saas", "hr tech", "remote work"],
      "linkedin_url": "https://linkedin.com/company/fastgrowth"
    }
  },
  "timeline": {
    "gathered_at": "2026-04-04T10:20:05Z",
    "scraped_at": "2026-04-04T10:20:42Z",
    "classified_at": "2026-04-04T10:21:01Z",
    "people_extracted_at": "2026-04-04T10:23:15Z"
  },
  "scrape": {
    "status": "success",
    "http_status": 200,
    "text_length": 4823,
    "text": "FastGrowth is a Series B startup..."
  },
  "classification": {
    "is_target": true,
    "confidence": 88,
    "segment": "EOR_CLIENTS",
    "reasoning": "Series B startup, 150 employees across 12 countries. Uses Deel. Would benefit from switching.",
    "classified_from": "scraped_text",
    "iteration": 1
  },
  "people_extraction": {
    "target_roles": ["VP HR", "CHRO", "Head of People"],
    "rounds": [
      {"round": 1, "enriched": ["VP Sales", "CRO", "CEO"], "verified": ["VP Sales"], "credits": 3},
      {"round": 2, "enriched": ["Head of Growth", "CMO"], "verified": ["Head of Growth", "CMO"], "credits": 2}
    ],
    "total_verified": 3,
    "total_credits": 5
  },
  "blacklisted": false
}
```

**Provenance chain**: company.found_by_requests → requests[id] → request.filter_snapshot_id → filter_snapshots[id].filters

**Dedup rule**: If same domain found by multiple requests, add ALL request IDs to `found_by_requests`. Don't create duplicate company entries.

## Company Name Normalization

Every company name gets normalized before storing and before pushing to SmartLead. Rules:
1. Strip legal suffixes: ", Inc.", ", LLC", ", Ltd.", ", Corp.", ", GmbH", ", S.A.", ", B.V.", ", Pty Ltd", ", PLC"
2. Strip trailing "." or ","
3. Trim whitespace
4. Keep original casing (don't force title case — "iOS" should stay "iOS")
5. Store both: `name` (raw from Apollo) and `name_normalized` (cleaned)

Examples: "FastGrowth, Inc." → "FastGrowth", "Stripe, Inc." → "Stripe", "SAP SE" → "SAP SE" (SE is not stripped — only comma-prefixed suffixes)

SmartLead custom fields use the normalized name: `{{company_name}}` = normalized.

## Entity 5: Contact

```json
{
  "email": "john.smith@fastgrowthstartup.com",
  "email_verified": true,
  "name": "John Smith",
  "title": "VP of People Operations",
  "seniority": "vp",
  "linkedin_url": "https://linkedin.com/in/johnsmith",
  "company_domain": "fastgrowthstartup.com",
  "company_name_normalized": "FastGrowth",
  "segment": "EOR_CLIENTS",
  "extraction": {
    "round_id": "round-001",
    "enrichment_round": 1,
    "credits_used": 1,
    "extracted_at": "2026-04-04T10:27:15Z",
    "role_match": "primary"
  }
}
```

## Entity 6: Iteration

Classification pass. New iteration created on user feedback.

```json
{
  "id": "iter-001",
  "created_at": "2026-04-04T10:25:00Z",
  "trigger": "initial_classification",
  "filter_snapshot_id": "fs-001",
  "parent_iteration": null,
  "feedback_applied": [],
  "results": {
    "total_classified": 334,
    "targets": 89,
    "target_rate": 0.27,
    "segment_distribution": {"EOR_CLIENTS": 62, "CONTRACTOR_PAYROLL": 27}
  }
}
```

After feedback:
```json
{
  "id": "iter-002",
  "trigger": "user_feedback",
  "parent_iteration": "iter-001",
  "feedback_applied": ["Exclude EOR providers (competitors). Only target companies that USE EOR services."],
  "results": {
    "total_classified": 334,
    "targets": 71,
    "target_rate": 0.21,
    "flipped_target_to_rejected": 22,
    "flipped_rejected_to_target": 4
  }
}
```

## Phase Tracking (state.yaml)

The pipeline tracks phase-level progress in `state.yaml` (separate from the run file).

**Relationship**:
- `state.yaml` = pipeline-level progress (which of 7 phases is complete)
- `runs/run-{id}.json` = execution-level detail (companies, contacts, rounds, filter snapshots)
- state.yaml is updated at PHASE BOUNDARIES only. Run file is updated continuously.

**Schema**: See io-state-safe skill for full schema and validation rules.

**Location**: `~/.gtm-mcp/projects/{slug}/state.yaml` — alongside run files.

**Resume**: On re-run, load state.yaml → skip completed phases → resume from first incomplete. See resume-checkpoint skill for the full algorithm.

## Pause/Resume Protocol

The pipeline supports pause and resume at natural checkpoints.

**Status transitions**:
```
running → paused    (user says "pause" or "stop" during pipeline)
paused  → running   (user says "continue" or "resume")
running → completed (KPI met)
running → insufficient (all keywords exhausted + 5 regen cycles)
running → failed    (unrecoverable error)
```

**How pause works**: The agent pauses NATURALLY at approval gates (cost gate, classification review, campaign push). No complex state machine needed — the conversation IS the pause mechanism.

**Explicit pause**: If user says "pause" or "stop" mid-pipeline:
1. Set `status: "paused"` in run file
2. Save current round state (in-progress phases complete, pending phases stop)
3. Record `paused_at` timestamp and `paused_after_phase` (gather/scrape/classify/people)
4. "Pipeline paused after {phase}. {N} companies gathered, {M} contacts so far. Say 'resume' to continue."

**Resume**: User says "continue" or "resume":
1. Load run file, check `status == "paused"`
2. Read `paused_after_phase` — pick up from next phase
3. Set `status: "running"`, record `resumed_at`
4. Continue round loop from where it stopped

**Approval gates are the primary pause mechanism**:
- Before any credit-spending action → show plan + wait
- Before SmartLead push → show draft + wait
- Before campaign activation → require "I confirm"
- These natural pauses mean the pipeline rarely needs explicit pause

## "Find More" Resume State

When user says "find more" or "continue", the pipeline resumes from where it left off. Each completed round stores resume state:

```json
{
  "resume_from": {
    "keywords_used": ["employer of record", "EOR platform", "...10 used"],
    "keywords_remaining": ["global payroll", "contractor management", "...15 remaining"],
    "industries_used": ["human resources"],
    "industries_remaining": [],
    "page_offsets": {
      "employer of record": 5,
      "EOR platform": 3,
      "human resources": 5
    },
    "companies_seen": 512,
    "contacts_so_far": 91,
    "filter_snapshot_id": "fs-001",
    "last_round_id": "round-001"
  }
}
```

**Resume algorithm**:
1. Load latest run → read `resume_from` from last round
2. Continue from `keywords_remaining` at `page_offsets` (don't re-fetch pages)
3. Dedup against ALL `companies` already in run (by domain)
4. Don't create new run — add new round to existing run
5. New round gets `resumed: true` flag and `resumed_from_round: "round-001"`
6. KPI check uses cumulative contacts across ALL rounds in this run

**Cost transparency on resume**:
```
"Current: 91 contacts (from 512 companies). 
 15 keywords remaining × ~3 pages = ~45 credits.
 Estimated: +200 companies → +70 targets → +210 contacts.
 Continue?"
```

## Complete Run File Structure

```json
{
  "run_id": "run-001",
  "project": "easystaff-payroll",
  "campaign_id": 3070919,
  "campaign_slug": "payments-us",
  "mode": "fresh",
  "created_at": "...",
  "status": "running | paused | completed | insufficient | failed",
  "completed_at": "...",

  "kpi": {
    "target_people": 100,
    "max_people_per_company": 3,
    "max_credits": 200
  },

  "dedup_baseline": {
    "previous_run_companies": 0,
    "previous_run_contacts": 0,
    "seen_domains_count": 0,
    "seen_emails_count": 0
  },

  "probe": {
    "filter_snapshot_id": "fs-001",
    "request_ids": ["req-001", "req-002", "req-003", "req-004", "req-005", "req-006"],
    "companies_from_probe": 253,
    "companies_deduped": 201,
    "credits_used": 6,
    "reused_on_confirm": true,
    "breakdown": [
      {"type": "industry", "tag_id": "5567cdd67369643e64020000", "name": "financial services", "request_id": "req-001", "total": 3200, "companies": 100},
      {"type": "industry", "tag_id": "5567cd4773696439b10b0000", "name": "banking", "request_id": "req-002", "total": 1800, "companies": 85},
      {"type": "keyword", "name": "payment gateway", "request_id": "req-003", "total": 3199, "companies": 85},
      {"type": "keyword", "name": "PSP platform", "request_id": "req-004", "total": 401, "companies": 68}
    ]
  },

  "filter_snapshots": [],
  "rounds": [],
  "requests": [],
  "companies": {},
  "contacts": [],
  "iterations": [],

  "funding_cascade": {
    "level_0_funded": {"requests": 0, "unique_companies": 0, "exhausted_at": null},
    "level_1_unfunded": {"requests": 0, "unique_companies": 0, "exhausted_at": null}
  },

  "taxonomy_extensions": [],

  "keyword_leaderboard": [],
  "industry_leaderboard": [],

  "totals": {
    "rounds_completed": 0,
    "total_api_requests": 0,
    "total_credits_search": 0,
    "total_credits_people": 0,
    "total_credits": 0,
    "total_usd": 0,
    "unique_companies": 0,
    "companies_scraped": 0,
    "companies_classified": 0,
    "targets": 0,
    "contacts_extracted": 0,
    "contacts_deduped_skipped": 0,
    "kpi_met": false,
    "duration_seconds": 0
  },

  "campaign": {
    "campaign_id": 3070919,
    "leads_pushed": 102,
    "pushed_at": "2026-04-06T11:00:00Z"
  }
}
```

**New fields explained:**

| Field | Purpose |
|-------|---------|
| `campaign_id` | SmartLead campaign this run feeds into (null until campaign created/assigned) |
| `campaign_slug` | Local campaign directory slug |
| `mode` | `"fresh"` = new campaign, `"append"` = adding to existing campaign |
| `dedup_baseline` | Snapshot of how many companies/contacts existed BEFORE this run started |
| `contacts_deduped_skipped` | Contacts found but not pushed because they were already in the campaign |
| `campaign` | Populated when leads are pushed (was always null before) |

## The Round Loop Algorithm

```
1. CREATE FilterSnapshot fs-001 (initial generation)
2. PROBE: 1 request per top-3 keywords + top-3 industries (6 credits max)
   → Each probe = a real APIRequest with `is_probe: true`, `round_id: null`
   → Probe companies saved to run's `companies` dict immediately (deduped by domain)
   → Probe `request_ids` stored in `probe.request_ids` array
   → Show `probe.breakdown` to user with per-filter results
   → WAIT for user confirmation

3. On confirm → CREATE Round round-001:
   a. GATHER (streaming):
      - 1 keyword per Apollo request, all in parallel
      - 1 industry_tag_id per Apollo request, all in parallel
      - If funding: funded AND unfunded variants of ALL above simultaneously
      - Each company → check global dedup (seen_domains set)
      - STOP adding new requests when 400 unique companies reached
      - Probe companies flow in first (skip page 1 for probed filters)
      - Track: each company gets found_by_requests[], found_in_round

   b. SCRAPE (streaming, starts as companies arrive):
      - 100 concurrent website scrapes
      - Each company → scrape result → flows to classify

   c. CLASSIFY (streaming, starts as scrapes arrive):
      - 100 concurrent classifications
      - Via negativa rules from company-qualification skill
      - Each company → is_target, confidence, segment, reasoning
      - classified_from: always "scraped_text" (NEVER Apollo industry)

   d. PEOPLE (streaming, starts as targets confirmed):
      - 20 concurrent people extractions
      - For each target: search (FREE) → enrich (1 credit/person)
      - Retry: if <3 verified, try next candidates matching target_roles
      - Max 3 retry rounds, max 12 credits per company
      - Seniority priority: owner > founder > c_suite > vp > head > director
      - Side effect: bulk_match may return new industry_tag_ids → save to taxonomy_extensions

   e. KPI CHECK (after all phases complete):
      - current_people >= target_people?
      - YES → DONE, proceed to campaign push
      - NO → decision: continue_to_round_2

4. If KPI not met:
   - Are there unused keywords? → use next batch in Round 2 (same filter snapshot)
   - All keywords exhausted? → REGENERATE keywords:
     - CREATE FilterSnapshot fs-002 (keyword_regeneration_1, parent: fs-001)
     - Angle: pick next from 10 angles (see quality-gate skill)
     - Informed by: which target companies were found (their Apollo keywords)
     - Excluded: ALL keywords from parent snapshot (never repeat)
   - CREATE Round round-002 with new/remaining keywords → go to step 3

5. REPEAT until:
   - KPI met → push to SmartLead (DRAFT)
   - All keywords exhausted + 5 regeneration cycles → status: "insufficient"
   - 200 credits cap hit → status: "insufficient", warn user
```

## Exhaustion Detection

Per keyword/industry stream:
- 10 consecutive empty pages = exhausted
- LOW_YIELD_THRESHOLD: page 1 returns <10 companies = stop immediately
- MAX_PAGES_PER_KEYWORD: 5 pages max per stream

Funding cascade:
- Level 0 (funded): all keyword+industry requests WITH funding → exhausted when 10 empty
- Level 1 (unfunded): same requests WITHOUT funding → often sparse pagination (0 results)
- Level 2+: keyword regeneration cycles

Geo and size filters are NEVER dropped. Funding is dropped when exhausted.

## Leaderboard Computation

After each round completes, compute per-keyword and per-industry stats:

```
For each keyword K:
  requests_for_K = requests.filter(r => r.type == "keyword" && r.filter_value == K)
  all_companies_for_K = companies.filter(c => c.found_by_requests intersects requests_for_K.ids)
  targets_for_K = all_companies_for_K.filter(c => c.classification.is_target)
  
  keyword_leaderboard.push({
    keyword: K,
    requests: requests_for_K.length,
    unique_companies: all_companies_for_K.length,
    targets: targets_for_K.length,
    target_rate: targets_for_K.length / all_companies_for_K.length,
    credits: sum(requests_for_K.result.credits_used),
    funded: requests_for_K[0].funded,
    quality_score: target_rate * log(unique_companies + 1) / credits
  })
```

Sort by `quality_score` DESC. Same for industries.

## Post-Run: Update Filter Intelligence

After run completes, update `~/.gtm-mcp/filter_intelligence.json`:

```
1. Read run file → keyword_leaderboard, industry_leaderboard
2. For each keyword:
   - Exists in keyword_knowledge? → update: avg_target_rate, increment times_used, update best_target_rate
   - New? → create entry with this run's stats
3. Same for industries
4. Update segment_playbooks:
   - Match run's segment to existing playbook (or create new)
   - Update: best_keywords (top 5 by quality_score), avg_target_rate, avg_cost
5. Update funding_knowledge based on funded vs unfunded comparison
6. Save with save_data("_global", "filter_intelligence.json", data, mode="merge")
```

## Consuming Intelligence (New Run)

When generating filters for a new run:

```
1. Read filter_intelligence.json
2. Find closest segment_playbook to current segment
3. best_keywords from playbook → HIGH-PRIORITY seeds for keyword generation
4. funding_essential → always include funding filter
5. industry classification → pick industry_first or keywords_first strategy
6. Show user: "Based on N previous runs, expect ~X% target rate, ~$Y cost"
```

Intelligence is ADVISORY. The agent uses it as seeds and hints, not as hard constraints. New keywords are still generated — intelligence just makes the starting point much better.

---

## Approval Document

Before pipeline execution starts, create `pipeline-config.yaml` in the project workspace:

```yaml
project: "Fintech Outreach"
source: apollo
destination: smartlead
status: awaiting_approval  # → approved → running → completed → failed

filters:
  segments: ["PAYMENTS", "LENDING", "REGTECH"]
  geo: ["United States", "United Kingdom"]
  size: "20,500"
  industries: ["financial services"]
  keywords: ["payment gateway API", "lending platform", ...]  # 20-30
  funding: ["series_a", "series_b"]  # prioritization

email_accounts:
  filter_used: "all accounts with Renat"
  selected:
    - {id: 14, email: "renat@sally.io", name: "Renat"}
    - {id: 27, email: "renat@trysally.io", name: "Renat S"}

sequence:
  type: "GOD_SEQUENCE"  # or "user_provided"
  steps: 4
  cadence: [0, 3, 7, 14]

blacklist:
  sources: ["ES Global Q1", "ES Global Q2"]
  domains_count: 1847
  time_window: null  # or "3_months"

kpi:
  target_contacts: 100
  contacts_per_company: 3

cost_estimate:
  search_credits: 30
  enrichment_credits: 100
  total: 130

max_cost: 200
```

**Status transitions**: `awaiting_approval → approved → running → completed`
- `awaiting_approval`: config created, shown to user, waiting for "proceed"
- `approved`: user confirmed, pipeline starting
- `running`: round loop executing
- `completed`: KPI met, campaign created
- `failed`: unrecoverable error

---

## Pipeline Completion Output

When pipeline finishes, return structured summary:

```json
{
  "status": "completed",
  "kpi_met": true,
  "campaign": {
    "id": 12345,
    "name": "IT Consulting — Miami",
    "url": "https://app.smartlead.ai/app/email-campaigns-v2/12345/analytics",
    "status": "DRAFT"
  },
  "contacts_file": "contacts.json",
  "costs": {
    "apollo_search_credits": 23,
    "apollo_enrichment_credits": 102,
    "total_credits": 125
  },
  "stats": {
    "companies_gathered": 487,
    "companies_scraped": 412,
    "targets_found": 52,
    "target_rate": "10.7%",
    "contacts_extracted": 134,
    "contacts_verified": 102,
    "rounds_completed": 2
  },
  "keyword_performance": {
    "payment gateway": {"new_unique": 198, "targets": 62, "rate": "31%"},
    "lending platform": {"new_unique": 52, "targets": 18, "rate": "35%"}
  }
}
```

---

## "Find More" Protocol

When user says "find more", "continue", or "get more contacts":

```
1. Load latest run file for this project
2. Identify campaign: run.campaign_id (may be null if campaign not yet created)
3. Check current state:
   - KPI met? → "Already have N contacts (KPI met). Gather more anyway?"
   - KPI not met? → "Have N contacts, need M more. Continuing..."

4. DO NOT create a new run — add new round to existing run
5. Build dedup sets:
   a. seen_domains = run.companies.keys()  (all companies already in this run)
   b. If run.campaign_id exists:
      - Load companies from ALL other runs for this campaign:
        campaign = load_data(project, f"campaigns/{run.campaign_slug}/campaign.yaml")
        for prev_run_id in campaign.run_ids:
          if prev_run_id != run.run_id:
            prev = load_data(project, f"runs/{prev_run_id}.json")
            seen_domains.update(prev.companies.keys())
      - Export existing campaign leads for email dedup:
        existing = smartlead_export_leads(run.campaign_id)
        seen_emails = {lead.email for lead in existing.leads}
6. Generate new keywords using next regeneration angle
   (angles: product names → tech stacks → use cases → buyer language → adjacent niches)
   Seed from keyword_leaderboard — top performers first
7. Create new FilterSnapshot with parent = previous snapshot
8. Execute round loop: gather → scrape → classify → people
   - Company dedup against seen_domains
   - Contact dedup against seen_emails

9. Update run file with new round data
10. If run.campaign_id exists:
    - Push new contacts: smartlead_add_leads(campaign_id, new_deduped_leads)
    - Update campaign.yaml: total_leads_pushed += N, run_ids (if not already there)
    - Update run.campaign: {leads_pushed: cumulative, pushed_at: now}
11. Show incremental stats: "+N new contacts (total: M), {skipped} duplicates filtered"
```

---

## Cross-Run Dedup Protocol (Append Mode)

When a run has `mode: "append"` (adding contacts to an existing campaign), dedup is critical to avoid wasting credits and pushing duplicate leads.

### Setup (before round loop starts)

```
1. Load campaign.yaml for the target campaign
2. Collect ALL companies from ALL previous runs for this campaign:
   seen_domains = set()
   for run_id in campaign.run_ids:
     prev_run = load_data(project, f"runs/{run_id}.json")
     seen_domains.update(prev_run.companies.keys())

3. Export existing campaign leads from SmartLead:
   existing = smartlead_export_leads(campaign_id)
   seen_emails = {lead["email"] for lead in existing.data.leads}
   seen_domains.update(existing.data.domains)

4. Record baseline in run file:
   dedup_baseline = {
     previous_run_companies: len(seen_domains),
     previous_run_contacts: existing.data.count,
     seen_domains_count: len(seen_domains),
     seen_emails_count: len(seen_emails)
   }
```

### During Round Loop

```
GATHER phase:
  - For each company returned by Apollo:
    if company.domain in seen_domains → SKIP (don't scrape, classify, or extract)
    else → add to run, proceed as normal

PEOPLE phase:
  - For each extracted contact:
    if contact.email in seen_emails → SKIP (don't push to campaign)
    else → add to contacts, will push to SmartLead

  Track: totals.contacts_deduped_skipped += skipped_count
```

### KPI Offset

```
Mode "fresh":   KPI target = kpi.target_people
Mode "append":  KPI target = kpi.target_people (this is already the DELTA — how many MORE)
                The /launch command calculates the delta before creating the run.
                Example: user says kpi=200, campaign has 102 → run.kpi.target_people = 98
```

### After Push

```
1. smartlead_add_leads(campaign_id, new_deduped_contacts)
2. Update campaign.yaml:
   run_ids: append this run_id
   total_leads_pushed: += len(new_contacts)
3. Update run.campaign:
   campaign_id, leads_pushed, pushed_at
4. Update filter_intelligence.json with keyword/industry leaderboards
```

---

## Temporal Blacklist

Blacklist entries include metadata for time-windowed filtering:

```json
{
  "domain": "example.com",
  "source": "smartlead_campaign",
  "campaign_name": "ES Global Q1",
  "last_contact_date": "2026-01-15",
  "blacklisted_at": "2026-04-06"
}
```

**Time-window logic**:
- Default: blacklist ALL (no time filter)
- User says "last 3 months only" → `last_contact_date > (now - 3 months)`
- Companies contacted more than 3 months ago are OK to re-target
- Store `last_contact_date` from SmartLead campaign lead data
