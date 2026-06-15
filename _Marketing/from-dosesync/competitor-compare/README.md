# competitor-compare — DoseSync Skill

Side-by-side UI benchmarking against 6 curated competitors. Organized by **UI pattern** (hero, paywall, onboarding, etc.), not by app-screen pair.

## Quick Start

```
/competitor-compare hero          # compare hero card pattern
/competitor-compare paywall       # compare paywalls
/competitor-compare all           # run every pattern
```

Generates `DoseSync/competitors/reports/YYYY-MM-DD_<pattern>.html`.

## Philosophy

- **Manual curation over scraping** — Mobbin Pro ($29/mo) + local folder, no runtime breakage
- **By pattern, not by app** — "best hero card" drives decisions, "Medisafe step 3 vs ours" wastes time
- **6 apps, not 50** — maintainable quarterly refresh, no stale noise

## Competitor Set

| App | Category | Why |
|-----|----------|-----|
| Medisafe | Direct | Market leader, new hard paywall |
| MyTherapy | Direct | Free B2B, UI polish without paywall pressure |
| CareClinic | Direct | Feature breadth anti-pattern |
| Flighty | Pattern ref | Hero + Live Activity gold standard |
| Huckleberry | Pattern ref | Family sync direct analog |
| How We Feel | Pattern ref | One-tap confirm + calm tone |

## Setup (one-time)

### 1. Create folder structure

```bash
mkdir -p DoseSync/competitors/{medisafe,mytherapy,careclinic,flighty,huckleberry,howwefeel,dosesync,reports}
for app in medisafe mytherapy careclinic flighty huckleberry howwefeel dosesync; do
    mkdir -p DoseSync/competitors/$app/{hero,paywall,onboarding,confirm-cta,empty-state,streak,family-feed}
done
```

### 2. Populate competitor screenshots

**Recommended:** Mobbin Pro subscription (~$29/mo).

Workflow per competitor:
1. Open Mobbin → search for app → browse flows
2. Screenshot-grab pattern screens, save to `competitors/<app>/<pattern>/NN_name.png`
3. Update metadata.yaml (last_updated, notes)

Takes ~30 min per app, do quarterly (~2 hours total).

**Free alternative for paywall/marketing screens:**
```bash
# Get Medisafe paywall screenshots from App Store
curl 'https://itunes.apple.com/lookup?id=920353840&country=us' \
  | jq -r '.results[0].screenshotUrls[]' \
  | xargs -I {} curl -o competitors/medisafe/paywall/{##} {}
```

### 3. Populate DoseSync screenshots

Use `/audit-ui` skill output → copy into `competitors/dosesync/<pattern>/`.

## Output format

HTML grid — CSS columns per app. Opens in any browser, diff-able in git, embeddable in Obsidian.

```
reports/2026-04-18_hero.html
├── Header: pattern name + date
├── Grid: [DoseSync | Medisafe | MyTherapy | Flighty | ...]
└── Observations section (Claude auto-writes 3-5 design takeaways)
```

Optional: `--export=png` generates shareable single-image composition via ImageMagick.

## Maintenance

- **Weekly:** refresh DoseSync via `/audit-ui` + copy to `competitors/dosesync/`
- **Quarterly:** refresh competitor screenshots (Mobbin browse session)
- **Annually:** re-evaluate competitor set

## Cost

- Mobbin Pro: ~$29/mo
- ImageMagick (optional): free (`brew install imagemagick`)
- iTunes Search API: free

## Roadmap

- **v1.0** (current): manual curation + HTML reports + ImageMagick export
- **v1.1:** iTunes Search API auto-refresh for public paywall screenshots
- **v1.2:** Obsidian vault sync via `vault-sync` skill
- **v2.0:** Pattern-level diff vs last comparison (change detection)

## Related

- `mapping.yaml` — full competitor config (IDs, URLs, roles)
- `/audit-ui` — generates DoseSync screenshots for comparison
- Mobbin: https://mobbin.com
