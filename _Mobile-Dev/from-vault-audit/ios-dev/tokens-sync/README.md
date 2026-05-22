# tokens-sync — DoseSync Skill

Design token sync + audit. Validates `DesignTokens.swift` ↔ `Assets.xcassets` consistency and optionally syncs from Figma Variables.

## Quick Start

### Mode A — Validate only (no Figma needed)

```
/tokens-sync
```

Audits:
- Swift token refs without colorset (build break risk)
- Orphan colorsets (candidates for deletion)
- Missing dark variants (Dark Mode risk)
- Hardcoded hex values in Views (token violation)

### Mode B — Sync from Figma

```
/tokens-sync figma=abc123XYZ
```

Additionally reads Figma Variables and updates colorset hex values.

## Prerequisites

### Mode A
- `DoseSync/DoseSync/Utilities/DesignTokens.swift` exists
- `DoseSync/DoseSync/Assets.xcassets/` has `ds.*.colorset/` entries

### Mode B
- All of Mode A, plus:
- Figma file with Variables set up (not just "local styles")
- `use_figma` MCP connected
- `mapping.yaml` updated with your Figma variable names

## Configuration

### `mapping.yaml`

Maps Figma Variable names → Swift colorset names:

```yaml
mappings:
  - figma: "color/accent/primary"
    swift: "accent"
  # ...
```

Edit this when your Figma structure differs from the default.

### Persistent fileKey

To run Mode B without args every time, set `figma_file_key` in `mapping.yaml`:

```yaml
figma_file_key: "YOUR_KEY"
figma_page_name: "Design System"
```

## Output

`DoseSync/tokens-sync-report.md` — validation results + applied updates.

## Safety

- Never writes malformed JSON
- Never deletes colorsets (only updates values)
- Tolerance ±2 per RGB channel prevents false "changed" from float imprecision
- Mode B is read-only if no changes detected

## Roadmap

- **v1.0** (current): validate + Figma → Code sync for colors
- **v1.1**: Handle `overlayDim` and other custom tokens
- **v1.2**: Code → Figma sync (reverse direction)
- **v2.0**: Typography, spacing, corner radius tokens
- **v2.1**: YAML as source of truth (generate Swift)

## Related

- `DesignTokens.swift` — canonical token definitions
- `Assets.xcassets/ds.*.colorset/` — color values
- `Color+Hex.swift` — hex utility (exempt from hardcoded-hex check)
- `figma-ios-design-pipeline` skill — full Figma design workflow
