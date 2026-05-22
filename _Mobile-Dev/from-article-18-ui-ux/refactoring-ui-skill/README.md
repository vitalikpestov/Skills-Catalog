# Refactoring UI - Claude Code Skill

A Claude Code skill that teaches AI to build better UIs using tactical design principles from [Refactoring UI](https://www.refactoringui.com/).

> **Why this matters:** AI can write functional code but often produces generic, poorly designed interfaces. This skill gives Claude Code a design system and tactical rules to follow, resulting in more professional UIs.

## What's Inside

```
.claude/
├── skills/ui-refactor/
│   ├── SKILL.md              # Main skill definition
│   └── references/
│       ├── hierarchy.md      # Visual hierarchy tactics
│       ├── layout-spacing.md # Spacing systems & grids
│       ├── typography.md     # Type scales & fonts
│       ├── color.md          # HSL palettes & contrast
│       └── depth-and-polish.md # Shadows & finishing touches
│
└── commands/                 # Slash commands for quick fixes
    ├── ui-refactor.md
    ├── fix-hierarchy.md
    ├── fix-typography.md
    ├── fix-layout.md
    └── fix-colors.md
```

## Usage

1. Copy the `.claude` folder to your project root
2. Ask Claude Code to build UI or use the skill directly:

```
/ui-refactor Create a dashboard with stats cards and a data table
```

Or just describe what you want:

```
"Build me a pricing page with three tiers"
"Make this form look more professional"
"Fix the visual hierarchy on this card component"
```

## Key Principles

The skill enforces these tactical rules:

- **No arbitrary values** - Uses defined spacing scales (4, 8, 12, 16, 24, 32, 48, 64px)
- **Hand-picked type scales** - Not ratio-based (12, 14, 16, 18, 20, 24, 30, 36px)
- **HSL colors** - With proper saturation curves and hue rotation for shades
- **Visual hierarchy** - Through weight and color, not just size
- **Elevation system** - Defined shadow levels for consistent depth

## Example Output

The `/design` folder contains an example dashboard built using this skill:

- `index.html` - Dashboard with sidebar, stats, charts, and data table
- `styles.css` - Complete design system with CSS custom properties
- `script.js` - Interactive functionality

[Live Demo](https://lovropodobnik.github.io/refactoring-ui-skill/design/)

## Credits

Design principles from [Refactoring UI](https://www.refactoringui.com/) by Adam Wathan & Steve Schoger. This skill is a distillation of their book into actionable rules for AI code generation.

---

*Built with Claude Code*
