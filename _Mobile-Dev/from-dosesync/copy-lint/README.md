# copy-lint — DoseSync Copy Audit Skill

Audits DoseSync copy for Guardrails, Brand Voice, and localization health. Read-only — reports violations, never auto-fixes.

## Quick Start

```
/copy-lint
```

Claude Code will:
1. Read `rules.yaml`
2. Scan `Localizable.xcstrings` + `Views/` + `ViewModels/`
3. Write report to `DoseSync/copy-lint-report.md`
4. Print summary with top 3 P0 violations

## What it Checks

6 rule categories (see `rules.yaml` for full list):

| ID | Category | Severity |
|----|----------|----------|
| G1 | Medication names/dosages in push copy | **P0** |
| G2 | Medical claims anywhere | **P0** |
| G3 | Generic CTAs (Brand Voice mismatch) | P1 |
| G4 | Missing translations / button overflow | P1 |
| G5 | Guilt-shaming in notifications | P1 |
| G6 | Hardcoded strings in views | P2 |

## Tuning

All rules live in `rules.yaml`:

- Add banned medications: `g1_medical_guardrails.banned_medications`
- Add medical claim phrases: `g2_medical_claims.banned_phrases`
- Add branded CTA pairs: `g3_brand_voice.pairs`
- Adjust RU button length: `g4_localization.button_max_length.ru`

## Known False Positives

- **G1** may flag medication names in `medications_db.json` autocomplete — those are legitimate (bundled DB). Skill filters by `context_keys` prefix but manual review still recommended.
- **G2** may flag benign medical terminology (e.g., "dose", "medication") — keep `banned_phrases` list specific to actual claims.
- **G6** may flag legitimate debug-only strings — keep `skip_files` list up to date.

## Roadmap

- v1.0 (current): Scan + report, read-only
- v1.1: CI/JSON output for pipelines
- v1.2: `--fix` flag for G6 (hardcoded → key generation)
- v2.0: Context-aware grammar check via LLM (opt-in)

## Related Docs

- `$PROJECT_ROOT/DoseSync-Brand-Voice-Guide.md` — source for G3 rules
- `$PROJECT_ROOT/CLAUDE.md` — Guardrails (G1, G2)
- `$PROJECT_ROOT/DoseSync/DESIGN.md` — UI principles
- `$PROJECT_ROOT/DoseSync-UI-UX-Sprint-Plan-V2.md` — anti-patterns (G5)
