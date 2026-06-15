---
name: copy-lint
description: "Audits DoseSync copy for Guardrails violations, Brand Voice compliance, and localization health. Use this skill when the user asks to lint copy, check strings, audit Localizable, run copy-lint, check Guardrails, validate push notifications, check for medical claims, or verify brand voice in iOS strings. Scans Localizable.xcstrings and all SwiftUI views for 6 categories of violations (medical guardrails, medical claims, brand voice, localization health, guilt-shaming, hardcoded strings) and generates a Markdown report."
---

# Copy Lint — DoseSync

Audits DoseSync copy against internal Guardrails, Brand Voice Guide, and localization rules. **Read-only** — reports violations, does not auto-fix.

## When to invoke

- User says: "copy-lint", "check strings", "audit localizable", "check guardrails", "validate push copy", "check brand voice"
- After Brand Voice Guide updates, to verify all strings aligned
- Before TestFlight submission, as part of QA pipeline
- After adding new features, to catch hardcoded strings

## 6 Violation Categories

| ID | Category | Severity | Example |
|----|----------|----------|---------|
| **G1** | Medical name/dosage in push copy | **P0 (legal)** | `"Time for Emma's Amoxicillin 250mg"` |
| **G2** | Medical claims in any copy | **P0 (legal)** | `"Clinically proven to prevent complications"` |
| **G3** | Generic CTA not matching Brand Voice | P1 | `"Give Dose"` instead of `"Yes, I gave it"` |
| **G4** | Localization health (missing/overflow) | P1 | RU value empty or > 30 chars in button context |
| **G5** | Guilt-shaming in notifications | P1 | `"You missed a dose!"` instead of `"Missed — log it now?"` |
| **G6** | Hardcoded strings in views | P2 | `Text("Settings")` instead of `Text("settings_title")` |
| **G7** | RU «Вы»-form violations | P1 | Delegated to `scripts/check_ru_tone.py` |

## Execution Steps

Run these in order:

### Step 1: Load rules

Read `.claude/skills/copy-lint/rules.yaml` — contains all banned terms, phrases, brand voice pairs, and locale limits.

### Step 2: Scan Localizable.xcstrings

File: `DoseSync/DoseSync/Localizable.xcstrings`

For each key:
1. Extract `en` and `ru` values
2. Identify **context** from key prefix:
   - `notif_*` → push notification (apply G1, G2, G5)
   - `*_button`, `*_cta`, `home_give_*` → CTA (apply G3, G4)
   - everything → apply G2, G6 checks
3. Check each value against rules in `rules.yaml`
4. Collect violations with file line numbers

**Note:** Some `medications_db.json` names ARE legitimate (bundled DB for autocomplete). G1 only flags medication names in **notification keys** (prefix `notif_`) and **push-related** keys, NOT in medication database entries.

### Step 3: Grep Views for hardcoded strings

Run: `grep -rn 'Text("[A-Z]' DoseSync/DoseSync/Views/ --include="*.swift"`

For each match:
- Skip if inside `#Preview` block (test strings OK)
- Skip if inside `accessibilityLabel` (those are audited separately)
- Skip if string starts with localization key pattern (lowercase + underscore)
- Skip if it's a `String(localized:)` pattern
- Flag everything else as G6 violation

### Step 3.5: Run RU tone check (G7)

Run: `cd DoseSync && python3 scripts/check_ru_tone.py`

This script verifies all RU strings use «Вы»-form (never «ты»). It's maintained separately in the project and already covers this category better than rule-based patterns.

Capture its output:
- `exit 0` + `"zero violations"` → G7 clean, report as ✓
- `exit 1` + list of violations → include each in G7 section of report

### Step 3.6: Apply skip_contexts and allowed_strings

Before writing violations to report, filter using `rules.yaml`:

- **G2.skip_contexts:** if violation key matches `key_prefix` AND value contains `allowed_phrases` → drop the violation (log as "false positive filtered")
- **G5.skip_contexts:** same pattern — paywall_* keys with "Don't lose track" are exempt
- **G6.allowed_strings:** if hardcoded string exactly matches any in `allowed_strings` list → drop
- **G6.skip_files:** if file path matches pattern (supports `*` wildcard) → drop all violations from that file

Count filtered violations separately in report summary as "false positives filtered".

### Step 4: Generate report

Write to `DoseSync/copy-lint-report.md` with structure:

```markdown
# Copy Lint Report — DoseSync

**Date:** YYYY-MM-DD
**Rules version:** X.Y (from rules.yaml)
**Total violations:** N (P0: N, P1: N, P2: N)

## Summary

| Category | P0 | P1 | P2 | Total |
|----------|----|----|----|-------|
| G1 Medical guardrails | N | 0 | 0 | N |
...

## P0 Violations (fix before launch)

### G1: Medical name in push copy

**File:** `Localizable.xcstrings:12345`
**Key:** `notif_dose_reminder_body`
**Value (en):** "Time for Emma's Amoxicillin 250mg"
**Problem:** Contains "Amoxicillin" + dosage "250mg"
**Fix:** Replace with "Time for Emma's morning dose"

---

## P1 Violations

...

## P2 Violations

...

## Clean categories

G5 (guilt-shaming): 0 violations ✓
```

### Step 5: Summary to user

Print concise summary:
- Total count by severity
- Top 3 critical files
- Path to full report
- Exit: suggest which P0/P1 to fix first

## Output format for user message

```
Copy Lint complete — N violations found.

P0 (legal risk): N
  - G1 medical names: N in X files
  - G2 medical claims: N in X files

P1 (brand/locale): N
  - G3 generic CTAs: N
  - G4 locale overflow: N
  - G5 guilt-shaming: N

P2 (hygiene): N
  - G6 hardcoded strings: N in X views

Full report: DoseSync/copy-lint-report.md

Start with: [top 3 P0 items]
```

## Rules extension

Rules live in `rules.yaml`. To add/edit:

- **G1 banned_medications:** list of active ingredient names (lowercase). Add brand names as needed.
- **G1 dosage_regex:** regex for dosage patterns.
- **G2 medical_claims:** phrases that trigger violation (case-insensitive).
- **G3 brand_voice_pairs:** `from → to` pairs from Brand Voice Guide.
- **G4 button_max_length_ru:** integer, RU button length warning threshold.
- **G5 guilt_patterns:** phrases + regex patterns for guilt-shaming detection.

## What this skill does NOT do

- **Does not translate** — use `xcstrings-localizer` for translation
- **Does not auto-fix** — read-only v1, user makes changes manually
- **Does not check grammar** — rule-based only, no LLM grammar check
- **Does not check context appropriateness** — only pattern matches

## Limitations and caveats

- **False positives expected** on G1/G2: some medical terminology is needed in pill counter, prescription scan flows. Review each G1/G2 flag manually before fixing.
- **G6 may flag legitimate strings** in debug/internal views — check context before converting to localized keys.
- **RU overflow (G4)** is heuristic — some languages naturally have longer strings; confirm visually in simulator at max Dynamic Type.
