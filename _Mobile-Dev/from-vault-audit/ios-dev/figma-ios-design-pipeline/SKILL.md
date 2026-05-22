---
name: figma-ios-design-pipeline
description: "Full iOS design pipeline in Figma via Plugin API: create screens from scratch, audit/fix existing designs, ensure Light/Dark parity, check WCAG AA accessibility, prepare designer handoff with Cover frame and labels, generate ТЗ as DOCX. Use this skill ALWAYS when the user asks to: build iOS screens in Figma, audit Figma designs, fix broken Figma frames, create Light and Dark mode pairs, check accessibility contrast, prepare Figma handoff, generate design ТЗ/spec document, create iOS widgets or components in Figma, or do any Figma Plugin API work for mobile app design. Also trigger when user mentions Figma + iOS, Figma audit, design QA, screen parity, or design handoff."
---

# Figma iOS Design Pipeline

End-to-end workflow for building, auditing, and handing off iOS app designs in Figma — entirely through the Plugin API (`use_figma` MCP tool). Battle-tested on a real production app with 57+ screens.

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Figma API Golden Rules](#2-figma-api-golden-rules)
3. [Creating Screens from Scratch](#3-creating-screens-from-scratch)
4. [Auditing Existing Designs](#4-auditing-existing-designs)
5. [Light/Dark Parity](#5-lightdark-parity)
6. [WCAG AA Accessibility](#6-wcag-aa-accessibility)
7. [Handoff Preparation](#7-handoff-preparation)
8. [ТЗ Generation (DOCX)](#8-тз-generation-docx)
9. [Workflow Order](#9-workflow-order)

---

## 1. Prerequisites

Before any Figma operation:

1. Identify the **fileKey** from the Figma URL: `figma.com/design/:fileKey/:fileName`
2. Know the **target page** name (e.g., "Screens", "Design System")
3. Have the Figma MCP tool `use_figma` available
4. For verification, have `get_screenshot` available

Read `references/figma-api-gotchas.md` before writing any `use_figma` code — it will save you from the most common failures.

---

## 2. Figma API Golden Rules

These are non-negotiable. Every `use_figma` call should follow them.

### Page Access
```javascript
// ALWAYS set page before accessing children — otherwise children = []
const page = figma.root.children.find(p => p.name === 'Screens');
await figma.setCurrentPageAsync(page);
// NOW page.children is populated
```

### Font Loading
```javascript
// ALWAYS load fonts before ANY text operation
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
await figma.loadFontAsync({ family: "Inter", style: "Medium" });
await figma.loadFontAsync({ family: "Inter", style: "Semi Bold" });
await figma.loadFontAsync({ family: "Inter", style: "Bold" });
// Only then: node.characters = "New text"
```

### Colors
```javascript
// Figma uses 0–1 floats, NOT 0–255
// Example: #0D9488 (Teal)
const teal = { r: 0.051, g: 0.58, b: 0.533 };
// Helper to convert HEX → Figma RGB:
function hexToFigma(hex) {
  const r = parseInt(hex.slice(0,2), 16) / 255;
  const g = parseInt(hex.slice(2,4), 16) / 255;
  const b = parseInt(hex.slice(4,6), 16) / 255;
  return { r, g, b };
}
```

### Auto-Layout Gotcha
```javascript
// Frames with layoutMode = "HORIZONTAL"/"VERTICAL" shrink to content!
// For fixed-size elements (e.g., OTP boxes 48×56):
frame.layoutMode = "NONE";
frame.resize(48, 56);
// If you need auto-layout AND a minimum size, set:
frame.minWidth = 48;
frame.minHeight = 56;
```

### Verification Pattern
After every significant change, take a screenshot:
```javascript
// In use_figma — return the node ID
return JSON.stringify({ nodeId: frame.id, name: frame.name });
// Then call get_screenshot with that nodeId to visually verify
```

For the full reference of gotchas and patterns, see `references/figma-api-gotchas.md`.

---

## 3. Creating Screens from Scratch

Use this when you need to create new iOS screens programmatically. Read `references/ios-screen-template.md` for the full annotated code template.

### Screen Anatomy (iPhone 15 Pro: 393×852)

```
┌──────────────────────────┐  y=0
│     Status Bar (54pt)    │  ← Dynamic Island area
├──────────────────────────┤  y=54
│     Navigation Bar       │  ← 44pt height, title + back/actions
├──────────────────────────┤  y=98
│                          │
│     Content Area         │  ← Scrollable, fills remaining space
│     (varies)             │
│                          │
├──────────────────────────┤  y=769
│     Tab Bar (83pt)       │  ← 49pt bar + 34pt home indicator
└──────────────────────────┘  y=852
```

### Step-by-Step Process

1. **Read the SwiftUI source** — understand what the screen shows (if code exists)
2. **Create the outer frame**: `393×852`, white/dark fill, clip content
3. **Add Status Bar**: time (left), Dynamic Island (center), icons (right)
4. **Add Navigation Bar**: back chevron, title, optional action buttons
5. **Add Content Area**: the screen's unique content
6. **Add Tab Bar**: 5 icons with labels (or 2 for Grandparent Mode)
7. **Name the frame**: `ScreenName - Light` / `ScreenName - Dark`
8. **Position on canvas**: place next to related screens
9. **Verify with screenshot**

### Light → Dark Cloning

After creating the Light version:
```javascript
// Color comparison helper (tolerance for float rounding)
function isClose(c1, c2, tol = 0.02) {
  return Math.abs(c1.r - c2.r) < tol &&
         Math.abs(c1.g - c2.g) < tol &&
         Math.abs(c1.b - c2.b) < tol;
}

const darkFrame = lightFrame.clone();
darkFrame.name = darkFrame.name.replace('Light', 'Dark');
darkFrame.x = lightFrame.x + 440; // 393 + 47 gap

// Swap colors
function swapColors(node) {
  if (node.fills && node.fills.length > 0) {
    const fills = [...node.fills];
    fills.forEach(fill => {
      if (fill.type === 'SOLID') {
        // White → Dark background
        if (isClose(fill.color, {r:1,g:1,b:1})) {
          fill.color = hexToFigma('111827'); // gray-900
        }
        // Dark text → Light text
        else if (isClose(fill.color, {r:0,g:0,b:0}) ||
                 isClose(fill.color, hexToFigma('111827'))) {
          fill.color = {r:1,g:1,b:1};
        }
        // Keep accent color (teal) as-is
      }
    });
    node.fills = fills;
  }
}

// Apply recursively
function traverseAndSwap(node) {
  swapColors(node);
  if ('children' in node) {
    for (const child of node.children) {
      traverseAndSwap(child);
    }
  }
}
traverseAndSwap(darkFrame);
```

---

## 4. Auditing Existing Designs

Run a design audit to catch issues before handoff. The audit outputs a report with screen completeness, parity, and quality scores.

### Audit Script Pattern

```javascript
const page = figma.root.children.find(p => p.name === 'Screens');
await figma.setCurrentPageAsync(page);

const frames = page.children.filter(n => n.type === 'FRAME');
const report = { total: frames.length, light: [], dark: [], orphans: [], issues: [] };

for (const frame of frames) {
  const name = frame.name;
  const isDark = name.toLowerCase().includes('dark');
  const isLight = !isDark;

  if (isLight) report.light.push(name);
  else report.dark.push(name);

  // Check for issues
  if (frame.width !== 393 || frame.height !== 852) {
    report.issues.push({ frame: name, issue: `Wrong size: ${frame.width}×${frame.height}` });
  }

  // Check text nodes for font consistency
  const texts = frame.findAll(n => n.type === 'TEXT');
  for (const t of texts) {
    if (t.fontName && t.fontName.family !== 'Inter') {
      report.issues.push({ frame: name, issue: `Wrong font: ${t.fontName.family} on "${t.characters.slice(0,30)}"` });
    }
  }
}

// Find orphans (Light without Dark pair or vice versa)
const lightNames = report.light.map(n => n.replace(/ - Light$| Light$/i, '').trim());
const darkNames = report.dark.map(n => n.replace(/ - Dark$| Dark$/i, '').trim());
lightNames.forEach(n => { if (!darkNames.includes(n)) report.orphans.push(`${n}: missing Dark`); });
darkNames.forEach(n => { if (!lightNames.includes(n)) report.orphans.push(`${n}: missing Light`); });

return JSON.stringify(report, null, 2);
```

### What to Check

| Category | Check | How |
|----------|-------|-----|
| Size | All frames 393×852 | `frame.width === 393 && frame.height === 852` |
| Fonts | Only Inter used | `findAll(TEXT).every(t => t.fontName.family === 'Inter')` |
| Colors | No hardcoded, use variables | Check fills against known palette |
| Parity | Every Light has a Dark | Name matching |
| Naming | Descriptive layer names | No "Frame 47", "Rectangle 12" |
| Content | No Lorem ipsum | Search text nodes |
| Spacing | Multiples of 4pt | Check y-positions and gaps |

---

## 5. Light/Dark Parity

Ensuring every screen has both Light and Dark variants is critical for iOS apps.

### Auto-Parity Check

```javascript
const page = figma.root.children.find(p => p.name === 'Screens');
await figma.setCurrentPageAsync(page);

const frames = page.children.filter(n => n.type === 'FRAME' && n.width === 393);
const lightFrames = frames.filter(f => !f.name.toLowerCase().includes('dark'));
const darkFrames = frames.filter(f => f.name.toLowerCase().includes('dark'));

const missingDark = [];
const missingLight = [];

for (const lf of lightFrames) {
  const baseName = lf.name.replace(/ ?- ?Light| ?Light/i, '').trim();
  const hasDark = darkFrames.some(df =>
    df.name.replace(/ ?- ?Dark| ?Dark/i, '').trim() === baseName
  );
  if (!hasDark) missingDark.push({ name: baseName, lightId: lf.id });
}

return JSON.stringify({ missingDark, missingLight,
  lightCount: lightFrames.length, darkCount: darkFrames.length });
```

### Color Mapping for Dark Mode

| Light | Dark | Usage |
|-------|------|-------|
| `#FFFFFF` | `#111827` (gray-900) | Background |
| `#F9FAFB` (gray-50) | `#1F2937` (gray-800) | Card/surface |
| `#111827` (gray-900) | `#FFFFFF` | Primary text |
| `#6B7280` (gray-500) | `#9CA3AF` (gray-400) | Secondary text |
| `#E5E7EB` (gray-200) | `#374151` (gray-700) | Borders |
| `#0D9488` (teal) | `#0D9488` (teal) | Accent — same in both |

---

## 6. WCAG AA Accessibility

iOS apps in the App Store are expected to meet WCAG AA. Check these programmatically.

### Contrast Checker

```javascript
function luminance(r, g, b) {
  const [rs, gs, bs] = [r, g, b].map(c =>
    c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
  );
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function contrastRatio(fg, bg) {
  const l1 = luminance(fg.r, fg.g, fg.b);
  const l2 = luminance(bg.r, bg.g, bg.b);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// WCAG AA requirements:
// Normal text (< 18pt or < 14pt bold): ratio >= 4.5
// Large text (>= 18pt or >= 14pt bold): ratio >= 3.0
// UI components and graphical objects: ratio >= 3.0
```

### Touch Target Check

```javascript
// Apple HIG minimum: 44×44 pt
const interactiveNodes = frame.findAll(n =>
  n.type === 'INSTANCE' || n.name.toLowerCase().includes('button') ||
  n.name.toLowerCase().includes('tap') || n.name.toLowerCase().includes('icon')
);

const tooSmall = interactiveNodes.filter(n =>
  n.width < 44 || n.height < 44
);
```

---

## 7. Handoff Preparation

Before sending the Figma file to a developer or designer, prepare it with navigation aids.

### Cover Frame

Create a Cover frame at position (0, 0) that serves as a file map:

```javascript
// See references/ios-screen-template.md for full Cover template
const cover = figma.createFrame();
cover.name = '📋 Cover — Handoff Index';
cover.resize(800, 1200);
cover.x = -900; // Left of the first screen
cover.fills = [{ type: 'SOLID', color: { r: 0.98, g: 0.98, b: 0.98 } }];

// Add: project name, subtitle, version info, screen index by section
```

### Screen Labels

Add text labels above each screen frame for easy identification:

```javascript
for (const frame of screenFrames) {
  await figma.loadFontAsync({ family: "Inter", style: "Semi Bold" });
  const label = figma.createText();
  label.characters = frame.name;
  label.fontSize = 14;
  label.fontName = { family: "Inter", style: "Semi Bold" };
  label.fills = [{ type: 'SOLID', color: hexToFigma('6B7280') }];
  label.x = frame.x;
  label.y = frame.y - 24;
}
```

### Section Headers

Group screens logically with section headers:
```
LIGHT MODE (Row 1): Home · Auth · Medications · Dose Log · Family
DARK MODE (Row 1): Home · Auth · Medications · Dose Log · Family
UTILITY: Push Notifications · UI States
```

---

## 8. ТЗ Generation (DOCX)

Generate a Technical Specification document for handoff using `docx` npm library.

### Reusable Helper Pattern

The helpers below are battle-tested. Use `scripts/docx-helpers.js` or copy this pattern:

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, BorderStyle, WidthType, ShadingType, AlignmentType,
  LevelFormat, Header, Footer, PageNumber, ExternalHyperlink, PageBreak
} = require("docx");

// Color constants
const TEAL = "0D9488", DARK = "111827", GRAY = "6B7280";

// Helpers: headerCell, cell, makeTable, heading, h2, h3, para, bullet,
//          numberedItem, spacer, link
// See scripts/docx-helpers.js for full implementations
```

### ТЗ Document Structure

A good design spec includes:

1. **Title page**: project name, version, date
2. **Project context**: target audience, brand values, design system summary
3. **Current state**: table of existing screens with status
4. **Tasks for designer**: prioritized with deliverables table
5. **Design system**: colors, typography, spacing, components
6. **QA checklist**: visual consistency, accessibility, Figma hygiene
7. **References**: Figma link, Apple HIG links, WCAG reference

### Cyrillic Validation

Always validate Cyrillic text in generated DOCX:
```python
from docx import Document
doc = Document('output.docx')
for p in doc.paragraphs[:20]:
    if p.text.strip():
        print(p.text[:80])
```

---

## 9. Workflow Order

When working on a full design pipeline, follow this order:

```
1. AUDIT       → Run audit script, understand current state
2. FIX         → Fix broken/incomplete screens
3. CREATE      → Build missing screens (Light first, then Dark clone)
4. PARITY      → Verify every Light has a Dark pair
5. VARIABLES   → Replace hardcoded colors with Figma Variables
6. WCAG        → Check contrast ratios, touch targets
7. HANDOFF     → Add Cover frame, labels, section headers
8. ТЗ          → Generate DOCX spec document
9. VERIFY      → Final screenshot comparison of all screens
```

Each step can be run independently. If you're doing a quick fix, start at step 2. If building from scratch, start at step 1.

### Per-Screen Workflow

For each new screen:
```
Read Swift source (if exists) → ASCII wireframe → Create Light frame →
Clone to Dark → Swap colors → Verify both with screenshots
```

---

## References

- `references/figma-api-gotchas.md` — comprehensive list of API pitfalls and solutions
- `references/ios-screen-template.md` — annotated code for creating a full iOS screen
- `scripts/docx-helpers.js` — reusable DOCX generation helpers
