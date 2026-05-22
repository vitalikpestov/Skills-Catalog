---
name: i18n-translator
description: Claude-powered FR/ES translation pipeline for DoseSync Localizable.xcstrings with brand voice injection, formality enforcement («vous»/«usted»), and medical-compliance guardrails. Pilot mode runs 50 curated strings for calibration; full mode processes ~2,235 strings in batches with human spot-check. Use when user asks "translate strings", "run i18n pilot", "BUG-002", "BUG-004", or "prepare FR/ES localization".
---

# i18n-translator — Claude API Translation Pipeline

## When to invoke

- PM asks to run i18n pilot or full translation (BUG-002 / BUG-004 from QA Remediation Plan)
- Need to translate new batches of Localizable.xcstrings strings to FR / ES
- Quality-check existing FR / ES translations against brand voice + tone-of-voice rules

## Why in-house Claude > generic vendor

1. **Brand voice consistency** — prompts inject `DoseSync-Brand-Voice-Guide.md` + `.claude/rules/tone-of-voice.md` («Вы»-equivalent «vous»/«usted»).
2. **Medical guardrails** — refuses prescriptive medical language that вендор может пропустить (см. `.claude/skills/copy-lint/` categories).
3. **Cost** — Claude API ~$0.01/string × 2,235 ≈ $25. Fiverr professional ≈ $200-400. Lokalise ≈ $500-750.
4. **Iteration speed** — recalibration = prompt edit, not vendor rebriefing.
5. **Context awareness** — знает медицинский домен DoseSync (double-dose, caregivers, family space) без брифа.

## Pipeline Phases

### Phase 1 — Pilot (50 strings, 2-3h, $30-50 human review)

**Goal:** калибровать prompt quality. Deadline 2026-04-29.

**Steps:**

1. **String selection** — взять 50 репрезентативных ключей:
   - 10× CTA (Confirm, Skip, Add medication, Get started, …)
   - 10× onboarding (welcome copy, step labels, trust messages)
   - 10× push notifications (dose reminder, missed, confirmed-by-other, trial-ending, weekly-digest)
   - 10× error messages (network, auth, sync failures)
   - 10× edge-case (empty states, paywall CTAs, legal, accessibility labels)

2. **Extract** через `scripts/extract_pilot_strings.py` (создать если нет) — читает `DoseSync/Localizable.xcstrings`, выплёвывает JSON:
   ```json
   [
     {"key": "dose_confirm_cta", "en": "Confirm dose", "context": "Primary CTA on HeroNextDoseCard"},
     ...
   ]
   ```

3. **Prompt template** — см. `translator-prompt.md` (создаётся этим skill'ом). Инструкции:
   - Форма обращения: formal «vous» (FR) / «usted» (ES)
   - Max length preserved (±10% relative to EN)
   - No medical prescription language
   - Preserve `%@`, `%lld`, `%1$@` placeholder markers verbatim
   - Preserve emoji и специальные символы
   - Brand voice: direct, empathetic, zero jargon

4. **Run** via Claude API (claude-sonnet-4-6, prompt caching enabled per `.claude/skills/claude-api/`). Batch 50 strings one request per locale = 2 requests total. Output JSON:
   ```json
   [
     {"key": "dose_confirm_cta", "en": "Confirm dose", "fr": "Confirmer la dose", "es": "Confirmar dosis", "notes": "..."},
     ...
   ]
   ```

5. **Human review** — Fiverr professional FR native + ES native reviewer. Budget $15-25 each для 50 строк. Brief: verify naturalness + brand fit + medical accuracy. Score each string 1-5.

6. **Calibration decision:**
   - Average score ≥ 4.5 → Phase 2 full run
   - 4.0-4.5 → iterate prompt (2-3 rounds), re-pilot subset
   - < 4.0 → pivot to Fiverr professional translation for full scope

### Phase 2 — BUG-002: 20 permission strings (1h)

**Scope:** 5 keys × 2 locales × 2 fields (NSHealthShareUsageDescription, NSHealthUpdateUsageDescription, NSCameraUsageDescription, NSPhotoLibraryUsageDescription, NSUserNotificationsUsageDescription) × FR+ES = 20 strings.

**Deadline:** 2026-05-15.

**Special rules for permission strings:**
- Apple rejects vague permission rationales — must explain WHY app needs the permission in concrete user benefit
- Max 175 characters per Apple HIG
- No marketing language — only functional explanation

**Steps:** extract от [Info.plist](../../../DoseSync/Info.plist) → prompt → Claude → 2-pass human review (permissions are reject-risk).

### Phase 3 — BUG-004: ~2,235 UI strings (8-16h runtime, $200-400 human review)

**Scope:** 1,159 FR + 1,076 ES strings per REMEDIATION-PLAN.md.

**Deadline:** 2026-06-01 (≥95% coverage).

**Batch strategy:**
- Split into batches of 50-100 strings (prompt token limit + iteration speed)
- Group by UI context (onboarding, paywall, home, family, settings, error, accessibility)
- Parallel FR + ES runs (can share same extraction pipeline)

**Quality gate:**
- Automated: placeholder preservation check (all `%@` in EN present in FR+ES) via `scripts/validate_xcstrings.py`
- Automated: max-length check (±10% EN)
- Automated: copy-lint pass (see `.claude/skills/copy-lint/`)
- Manual: spot-check 10% random sample by Fiverr native reviewers

### Phase 4 — Ingest back to xcstrings

**Goal:** atomic commit all translated strings into `DoseSync/Localizable.xcstrings`.

**Steps:**
1. Convert output JSON → xcstrings format (`scripts/json_to_xcstrings.py`)
2. Merge with existing (preserve any hand-translated overrides via `state: "translated"` marker)
3. Build verify: `xcodebuild -project DoseSync.xcodeproj build` — no missing translation warnings
4. CI check: `scripts/check_ru_tone.py` equivalent for FR/ES (formal address enforcement)
5. Commit: `feat(i18n): BUG-004 FR+ES UI translation (N strings)`

## Prompt Template (core)

Location: `.claude/skills/i18n-translator/translator-prompt.md` (created on first run).

Key sections:
- Role definition (medical app localizer)
- Brand voice injection (DoseSync-Brand-Voice-Guide.md excerpt)
- Formality rule (vous/usted)
- Placeholder preservation instructions
- Output format (JSON with en/fr/es/notes)
- Medical language guardrails (no prescriptions, no medical claims)

## Success Metrics

| Metric | Target |
|--------|--------|
| Pilot average quality score | ≥ 4.5 / 5 |
| BUG-002 Apple approval rate | 100% (0 rejections on permission copy) |
| BUG-004 coverage | ≥ 95% of EN keys (deadline 2026-06-01) |
| Placeholder preservation | 100% (automated check) |
| Budget total | ≤ $150 (Claude API + human review) |
| Time savings vs manual | ~80% vs translating 2,235 strings manually |

## Files

- `SKILL.md` — this file
- `translator-prompt.md` — core prompt (generated on first pilot run)
- `extract_pilot_strings.py` — xcstrings → JSON extractor (generated as needed)
- `validate_xcstrings.py` — post-translation QA (generated as needed)
- Output logs: `DoseSync/i18n-pilot-YYYY-MM-DD.json`

## References

- QA Remediation Plan: `DoseSync-qa/QA/Audit-v1.0/REMEDIATION-PLAN.md` (BUG-002, BUG-004)
- Brand Voice: `DoseSync/DoseSync-Brand-Voice-Guide.md`
- Tone of Voice: `DoseSync/.claude/rules/tone-of-voice.md`
- Copy Lint: `.claude/skills/copy-lint/SKILL.md`
- Claude API: `.claude/skills/claude-api/`
