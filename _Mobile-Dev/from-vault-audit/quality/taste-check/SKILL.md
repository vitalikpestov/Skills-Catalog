---
name: taste-check
description: "Visual taste validation for DoseSync rendered screens. Takes simulator screenshots (from audit-ui or manual capture) and evaluates them against 15 taste criteria: spatial rhythm, typographic contrast, color weight balance, negative space use, motion intent, information density, icon consistency, and more. Inspired by leonxlnx/taste-skill, adapted for iOS SwiftUI with DoseSync design system. Use after audit-ui screenshot capture, before TestFlight, or when a screen 'feels off' but static analysis passes clean."
user-invocable: true
---

# Taste Check — Visual Taste Validation for DoseSync

A **subjective-but-systematic** review layer on top of `audit-ui` screenshots. Where `audit-ui` catches accessibility and code violations, `taste-check` catches visual quality issues: rhythm, density, hierarchy, motion intent, and polish signals that automated tools miss.

## When to invoke

- `/taste-check` or "taste check", "visual polish review", "does this look good"
- After `audit-ui` completes (screenshots available at `DoseSync/audit-ui-screenshots/`)
- Before major TestFlight releases
- When Figma mocks look good but the running app "feels off"
- Per-screen: "taste check HomeView"

## Input

Either:
1. **Auto:** use screenshots from `DoseSync/audit-ui-screenshots/` (Light Normal state = baseline)
2. **Manual:** user provides screenshot paths
3. **Per-screen:** navigate simulator to specific screen and capture via `screenshot` MCP tool

## Output

- Console review per screen
- `DoseSync/taste-report.md` — findings table with severity + fix suggestions
- Design references where relevant (cite: Mobbin / Dribbble / paywallscreens.com patterns)

---

## 15 Taste Criteria

### T1 — Spatial Rhythm (4pt grid)

**What to look for:** consistent vertical spacing between elements. DoseSync uses a 4pt grid (4 / 8 / 12 / 16 / 24 / 32 / 48pt).

**Red flags:**
- Elements visually "floating" without clear alignment to neighbors
- Padding that looks "about right" but breaks the 4pt grid (5pt, 7pt, 11pt)
- Groups of cards with inconsistent inter-card spacing

**How to check:** eyeball horizontal alignment — can you draw invisible vertical lines through left edges? Can you mentally snap elements to a grid?

**Severity:** P2 (consistent grid = professionalism signal)

---

### T2 — Typographic Scale Contrast

**What to look for:** clear size jump between hierarchy levels (title → body → caption).

**Red flags:**
- Title and body are the same size (e.g. both `.body`) — nothing reads as "the headline"
- Caption text at 11pt or smaller on a dense card
- Monospaced-style visual weight (every text element looks equally important)
- Missing bold weight on information the user needs to read first

**DoseSync scale (reference):**
- Large title: `.largeTitle` (34pt) — screen-level titles only
- Headline: `.headline` (17pt semibold) — card titles
- Body: `.body` (17pt) — dose names, timestamps
- Subheadline: `.subheadline` (15pt) — secondary labels
- Caption: `.caption` (12pt) — metadata, timestamps secondary

**Severity:** P1 if two adjacent hierarchy levels are indistinguishable

---

### T3 — Color Weight Balance

**What to look for:** accent color (`#00C896`) should attract the eye to the most important element — not be used decoratively everywhere.

**Red flags:**
- Accent appears on 3+ elements on the same screen (eye has nowhere to land)
- Accent used on decorative icons (status icons, timestamps) competing with primary CTA
- Muted/gray tones making the entire screen feel cold or "unbranded"
- Warning/danger colors (#F2950A / #E73B3B) competing with accent — two visual anchors

**Visual test:** look at the screen from 1 meter away blurred. What color pops? That should be the primary action or information.

**Severity:** P1 if two accent-colored elements compete for attention

---

### T4 — Negative Space (Breathing Room)

**What to look for:** intentional empty space that gives the eye a rest.

**Red flags:**
- Content running edge-to-edge with minimal margin (< 16pt from screen edges)
- Cards touching each other (no inter-card gap)
- Dense list views with no visual "breathers" (date separators, section headers)
- Grandparent Mode screens crowded (grandparent mode needs MORE negative space, not less)

**Reference:** Medisafe's caregiver log — too dense. Daylite's calendar cards — good breathing room.

**Severity:** P2 for general screens, P1 for Grandparent Mode (accessibility)

---

### T5 — Icon Consistency

**What to look for:** all SF Symbols at the same weight and usage context.

**Red flags:**
- Mixed icon weights (`.regular` for some, `.medium` for others in same row)
- Outlined icons in some places, filled in others for same semantic meaning
- Icon size inconsistency within tab bar (some 22pt, some 24pt)
- Custom icons mixed with SF Symbols without visual weight matching

**Check:** tab bar icons must all be same SF Symbol weight. Action icons in cards must match.

**Severity:** P2

---

### T6 — Information Density

**What to look for:** appropriate density for user type and context.

**DoseSync density tiers:**
- **Home / HeroNextDoseCard:** LOW density — one primary action dominates
- **DoseLog:** MEDIUM density — scannable list with clear status
- **Grandparent Mode:** VERY LOW — max 2 items visible at once
- **Paywall:** LOW — one price point in focus
- **Settings:** HIGH density OK — users expect lists

**Red flags:**
- Home screen showing 6+ dose cards visible (too much info, key action buried)
- Grandparent Mode with small text or multiple CTAs
- Paywall with feature comparison table AND testimonials AND pricing all above the fold

**Severity:** P1 for Grandparent Mode, P2 for others

---

### T7 — Motion Intent

**What to look for:** every animation has a clear purpose (continuity / feedback / focus — per swiftui-views.md).

**Red flags (visual, not code):**
- Elements that pop in/out without transition (harsh discontinuity)
- Animations that feel random or unrelated to user gesture
- Over-animation: too many things moving at once
- Stagger effect that draws attention AWAY from primary element
- Celebrations that play without any user action (auto-fire on appear)

**Test:** watch the transition. Can you answer "why did that move?" If not → purposeless animation.

**Severity:** P2 for decoration, P1 for feedback animations that mismatch action

---

### T8 — Card Elevation Consistency

**What to look for:** cards use the DoseSync elevation vocabulary consistently.

**DoseSync card hierarchy (reference):**
- Background surface: `.background` → system background
- Card level 1: subtle shadow / 1pt border in `.quaternarySystemFill`
- Card level 2 (modals/sheets): slightly elevated, `.systemBackground`
- HeroNextDoseCard: most elevated — brand accent border or shadow

**Red flags:**
- Cards with no border or shadow (invisible against background)
- All cards at the same elevation (no hierarchy between card types)
- Thick borders (> 1.5pt) making UI look heavy/outdated
- Drop shadows using incorrect blur radius (iOS shadows are subtle — 2-4pt blur, not 8pt)

**Severity:** P2

---

### T9 — Empty State Quality

**What to look for:** empty states that feel intentional, not like placeholders.

**Quality markers:**
- Illustration or meaningful SF Symbol (not a generic `questionmark.circle`)
- Headline that understands the user's context ("No medications yet" not "Empty")
- CTA that resolves the empty state ("Add your first medication →")
- Visual weight appropriate for the screen (not a tiny icon centered on a huge phone)

**Red flags:**
- "No data" or "Nothing here" as the entire empty state
- Missing CTA (dead end)
- Illustrtion that doesn't relate to the domain (generic charts/graphs for a dose log)

**Severity:** P1 (empty states are first impression for new users)

---

### T10 — Focus Point per Screen

**What to look for:** one clear visual anchor per screen where the eye lands first.

**Test:** blur your eyes and look at the screen. What's the first thing you see? That should be the primary value prop or action.

**Red flags:**
- Two equally large/bold elements competing (dual-focal screen)
- Primary CTA button not the highest-contrast element
- Decorative illustrations larger than the CTA
- Dense list where no single item has visual priority

**Severity:** P1 if the primary CTA is not the dominant visual element

---

### T11 — Dark Mode Color Temperature

**What to look for:** Dark Mode screens feel intentionally designed, not just "colors inverted."

**Red flags:**
- Pure black backgrounds (#000000) — feels harsh; use `#0F1117` (DoseSync dark bg)
- White text on dark that looks overly stark (consider `Color.primary` which auto-adapts)
- Brand teal (`#00C896`) that "floats" without dark-mode-appropriate container
- SemanticTint backgrounds that are too faint (DES-QA-V1-02 fix) or too garish

**Reference:** compare Light vs Dark screenshots from `audit-ui` — each element should feel equally designed in both modes.

**Severity:** P1 (Dark Mode is 60% of H&F category per Apple reports)

---

### T12 — Loading Skeleton Quality

**What to look for:** skeleton states that approximate the real content layout.

**Red flags:**
- Skeleton that's just gray rectangles with no relationship to real content size
- Skeleton with wrong number of "rows" (5 skeleton rows for a 2-item list)
- No shimmer animation (static skeleton feels broken, not loading)
- Skeleton that disappears instantly before content appears (flash of empty)

**Severity:** P2

---

### T13 — Grandparent Mode Specifics

Only evaluate if Grandparent Mode screens are in scope.

**Taste checks specific to grandparent:**
- [ ] Button height ≥ 80pt (not just 44pt minimum)
- [ ] Button label font ≥ `.title3` (21pt)
- [ ] No more than 2 CTA options visible simultaneously
- [ ] High contrast — status colors distinguishable for mild color blindness
- [ ] Name of dependent visible without scrolling (memory aid)
- [ ] Minimal UI chrome — no settings gear, no tab bar visible, no overflow menus

**Severity:** P0 for any violation (Grandparent Mode is a key differentiator and must be impeccable)

---

### T14 — Paywall Trust Signal Quality

Only evaluate if Paywall screens are in scope.

**Taste checks specific to paywall:**
- [ ] Trust screen 1 (social proof): testimonial photo/avatar + real name + benefit stated
- [ ] Trust screen 2 (value): specific number ("prevented 847 double-doses") not generic
- [ ] Trust screen 3 (personalization): refers back to user's scenario (Solo / Family)
- [ ] Plan card visual: highlighted plan has clear visual distinction (badge + border + color)
- [ ] CTA color: brand teal, NOT system green/blue
- [ ] Skip/dismiss option visible but de-emphasized (smaller, plain text, not competing with CTA)

**Reference:** paywallscreens.com — filter Health & Fitness, sort by rating.

**Severity:** P1 per failed check (paywall = revenue)

---

### T15 — Overall First Impression (Gestalt)

**What to look for:** the screen communicates its purpose within 2 seconds.

**Test:** show the screenshot to someone unfamiliar with the app for 3 seconds. Ask: "What would you do on this screen?" If they can't answer → screen fails the gestalt test.

**Red flags:**
- Multiple CTAs competing (user doesn't know what to do)
- No obvious hierarchy (everything equally visible)
- App "brand" not perceivable (could be any app)
- Screen feels crowded or sparse without reason

**Severity:** P1 for core screens (Home, Paywall, Onboarding steps), P2 for secondary screens

---

## Execution Steps

### Step 1: Identify screenshots to review

Option A — use audit-ui output:
```bash
ls DoseSync/audit-ui-screenshots/ | grep "light-normal"
```

Option B — capture specific screens via XcodeBuildMCP `screenshot` tool.

### Step 2: For each screenshot, evaluate T1–T15

Work screen by screen. For each criterion:
- **Pass:** no comment needed (report space is for findings only)
- **Fail:** record `{screen, criterion, observation, severity, suggested fix}`

Skip criteria that don't apply (T13/T14 if screen doesn't contain grandparent/paywall).

### Step 3: Write taste-report.md

```markdown
# Taste Check — {DATE}

## {N} screens reviewed

### Home (home-A-light-normal.png)

| # | Criterion | Finding | Sev | Fix |
|---|-----------|---------|-----|-----|
| 1 | T3 Color Weight | Accent teal on 4 elements (HeroCard title, tab icon, status dots, CTA) — eye has nowhere to anchor | P1 | Reserve accent for HeroCard CTA only; use `.secondary` for status dots |
| 2 | T10 Focus Point | ProgressView and HeroCard both compete at same visual weight | P2 | Increase HeroCard contrast, reduce ProgressView size |

### DoseLog
...
```

### Step 4: Summary

```
Taste Check complete — {N} screens reviewed.

Findings: {total} ({P0} P0 · {P1} P1 · {P2} P2)

Top taste issues:
1. T3 — Color weight: accent overused on Home (4 elements compete)
2. T13 — Grandparent Mode: confirm button 60pt (needs ≥ 80pt)
3. T9 — Empty state: DoseLog empty has no CTA

Full report: DoseSync/taste-report.md
```

---

## Reference Library

When suggesting fixes, reference these as examples of patterns done well:

| Pattern | Reference app |
|---------|---------------|
| Breathing room + card elevation | Notion iOS |
| Grandparent-scale UI | Simple Bank (large touch targets) |
| Paywall trust signals | Headspace paywall (social proof placement) |
| Empty states with CTAs | Airbnb search empty state |
| Color weight restraint | Linear iOS (accent used once per screen) |
| Dark Mode temperature | Apollo for Reddit (warm dark palette) |
| Typographic scale | Bear Notes (clear title/body/caption differentiation) |

## Relationship to other skills

- **`audit-ui`** — captures screenshots. Run first, then feed output to `taste-check`.
- **`impeccable`** — detects code-level anti-patterns. `taste-check` detects rendered visual issues.
- **`figma-ios-design-pipeline`** — after finding taste issues, use this skill to update Figma mocks.

## Source

Adapted from [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) concept. DoseSync-specific criteria added: T11 (Dark Mode temperature), T13 (Grandparent Mode), T14 (Paywall trust signals). Criteria count: 15 (original ~10 taste dimensions + 5 DoseSync-specific).
