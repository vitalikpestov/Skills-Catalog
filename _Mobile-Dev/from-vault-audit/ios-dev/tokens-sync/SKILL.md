---
name: tokens-sync
description: "Syncs design tokens between Figma Variables and DoseSync DesignTokens.swift + Assets.xcassets. Two modes: (1) validate-only — audits consistency of Swift tokens vs Asset Catalog colorsets (works without Figma), (2) figma-sync — reads Figma Variables via use_figma MCP and updates colorset hex values. Use this skill when the user asks to sync tokens, validate design tokens, check token consistency, sync colors from Figma, verify asset catalog, or audit DesignTokens.swift. Outputs tokens-sync-report.md with diff of changed/unchanged/mismatched tokens."
---

# Tokens Sync — DoseSync

Design token audit + Figma sync. Validates consistency of `DesignTokens.swift` ↔ `Assets.xcassets/ds.*.colorset/` and optionally syncs from Figma Variables.

## When to invoke

- `/tokens-sync`, "sync tokens", "validate design tokens"
- "check asset catalog", "audit colorsets"
- "sync colors from Figma"
- Before TestFlight — verify no orphan tokens, no missing dark mode pairs
- After design updates in Figma

## Two Modes

### Mode A: Validate-only (default, no Figma needed)

Audits internal consistency:
1. Every `Color.DS.xxx` in `DesignTokens.swift` has matching `ds.xxx.colorset/` in Asset Catalog
2. Every `ds.xxx.colorset/` has both light + dark appearance defined
3. No orphan colorsets (defined but not referenced in Swift)
4. No hardcoded hex colors outside `DesignTokens.swift` / `Color+Hex.swift`

### Mode B: Figma → Code sync (requires fileKey)

Additionally:
1. Reads Figma Variables via `use_figma` MCP tool
2. Maps Figma names to Swift names via `mapping.yaml`
3. Computes diff: which colors changed
4. Updates `Contents.json` in each matched colorset (light + dark values)
5. Reports unchanged / updated / mismatched

Mode B is invoked when user provides fileKey:
```
/tokens-sync figma=abc123XYZ
```

## Execution Steps

### Step 1: Determine mode

- If user message or args contain `figma=<fileKey>`: Mode B
- Otherwise: Mode A (validate-only)

### Step 2: Read Swift tokens

Parse `DoseSync/DoseSync/Utilities/DesignTokens.swift`:

```swift
extension Color {
    enum DS {
        static let background       = Color("ds.background")
        // ...
    }
}
```

Extract all `Color("ds.xxx")` references → set of expected colorset names: `{ds.background, ds.surface, ds.accent, ...}`.

### Step 3: List Asset Catalog colorsets

```bash
ls DoseSync/DoseSync/Assets.xcassets/ | grep '\.colorset$'
```

For each, read `Contents.json`:
```json
{
  "colors": [
    { "appearances": [...], "color": { "color-space": "srgb", "components": { "red": "0.29", "green": "0.63", "blue": "0.59", "alpha": "1.0" } } }
  ]
}
```

Extract:
- Name (from directory)
- Has light variant? (entry without `appearances` or with `luminosity:light`)
- Has dark variant? (entry with `luminosity:dark`)
- Hex values for light + dark (convert RGB components to hex)

### Step 4: Audit (Mode A + B)

Build 4 diff lists:

1. **Swift refs without colorset** — `Color("ds.xxx")` in code but no `ds.xxx.colorset/` exists. **Critical** — build will fail or show default fallback.

2. **Colorsets without Swift ref** — `ds.xxx.colorset/` exists but no `Color("ds.xxx")` in Swift. Not critical but orphan — candidate for deletion.

3. **Colorsets missing dark variant** — has light only. Flagged as "dark mode risk".

4. **Hardcoded hex outside tokens** — grep for `Color(hex:` or `#[0-9A-F]{6}` in `Views/`, `ViewModels/`. Each hit = potential token violation (should use `Color.DS.xxx` instead). Allow list: `Color+Hex.swift`, `AppStoreAssets/`, `MilestoneShareCardView.swift`.

### Step 5 (Mode B only): Read Figma

```
use_figma.get_variables({ fileKey: $FIGMA_KEY })
```

Extract color variables. For each:
- Figma name (e.g., `color/accent/primary`)
- Light mode value (hex)
- Dark mode value (hex, if defined)

### Step 6 (Mode B only): Map Figma → Swift

Load `mapping.yaml`:
```yaml
mappings:
  - figma: color/accent/primary
    swift: ds.accent
  - figma: color/accent/muted
    swift: ds.accentMuted
  - figma: color/semantic/success
    swift: ds.success
  # ...
```

For each mapping:
- Figma value exists + Swift colorset exists → compare hex
- Figma value exists + Swift missing → "Swift needs new colorset" (manual action)
- Swift exists + no Figma mapping → "Orphan Swift token" (consider adding to Figma)

### Step 7 (Mode B only): Apply updates

For each matched pair where Figma hex ≠ Swift hex:
- Read `ds.xxx.colorset/Contents.json`
- Update red/green/blue values for matching appearance (light/dark)
- Write back with 2-space indent

**Safety check:** before writing, verify structure integrity. Never write malformed JSON.

### Step 8: Generate report

Write `DoseSync/tokens-sync-report.md`:

```markdown
# Tokens Sync Report — DoseSync

**Date:** YYYY-MM-DD
**Mode:** [A validate-only | B figma-sync]
**Figma fileKey:** {if mode B}
**Swift tokens:** N
**Colorsets:** N

## Summary

| Check | Count | Status |
|-------|-------|--------|
| Swift refs with matching colorset | N | ✓ |
| Swift refs without colorset | N | ⚠ if > 0 |
| Orphan colorsets (no Swift ref) | N | ⚠ if > 0 |
| Colorsets missing dark variant | N | ⚠ if > 0 |
| Hardcoded hex in Views | N | ⚠ if > 0 |
{Mode B: |
| Figma matches Swift | N | ✓ |
| Figma differs from Swift | N | (updates applied) |
| Figma not in mapping | N | manual action |
}

## Details

### Swift tokens referenced
- ds.background ✓
- ds.surface ✓
...

### Orphan colorsets (candidate for deletion)
- ds.oldColor

### Missing dark variant
- ds.xxx — only light defined

### Hardcoded hex violations
- ViewName.swift:42 — `Color(hex: "#FF5733")` → should use Color.DS.?

{Mode B:
## Figma Updates Applied
- ds.accent: #2C7A7B → #1A8A7F (light), #4A9782 → #2A8A7F (dark)
...
}
```

### Step 9: Summary to user

```
Tokens Sync [mode] complete.

Swift tokens: N
Colorsets: N
Issues: N

{if issues > 0:}
Top 3 to fix:
1. {issue}
2. {issue}
3. {issue}

{if Mode B:}
Figma updates: N applied
- ds.accent (light): #2C7A7B → #1A8A7F
- ...

Report: DoseSync/tokens-sync-report.md
```

## Example invocations

**Validate-only:**
```
/tokens-sync
```

**Figma sync:**
```
/tokens-sync figma=abc123XYZ
```

**Figma sync with specific page:**
```
/tokens-sync figma=abc123XYZ page="Design System"
```

## Current DoseSync tokens (as of 2026-04-18)

From `DesignTokens.swift`:

| Swift key | Purpose |
|-----------|---------|
| `ds.background` | Screen background |
| `ds.surface` | Card backgrounds |
| `ds.surfaceSecondary` | Nested/grouped cards |
| `ds.textPrimary` | Primary text |
| `ds.textSecondary` | Secondary text, timestamps |
| `ds.accent` | Brand color, primary actions |
| `ds.accentMuted` | Unselected chips |
| `ds.separator` | Dividers |
| `ds.destructive` | Delete buttons |
| `ds.success` | Given status, confirmations |
| `ds.warning` | Late status |
| `ds.danger` | Missed status, errors |
| `ds.muted` | Pending/Skipped, disabled |

**13 colorsets expected.** Run `/tokens-sync` to verify all present with light + dark variants.

## What this skill does NOT do

- Does not translate / rename tokens — only updates values
- Does not create new tokens from Figma — manual action required
- Does not handle non-color tokens (spacing, typography) in v1 — future work
- Does not update Swift code — only Asset Catalog JSON

## v2 roadmap

- **v1.1:** Add `overlayDim` if not in current set (noticed in FirstDoseCelebrationView linter refactor — `Color.DS.overlayDim` referenced but need to verify it exists)
- **v1.2:** Bi-directional sync (Code → Figma for tokens added in Swift first)
- **v2.0:** Non-color tokens: typography sizes, spacing scale, corner radius
- **v2.1:** Auto-generate `DesignTokens.swift` from YAML source (source of truth)

## Troubleshooting

**Malformed Contents.json:** skill refuses to write. Check original JSON is valid.

**Figma Variables API returns empty:** verify fileKey + page name. Some Figma files use "local styles" instead of "variables" — not compatible with this skill in v1.

**Hex conversion off by 1:** floating point imprecision. Acceptable tolerance: ±0.01 per channel (roughly ±2 on 0-255 scale).
