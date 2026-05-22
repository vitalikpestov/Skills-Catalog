# audit-ui — DoseSync Skill

Automated UI audit. Build + simulator navigation + 20 screenshots (5 screens × 4 states) + static code analysis + HTML report.

## Quick Start

```
/audit-ui
```

Claude Code will:
1. Build app + boot simulator
2. Install and launch DoseSync
3. Capture 20 screenshots across 4 state combinations
4. Run static analysis for 4 defect categories
5. Generate `DoseSync/audit-ui-report.html`

**Duration:** ~3-5 minutes for first run (build + 20 captures + analysis).

## States × Screens Matrix

|  | A: Light/Normal | B: Light/XXL | C: Dark/Normal | D: Dark/XXL |
|--|-----------------|--------------|----------------|-------------|
| Home | ✓ | ✓ | ✓ | ✓ |
| Meds | ✓ | ✓ | ✓ | ✓ |
| Dose Log | ✓ | ✓ | ✓ | ✓ |
| Family | ✓ | ✓ | ✓ | ✓ |
| Settings | ✓ | ✓ | ✓ | ✓ |

**20 screenshots total.**

## Defect Categories

| Severity | Category | What it catches |
|----------|----------|-----------------|
| High | Missing a11y label | Icon-only buttons without `.accessibilityLabel` |
| Medium | Touch target < 44pt | Fixed frames smaller than Apple HIG minimum |
| Medium | Hardcoded font size | `.font(.system(size: N))` that breaks Dynamic Type |
| Low | Direct black/white | `Color.white` / `.foregroundColor(.black)` — Dark Mode risk |

## Customization

All detection patterns + exempt files in `screens.yaml`:

- **Screens list** — add/remove screens (note: v1 only supports tab bar level)
- **States** — add intermediate Dynamic Type (normal/large/xxl) if needed
- **Whitelist** — add file paths that are intentionally exempt (marketing renders, decorative)
- **Detection patterns** — tune regex for each category

## Requirements

- Xcode 16+ with iPhone 17 simulator installed
- XcodeBuildMCP MCP server connected
- Session defaults configured (scheme, simulator)

## Roadmap

- **v1.0** (current): tab bar screens, 4 states, 4 static analysis categories
- **v1.1**: Sheet/modal navigation (Add Medication, Confirm, paywall)
- **v1.2**: Grandparent Mode separate audit
- **v2.0**: VoiceOver audit via XCUITest + pixel-level contrast measurement
- **v2.1**: Visual regression diff vs previous audit

## Related Skills

- `/copy-lint` — text audit (complements visual audit)
- `/appstore-screens` — marketing screenshot generation (different output, same infra)
- `/paywall-check` — focused paywall flow verification

## Troubleshooting

See SKILL.md "Troubleshooting" section for:
- Simulator boot failures
- Dark mode not applying
- Dynamic Type XXL ignored
- Tab coordinates mismatch
