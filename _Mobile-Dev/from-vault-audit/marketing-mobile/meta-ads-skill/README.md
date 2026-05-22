# 🎯 Meta Ads Expert — Claude Skill

> **Turn Claude into a senior Meta Ads consultant.** Campaign strategy, creative specs, audience targeting, competitor research, and performance data export — all powered by official Meta documentation and bundled API scripts.

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blueviolet?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==)](https://docs.anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Meta Ads](https://img.shields.io/badge/Meta_Ads-2025%2F2026-blue?style=flat-square&logo=meta)](https://www.facebook.com/business/ads)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

---

## Why This Exists

Running Meta Ads means juggling specs, policies, API docs, creative best practices, and platform changes that shift every few months. Most AI assistants give you generic advice or hallucinate outdated settings.

**This skill injects real, structured Meta Ads knowledge directly into Claude's context**, turning it into a specialist that knows:
- The exact image size for every placement (not "it depends")
- Current Advantage+ behavior and when to use it
- How to diagnose a tanking campaign step-by-step
- How to pull competitor ads programmatically via the Ad Library API
- How to export your campaign performance data via the Marketing API

Built for marketers, agencies, and developers who use Claude daily and want **accurate, actionable Meta Ads help** without switching tabs.

---

## What's Inside

```
meta-ads-expert/
├── SKILL.md                          # Skill definition + routing logic
├── references/                       # Curated knowledge base (85KB)
│   ├── strategy-and-objectives.md    # ODAX objectives, campaign structure, funnel mapping
│   ├── specs-and-formats.md          # Every ad format spec (image, video, carousel, etc.)
│   ├── targeting-and-audiences.md    # Custom/Lookalike audiences, Advantage+ Audience
│   ├── tracking-and-measurement.md   # Pixel, CAPI, EMQ, attribution windows
│   ├── policies-and-compliance.md    # Ad review, restrictions, special categories
│   ├── creative-strategy.md          # Hooks, UGC frameworks, testing methodology
│   ├── budget-and-scaling.md         # CBO vs ABO, learning phase, scaling playbooks
│   ├── ad-library-research.md        # Competitive research framework + API usage
│   └── campaign-insights-api.md      # Marketing API Insights: fields, breakdowns, exports
├── scripts/                          # Ready-to-run Python scripts (36KB)
│   ├── fb_ads_library_api.py         # Ad Library API client
│   ├── fb_ads_library_api_cli.py     # CLI wrapper for Ad Library queries
│   ├── fb_ads_library_api_operators.py
│   ├── fb_ads_library_api_utils.py
│   └── meta_campaign_insights.py     # Campaign Insights exporter (CSV/JSON)
```

---

## Features

### 📚 Knowledge Base (9 Reference Modules)

Each module is a deep, structured reference file that Claude reads on-demand based on what you ask:

| Module | Covers |
|--------|--------|
| **Strategy & Objectives** | 6 ODAX objectives, campaign structure, funnel-to-objective mapping, when to use what |
| **Specs & Formats** | Every ad format (image, video, carousel, collection, Instant Experience), dimensions, file limits, codec requirements |
| **Targeting & Audiences** | Custom Audiences, Lookalikes, Advantage+ Audience, interest stacking, exclusions, special ad categories |
| **Tracking & Measurement** | Meta Pixel setup, Conversions API (CAPI), Event Match Quality, attribution models, iOS 14.5+ impact |
| **Policies & Compliance** | Ad review process, common rejection reasons, restricted content, special categories (housing/credit/employment) |
| **Creative Strategy** | Hook frameworks (3-second rule), UGC best practices, ad fatigue signals, A/B testing methodology |
| **Budget & Scaling** | CBO vs ABO (now Advantage Campaign Budget), learning phase rules, vertical/horizontal scaling, bid strategies |
| **Ad Library Research** | Competitive intelligence framework + programmatic API access for bulk competitor analysis |
| **Campaign Insights API** | Full Marketing API Insights reference: 50+ metrics, breakdowns, date ranges, export formats |

### 🔧 Bundled Scripts

#### Ad Library API — Competitor Research
Programmatic access to Meta's Ad Library. Search any advertiser's active ads, filter by country/platform/media type, and export results for analysis.

```bash
# Search for active ads by a competitor
python scripts/fb_ads_library_api_cli.py \
  --access-token YOUR_TOKEN \
  --search-term "your competitor" \
  --country IT \
  --ad-type ALL
```

#### Campaign Insights Exporter — Performance Data
Export your own campaign data from the Marketing API. Supports every metric available in Ads Manager, with breakdowns, date ranges, and CSV/JSON output.

```bash
# Export last 30 days of campaign performance
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --date-preset last_30d \
  --level campaign \
  -o campaigns.csv

# Daily breakdown by age and gender at ad set level
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --level adset \
  --breakdowns age,gender \
  --time-increment 1 \
  -o demo_daily.csv
```

---

## Quick Start

### 1. Install the Skill

Copy the `meta-ads-expert/` folder into your Claude skills directory:

```bash
# If using Claude Desktop / Claude Code
cp -r meta-ads-expert/ ~/.claude/skills/meta-ads-expert/
```

### 2. Start Asking

Once installed, Claude automatically activates the skill when you ask about Meta Ads. Examples:

- *"What's the best campaign structure for a lead gen campaign spending €50/day?"*
- *"My ROAS dropped 40% this week — help me diagnose"*
- *"What image sizes do I need for a carousel ad on Instagram?"*
- *"Show me what my competitors are running on Facebook in Italy"*
- *"Export my last 30 days of ad performance broken down by age group"*

### 3. Use the Scripts (Optional)

For API-powered features, you'll need a [Facebook Developer access token](https://developers.facebook.com/tools/accesstoken/):

```bash
pip install requests
python scripts/fb_ads_library_api_cli.py --access-token YOUR_TOKEN --search-term "brand name" --country US
```

---

## Example Conversations

<details>
<summary><strong>🏪 "I run a barbershop and want to get more bookings through Instagram"</strong></summary>

Claude will:
1. Recommend the **Leads** objective with Instant Forms
2. Suggest vertical 9:16 Reels creative showing before/after transformations
3. Advise on local targeting radius + Advantage+ Audience
4. Provide exact specs (1080×1920px, MP4, < 30s)
5. Suggest €15-25/day starting budget with CBO
6. Offer to research competitor barbershop ads via the Ad Library

</details>

<details>
<summary><strong>📊 "My campaigns aren't converting anymore — what's wrong?"</strong></summary>

Claude will walk through a structured diagnostic:
1. Check if you're stuck in **learning phase** (< 50 conversions/week)
2. Evaluate **creative fatigue** signals (rising frequency, declining CTR)
3. Verify **tracking setup** (Pixel + CAPI, EMQ score)
4. Review **audience overlap** between ad sets
5. Check for **objective mismatch** (optimizing for traffic when you want sales)
6. Suggest an export of your campaign data to analyze trends

</details>

<details>
<summary><strong>🔍 "What ads are my competitors running?"</strong></summary>

Claude will:
1. Guide you through the Meta Ad Library search process
2. Offer to run the bundled API script for bulk results
3. Analyze creative patterns: formats, hooks, CTAs, messaging angles
4. Identify gaps and opportunities for differentiation
5. Suggest a testing framework based on findings

</details>

---

## Who Is This For

- **Solo marketers & freelancers** who want expert-level Meta Ads guidance inside their AI workflow
- **Agencies** looking to standardize Meta Ads knowledge across their team's Claude usage
- **Developers** building ad management tools who need a reliable reference layer
- **SMEs** (especially Italian market) running their own Facebook/Instagram campaigns
- **Claude skill builders** looking for a real-world example of a production-grade skill

---

## Built With Official Sources

All reference material is sourced from and cross-checked against:

- [Meta Business Help Center](https://www.facebook.com/business/help)
- [Meta Ads Guide](https://www.facebook.com/business/ads-guide)
- [Meta Marketing API Docs](https://developers.facebook.com/docs/marketing-api)
- [Meta Ad Library](https://www.facebook.com/ads/library/)
- [Meta Blueprint](https://www.facebookblueprint.com/)

No hallucinated specs. No outdated settings. Real documentation, structured for LLM consumption.

---

## Contributing

Contributions are welcome! Meta's ad platform changes frequently, so help keeping this current is appreciated.

**Ways to contribute:**
- 🐛 Report outdated specs or incorrect information
- 📝 Add coverage for new Meta features (Threads ads, new Advantage+ options, etc.)
- 🔧 Improve or extend the bundled scripts
- 🌍 Add localization notes for other markets
- 📖 Improve reference documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Roadmap

- [ ] A/B test result analyzer script
- [ ] Budget allocation calculator
- [ ] Multi-market campaign planner reference
- [ ] Integration with Meta's Marketing API for real-time optimization suggestions

---

## License

MIT — use it, fork it, improve it.

---

## Star History

If you downloaded this skill, consider leaving a ⭐

---

<p align="center">
  <b>Built by <a href="https://github.com/giacomoarienti">Giacomo Arienti</a></b> 🇮🇹
</p>
