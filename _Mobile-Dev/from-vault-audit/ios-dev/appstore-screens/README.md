# appstore-screens — DoseSync Skill

Generates App Store preview screenshots via SwiftUI `ImageRenderer`. Produces PNGs at Apple-required resolutions with phone mockup + text overlay + brand gradient compositions.

## Quick Start

```
/appstore-screens
```

Claude Code will:
1. Verify `ScreenshotComposerView.swift` + `screenshot-specs.yaml` exist
2. Capture source screens from simulator (if missing)
3. Render 5 hero PNGs to `DoseSync/AppStoreAssets/screenshots/`
4. Validate dimensions + content guardrails
5. Print paths for upload to App Store Connect

## Output

5 hero PNGs at **1290 × 2796** (iPhone 6.9"):

| # | Slug | Story |
|---|------|-------|
| 1 | `coordination` | "Never guess if Mom took her pill" — family sync |
| 2 | `double-dose` | "No more double doses" — moat |
| 3 | `grandparent` | "Grandma stays in sync" — accessibility |
| 4 | `streaks` | "Your streak, your pace" — retention |
| 5 | `family-feed` | "Family log, one tap" — network effect |

## First-time Setup

Before first run, create Xcode target for rendering:

1. Add `DoseSync/DoseSync/AppStoreAssets/` group
2. Create `ScreenshotComposerView.swift` (template in SKILL.md)
3. Create `ScreenshotRenderer.swift` (template in SKILL.md)
4. Copy `screenshot-specs.yaml` to `AppStoreAssets/`
5. Optional: add a "Screenshot Rendering" Xcode Preview or CLI target

## Configuration

All content in `screenshot-specs.yaml`:

- **Headlines** — 3-6 words, bold, family emotional framing
- **Subtitles** — 0-8 words, supportive line
- **Backgrounds** — 4 brand gradients (mint-teal, teal-navy, warm-teal, sunrise)
- **Typography tokens** — 72pt/30pt from research

## Guardrails

Content is validated against `content_guardrails` in specs:

- No medication names (amoxicillin, tylenol, etc.)
- No dosage patterns (250mg, 5ml)
- No medical claims (clinically, FDA, proven)
- Mock data only (dependent name = "Sofia", not real)

## Requirements (Apple App Store 2026)

- **iPhone 6.9"** (1290×2796) — REQUIRED. Apple auto-scales to 6.5".
- **iPad 13"** (2064×2752) — Required ONLY if iPad build shipped.
- **6.5" / 5.5"** — No longer required since 2024.
- **File size:** < 8 MB per screenshot.

## Roadmap

- **v1.0** (current): iPhone 6.9" EN screenshots
- **v1.1**: Localized variants (RU, ES)
- **v1.2**: iPad 13" variants
- **v2.0**: A/B variant support, Apple Watch screenshots
- **v3.0**: Automated simulator navigation for source screens

## Related Docs

- `.claude/skills/copy-lint/` — validates text overlay copy against Guardrails
- `DoseSync-Brand-Voice-Guide.md` — headline/subtitle tone reference
- `DoseSync/DESIGN.md` — brand colors, typography scale
- `.claude/rules/conversion-framework.md` — App Store Landing Page section
