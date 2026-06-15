---
name: competitor-compare
description: "Generates side-by-side HTML comparisons of DoseSync UI patterns against 6 curated competitors (Medisafe, MyTherapy, CareClinic, Flighty, Huckleberry, How We Feel). Reads locally-curated screenshots from competitors/ folder — no runtime scraping. Organized by UI pattern (hero card, paywall, onboarding, confirm CTA, empty state, streak). Use this skill when the user asks to compare against competitors, benchmark UI patterns, generate competitive analysis, see DoseSync vs Medisafe, or create design benchmarking report. Outputs HTML files in competitors/reports/."
---

# Competitor Compare — DoseSync

Side-by-side UI benchmarking against 6 curated competitors. Compares **by UI pattern**, not by app-screen — that's how design decisions actually get made.

## When to invoke

- `/competitor-compare hero` — compare hero card pattern across apps
- `/competitor-compare paywall` — paywall designs
- `/competitor-compare onboarding` — onboarding flows
- `/competitor-compare all` — generate all pattern reports
- Before major UI refactor, to check what benchmarks exist

## Competitor Set (6 — curated, maintainable)

### Direct competitors (3)

| App | Role | What to study |
|-----|------|---------------|
| **Medisafe** | Market leader, 10M+ DL | Onboarding, hard paywall (new Jan 2026), pill tray metaphor |
| **MyTherapy** | Free B2B, different monetization | UI polish without paywall pressure, mood check-in |
| **CareClinic** | Closest to family/holistic | Feature breadth trap (we avoid), tracking variety |

### Pattern references (3)

| App | Pattern | Why |
|-----|---------|-----|
| **Flighty** | Hero card + Live Activity | Gold standard for countdown/next-event card |
| **Huckleberry** | Family sync + child-caregiver | Direct analog for our family coordination |
| **How We Feel** | One-tap confirm + calm tone | Benchmark for dose confirm CTA |

**Dropped (why):** Pillo (too new), Dosecast (outdated), Zero (wrong context), Copilot Money (tone ref, use ad-hoc), Flo (cycle logging, overlap minimal vs Huckleberry).

## UI Patterns Tracked

Comparisons organized by pattern — not by app-screen pair. This is because design decisions are usually "what's the best hero card" not "Medisafe onboarding step 3 vs ours".

| Pattern slug | Description | Competitors with this pattern |
|--------------|-------------|-------------------------------|
| `hero` | Main screen hero card / next event | Flighty ⭐, Medisafe, MyTherapy |
| `paywall` | Subscription paywall surface | Medisafe, Flighty, Flo (ref) |
| `onboarding` | Welcome + first steps | Medisafe, Huckleberry, How We Feel |
| `confirm-cta` | Primary action confirmation | How We Feel ⭐, MyTherapy |
| `empty-state` | No data initial view | Bears Gratitude (ref), MyTherapy |
| `streak` | Habit/adherence streak | Duolingo (ref), Gentler Streak (ref) |
| `family-feed` | Multi-user activity log | Huckleberry ⭐, Strava (ref) |

## Setup (one-time)

### Folder structure

```
DoseSync/competitors/
├── medisafe/
│   ├── hero/
│   │   ├── 01_home.png
│   │   └── 02_next_dose.png
│   ├── paywall/
│   │   ├── 01_trust.png
│   │   ├── 02_plans.png
│   │   └── 03_trial.png
│   ├── onboarding/
│   │   └── 01_welcome.png
│   └── metadata.yaml    # app info, last updated
├── mytherapy/
├── careclinic/
├── flighty/
├── huckleberry/
├── howwefeel/
├── dosesync/            # our own screens — captured via /audit-ui
│   ├── hero/
│   ├── paywall/
│   └── onboarding/
└── reports/             # HTML outputs
    ├── 2026-04-18_hero.html
    ├── 2026-04-18_paywall.html
    └── ...
```

### How to populate screenshots

**Recommended:** Mobbin Pro subscription (~$29/mo) — manual curation, ~30 min per app flow, do quarterly.

Workflow:
1. Open Mobbin → search "Medisafe" → browse flows
2. Screenshot-grab the relevant pattern screens
3. Save to `competitors/medisafe/<pattern>/NN_screen.png` (zero-padded order)
4. Update `competitors/medisafe/metadata.yaml`

**Alternative for marketing/paywall:** iTunes Search API returns public App Store screenshots:
```bash
curl 'https://itunes.apple.com/lookup?id=920353840&country=us' | jq '.results[0].screenshotUrls'
```
(ID 920353840 = Medisafe). Download and save to appropriate pattern folder.

## Execution Steps

### Step 1: Parse invocation

- `/competitor-compare <pattern>` — compare this pattern across all competitors that have it
- `/competitor-compare all` — run every pattern
- No args → default to `hero` (most-requested)

### Step 2: Read metadata

For each competitor in `competitors/<name>/metadata.yaml`, load:
- App name, App Store URL
- Last updated date (warn if > 90 days old)
- Notes (what's interesting about their approach)

### Step 3: Collect screenshots for the pattern

For selected pattern `P`:
- For each competitor: read `competitors/<name>/P/*.png` (sorted alphabetically)
- For DoseSync: read `competitors/dosesync/P/*.png`

If any folder missing — report as "not yet curated" in output, skip gracefully.

### Step 4: Generate HTML report

Write `DoseSync/competitors/reports/YYYY-MM-DD_<pattern>.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>DoseSync vs Competitors — <pattern> — YYYY-MM-DD</title>
  <style>
    /* CSS grid: N columns = number of apps with this pattern */
    /* Image max-width: 240px, tall aspect preserved */
    /* Caption below each screenshot with app name + screen name */
  </style>
</head>
<body>
  <h1>Pattern: <pattern></h1>
  <div class="grid">
    <!-- Column per app: DoseSync first, then competitors -->
    <div class="column">
      <h3>DoseSync</h3>
      <img src="../dosesync/<pattern>/01_X.png" />
      <img src="../dosesync/<pattern>/02_Y.png" />
    </div>
    <div class="column">
      <h3>Medisafe</h3>
      <!-- ... -->
    </div>
    <!-- etc -->
  </div>
  <h2>Observations</h2>
  <!-- Claude writes 3-5 bullet design takeaways based on visual comparison -->
</body>
</html>
```

### Step 5: Optional single-PNG composition

If `--export=png` flag passed, use ImageMagick (`brew install imagemagick`) to create shareable single image:

```bash
montage competitors/dosesync/hero/*.png competitors/medisafe/hero/*.png [...] \
  -tile 6x1 -geometry 240x800+8+8 \
  competitors/reports/YYYY-MM-DD_hero.png
```

Useful for Telegram/Twitter sharing.

### Step 6: Summary to user

```
Competitor Compare complete — pattern: <P>

Apps compared: N
Screens per app: avg X

Report: competitors/reports/YYYY-MM-DD_<P>.html

Key observations:
1. {takeaway}
2. {takeaway}
3. {takeaway}

Next: open the HTML in browser, review, document decisions in DESIGN.md.
```

## Maintenance cadence

- **Weekly:** add new DoseSync screens to `competitors/dosesync/` via `/audit-ui` workflow
- **Quarterly:** refresh competitor screenshots (Mobbin Pro browse session, ~1 hour)
- **Annually:** re-evaluate competitor set — drop dead apps, add new breakouts

## What this skill does NOT do

- Does NOT scrape App Store or Mobbin at runtime — brittle, ToS risk
- Does NOT auto-analyze design decisions — humans still compare and decide
- Does NOT measure pixel-level metrics — visual side-by-side only
- Does NOT cover Android apps — iOS only

## Known gaps

- Relies on manual curation — stale data if not refreshed quarterly
- No automated change detection (did Medisafe change paywall? you'll miss it)
- Mobbin Pro subscription required for most pattern curation (~$29/mo)

## v2 roadmap

- **v1.1:** iTunes Search API integration for marketing screenshots (paywall in particular) — automated refresh for public assets
- **v1.2:** Obsidian integration — drop comparisons into vault via `vault-sync` skill
- **v2.0:** Pattern-level diff vs last comparison (did the design change since last review?)
- **v2.1:** Mobile app reviews scraping for qualitative feedback (paired with visual)

## Example outputs

**Pattern `hero`:** 6 apps × 2 screens = 12 screenshots side-by-side with observations like:
- "Flighty hero is 1.8× taller than ours — gives countdown more visual weight"
- "Medisafe shows 3 doses in carousel; we show 1 hero + list"
- "None of the competitors have attribution ('given by Grandma') — our moat confirmed visually"

## Related

- `mapping.yaml` — competitor app configuration (IDs, URLs, notes)
- `/audit-ui` skill — generates DoseSync own screenshots for comparison
- Mobbin Pro: https://mobbin.com (paid, $29/mo)
- iTunes Search API: https://itunes.apple.com/lookup?id=<app_id>
