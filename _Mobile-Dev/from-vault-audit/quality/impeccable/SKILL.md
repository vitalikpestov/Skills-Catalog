---
name: impeccable
description: "AI-slop pattern detector for DoseSync SwiftUI views. Scans Views/ for 22 design anti-patterns common in AI-generated iOS code: generic placeholder copy, visual hierarchy collapses, broken empty states, incorrect haptic pairing, missing press feedback, inconsistent corner radii, force-unwrapped color literals, and more. Inspired by pbakaus/impeccable. Use before TestFlight submission, after major UI refactors, or when onboarding new screens. Outputs a ranked defect report with file:line refs and suggested fixes."
user-invocable: true
---

# Impeccable — AI-Slop Detector for DoseSync SwiftUI

Scans `DoseSync/DoseSync/Views/` for 22 patterns that signal AI-generated or copy-pasted code lacking visual polish. Does NOT replace `audit-ui` (which does screenshot capture + a11y grep) — this is a **code-reading pass** focused on design quality.

## When to invoke

- `/impeccable` or "run impeccable", "check for ai slop", "polish audit"
- Before TestFlight submission (mandatory pre-flight)
- After major UI changes or new screen additions
- When a screen "looks a bit off" but you can't articulate why

## Output

- Console report sorted by severity (P0 → P3)
- `DoseSync/impeccable-report.md` — markdown table with all findings
- Summary counts per category

---

## 22 Anti-Patterns (Detection Rules)

### Category A — Copy & Tone (P1–P2)

**A1 — Hardcoded English in RU/FR/ES paths**
```
Grep: 'Text\("[A-Z][a-z]' in Views/
```
Flag any `Text("Literal string")` not wrapped in `String(localized:)` or `LocalizedStringKey`. 
Exempt: `#Preview` blocks, `// MARK:` comments.

**A2 — Placeholder copy signals**
```
Grep: 'TBD|TODO|Coming soon|Placeholder|Lorem|test text|Sample|dummy|fake' in Views/ (case-insensitive)
```
Flag each hit. These should never ship to TestFlight.

**A3 — Generic error messages**
```
Grep: '"Something went wrong"|"An error occurred"|"Error"|"Failed"' in Views/
```
Flag raw non-localized error strings. DoseSync error messages must describe the action that failed ("Couldn't confirm dose — tap to retry").

**A4 — «Ты»-form in Russian copy**
```
Grep: 'твой|тебя|тебе|тобой|твоя|твоё|твои|ты |Ты ' in Views/ AND in Localizable.xcstrings
```
Flag violations of the «Вы»-form rule (tone-of-voice.md). Case-sensitive for pronoun forms.

---

### Category B — Visual Hierarchy (P1–P2)

**B1 — Everything `.headline` or `.body` font weight**
```
Grep: '\.font\(\.headline\)' in Views/
```
Count consecutive `headline` usages within 30 lines of each other. If 3+ elements on one screen all use `.headline` → P2 flag (missing hierarchy differentiation: title / headline / body / caption progression).

**B2 — All-caps overuse**
```
Grep: '\.textCase\(\.uppercase\)' OR '\.uppercased()' in Views/
```
More than 2 occurrences in a single file → P3. All-caps signals AI filler when applied to body copy.

**B3 — Missing visual weight on primary CTA**
```
Grep: 'Button.*\.buttonStyle\(\.plain\)' adjacent to primary action labels
```
Plain-style on primary CTA buttons collapses visual hierarchy. Primary CTAs need `.buttonStyle(.borderedProminent)` or custom full-width style.

**B4 — VStack/HStack with zero spacing control**
```
Grep: 'VStack \{|HStack \{' (no spacing: parameter) in Views/
```
Flag VStack/HStack without explicit `spacing:` parameter — uses system default which is often wrong (8pt is rarely the right grid step for DoseSync 4pt grid). Exempt: when enclosed in `.padding()` blocks that establish rhythm.

---

### Category C — Empty & Loading States (P0–P2)

**C1 — Missing empty state**
```
Grep: 'case .empty' in Views/ — cross-reference with List/ScrollView files
```
Every file with `List` or `ScrollView` must have a `.empty` case handler. Files with List/ScrollView but no empty case → P1.

**C2 — Empty state without action CTA**
```
Read EmptyStateView usages — check if `action:` parameter is provided
```
Empty state with only message and no action button = dead end (violates Nielsen H10 + H3). Flag as P2.

**C3 — ProgressView without timeout handling**
```
Grep: 'ProgressView()' in Views/
```
Bare `ProgressView()` without surrounding `.task {}` timeout or error state → P2. Infinite spinner is an AI-slop pattern (appears to handle loading but doesn't handle failure).

**C4 — Missing four-states pattern**
```
For each ViewModel file: check that ViewState enum has .loading, .empty, .error, .loaded cases
```
Per `swiftui-views.md` rule. ViewModels missing any of the 4 states → P1.

---

### Category D — Interaction & Feedback (P0–P1)

**D1 — Tappable element without press feedback**
```
Grep: 'Button \{|\.onTapGesture \{' in Views/
```
For each interactive element: check if `.scaleEffect` or haptic is provided within 10 lines. Missing press feedback on tap-targets → P1 (violates swiftui-views.md motion rules §"Press feedback").

**D2 — Wrong haptic for context**
```
Grep: '.notificationOccurred\(.success\)' near non-success actions
Grep: '.impactOccurred' near success/failure feedback
```
Cross-reference with haptic choreography table in `swiftui-views.md`. Mismatched haptic type → P1.

**D3 — Animation without reduceMotion check**
```
Grep: 'withAnimation\(' in Views/
```
For each `withAnimation` without adjacent `accessibilityReduceMotion` guard → P1. Per motion rules in swiftui-views.md.

**D4 — easeIn on interactive elements**
```
Grep: '\.easeIn\b' OR 'Animation.easeIn' in Views/
```
easeIn = slow start = UI feels broken on interactive elements. Flag every usage → P1 (swiftui-views.md: "НИКОГДА `.easeIn` на interactive-элементах").

---

### Category E — Color & Token Misuse (P0–P2)

**E1 — Direct hex color literals**
```
Grep: 'Color\(red:|Color\(#|Color(hex:' in Views/ (NOT in DesignTokens.swift or AppStoreAssets/)
```
Raw hex in Views/ bypasses DS token system. Each hit → P1. All colors must come from `Color.DS.*` tokens.

**E2 — System green / system blue leaking**
```
Grep: 'Color\.green|Color\.blue|Color\.accentColor' in Views/ (excluding Comments)
```
System green = #34C759 (NOT brand teal #00C896). System blue = #007AFF. Both banned in DoseSync per brand rules. Each hit → P1.

**E3 — Direct white/black without semantic intent**
```
Grep: 'Color\.white|Color\.black|\.foregroundColor\(\.white\)|\.foregroundColor\(\.black\)' in Views/
```
Per audit-ui checks — these break Dark Mode. Flag unless in `AppStoreAssets/` or marketing renders. → P2.

**E4 — Opacity-on-color without SemanticTintBackground**
```
Grep: 'Color\.DS\.(warning|danger)\.opacity(' in Views/
```
Post DS-V1-opacity-audit.md: this pattern fails WCAG in Dark Mode. All remaining instances must use `SemanticTintBackground` modifier. → P0 (WCAG regression).

---

### Category F — Code Structure (P2–P3)

**F1 — Business logic in View body**
```
Grep: 'func [a-z].*async\b' in struct.*: View files
```
Async functions defined inside View structs (not extracted to ViewModel) = MVVM violation. → P2.

**F2 — print() statements**
```
Grep: '\bprint\(' in Views/ AND Services/ AND ViewModels/
```
All logging must use `Logger(subsystem:category:)`. Each `print()` → P1.

**F3 — Force unwrap without justification**
```
Grep: '[^!]![^=\?]' in Views/ (simplified — matches `!` not followed by `=` or `?`)
```
Each force unwrap without adjacent justification comment → P0.

**F4 — Combine usage**
```
Grep: 'import Combine|@Published|PassthroughSubject|CurrentValueSubject' in Views/ OR ViewModels/
```
Combine banned — async/await only. Each hit → P1.

---

## Execution Steps

### Step 1: Collect all View files

```bash
find DoseSync/DoseSync/Views -name "*.swift" | sort
```

Save list. Count = N files.

### Step 2: Run all 22 pattern checks

For each pattern (A1–F4):
1. Run the grep command against `DoseSync/DoseSync/Views/` (and `ViewModels/` for C4/F1/F2/F4)
2. Collect hits as `{pattern_id, file, line, snippet}`
3. Classify severity per pattern definition

### Step 3: Deduplicate and rank

Sort all hits by severity (P0 first), then by file path.

Remove known exemptions:
- `#Preview` blocks (any file line after `#Preview {`)
- `AppStoreAssets/` files (marketing renders, not app UI)
- `DoseSync-qa/`, `DoseSync-i18n/` worktrees (not main branch UI)

### Step 4: Write report

Write `DoseSync/impeccable-report.md`:

```markdown
# Impeccable UI Audit — {DATE}

## Summary
| Severity | Count |
|----------|-------|
| P0 | {n} |
| P1 | {n} |
| P2 | {n} |
| P3 | {n} |
| **Total** | **{n}** |

## Findings

| # | Severity | Pattern | File:Line | Snippet | Fix |
|---|----------|---------|-----------|---------|-----|
| 1 | P0 | E4 — opacity-on-color | HomeStreakBanner.swift:51 | `Color.DS.warning.opacity(0.15)` | Use `SemanticTintBackground(.warning, .track)` |
...
```

### Step 5: Print summary to user

```
Impeccable audit complete — {N} files scanned.

Findings: {total} ({P0} P0 · {P1} P1 · {P2} P2 · {P3} P3)

Top P0s to fix before TestFlight:
1. E4 — opacity-on-color (N remaining violations of DS-V1-opacity-audit)
2. F3 — force unwrap without justification: {file:line}
3. C1 — missing empty state: {file}

Full report: DoseSync/impeccable-report.md
```

---

## Known Baseline (from previous audits)

These are pre-existing findings that are tracked but may not need immediate fix:

| Pattern | Known hits | Status |
|---------|-----------|--------|
| A1 — hardcoded strings in swipe actions | DoseLogView:296-309, 325, 335 | P2 backlog (DES-SCR-REVIEW-01) |
| A1 — hardcoded "pending" | DoseLogView:87 | P2 backlog |
| E4 — opacity-on-color | 2 post-spec hits: HeroNextDoseCard:136, GrandparentSetupFlow:153 | P0 — check if migrated in feat/ios-qa-v1-11-opacity |

## Relationship to other skills

- **`audit-ui`** — screenshot capture + static a11y checks (touch targets, Dynamic Type). Run alongside impeccable.
- **`copy-lint`** — Russian «Вы»-form + medical claim detection. Overlaps with A4 — run copy-lint for deeper RU validation.
- **`taste-check`** — visual taste validation on rendered screenshots. Impeccable = code, taste-check = rendered.

## Source

Adapted from [pbakaus/impeccable](https://github.com/pbakaus/impeccable) concept. DoseSync-specific patterns added: RU tone (A4), SemanticTintBackground (E4), four-states (C4), Combine ban (F4). Pattern count: 22 (original ~20 + 4 DoseSync-specific).
