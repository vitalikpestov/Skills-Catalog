---
name: seo-email-funnel
description: "DoseSync SEO Email Funnel Builder. Takes a list of caregiver questions + voice interview transcripts, generates a full content package per question: SEO blog post (markdown), lead magnet spec, pre-launch email nurture sequence (JSON), and analytics/UTM recommendations. Invoke when Vitalik says 'build funnel for question', 'generate blog + emails for [topic]', or 'run seo-email-funnel'."
---

# SEO Email Funnel Builder — Workflow

## Prerequisites

```bash
cd $PROJECT_ROOT/.claude/skills/seo-email-funnel
pip install -r requirements.txt   # optional: only needed for standalone API mode
```

**Two run modes:**
- **Native (default):** Claude Code generates content directly — no API key needed. Python handles guardrails + file I/O.
- **Standalone:** Set `ANTHROPIC_API_KEY` + run `python3 example_usage.py` — fully autonomous.

## How to Run

### Option A — Native in Claude Code (no API key)

Provide `QuestionInput` data in the conversation. Claude Code runs the pipeline:
1. Python: guardrails on transcript
2. Claude Code: generates SEO outline, interview blocks, blog post, lead magnet, email funnel
3. Python: analytics recommendations + saves all artifacts to `output/`

### Option B — Standalone Python (batch mode)

Edit `example_usage.py` with your questions and transcripts, then:

```bash
ANTHROPIC_API_KEY=sk-... python3 example_usage.py
```

### Option C — Inline Python (single question)

```python
from input_models import QuestionInput, SkillConfig
from skill import run_skill

q = QuestionInput(
    id="q001",
    raw_question="How to prevent double-dosing?",
    topic_cluster="double_dosing",       # double_dosing | grandparents | adhd_kids | burnout | other
    persona_segment="sandwich_caregiver", # sandwich_caregiver | young_parent | grandparent | professional_caregiver | other
    interview_transcript="[paste your voice memo transcript here]",
    language="en",  # "en" or "ru"
)

config = SkillConfig(
    launch_date="2026-08-04",
    article_length="medium",    # short | medium | long
    emails_count=5,
    product_integration_level="medium",  # light | medium | strong
    output_dir="output",
)

result = run_skill([q], config)
```

## Outputs (saved to `output/`)

| File | Content |
|------|---------|
| `blog_{id}_{slug}.md` | Full SEO article, markdown |
| `lead_magnet_{id}_{slug}.md` | Lead magnet spec + opt-in copy |
| `email_funnel_{id}.json` | Nurture sequence + launch broadcast |
| `analytics_{id}.json` | Segments, PostHog events, UTM params |
| `meta.json` | Index of all generated artifacts |

## Module Map

```
skill.py                 ← entry point: run_skill()
input_models.py          ← QuestionInput, SkillConfig dataclasses
guardrails.py            ← medical content safety filter
seo_analysis.py          ← SEO outline + keyword via Claude API
interview_parser.py      ← transcript → structured content blocks
blog_generator.py        ← full article markdown via Claude API
lead_magnet_generator.py ← lead magnet type + copy via Claude API
email_funnel_generator.py ← nurture sequence + launch broadcast via Claude API
analytics_recommender.py ← Resend tags, PostHog events, UTM recs (pure Python)
io_utils.py              ← saves all artifacts to disk
```

## Config Reference

| Field | Default | Options |
|-------|---------|---------|
| `launch_date` | `"2026-08-04"` | any ISO date |
| `article_length` | `"medium"` | `short`=800w / `medium`=1500w / `long`=2500w |
| `emails_count` | `5` | 1–5 |
| `product_integration_level` | `"medium"` | `light` (1 mention) / `medium` (2-3) / `strong` (woven throughout) |
| `model` | `"claude-sonnet-4-6"` | any Anthropic model ID |
| `output_dir` | `"output"` | any path |

## Guardrails (always active)

- Drug names auto-anonymised → `[medication]`
- Forbidden phrases removed: "clinically proven", "cures", "лечит", etc.
- Disclaimer auto-appended to every blog post and launch email
- "Вы"-form enforced for Russian content (tone-of-voice rule)

## Adding a New Question

1. Create `QuestionInput` with unique `id`, paste transcript, pick cluster + persona
2. Run `run_skill([q], config)`
3. Check `output/meta.json` for artifact paths
4. Blog post → publish; lead magnet → upload to Resend/landing; funnel JSON → import to email platform
