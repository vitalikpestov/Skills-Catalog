---
name: audit-ui
description: "Automated UI audit for DoseSync — builds app, boots simulator, navigates through 5 main screens (Home, DoseLog, Meds, Family, Settings), captures 20 screenshots across 4 state combinations (Light/Dark × Normal/XXL Dynamic Type), runs static code analysis for accessibility defects, and generates an HTML report. Use this skill when the user asks to audit UI, check accessibility, run ui audit, capture all screens, verify Dark Mode parity, check Dynamic Type overflow, generate visual regression baseline, or prepare TestFlight UI QA."
---

# UI Audit — DoseSync

Automated multi-state UI audit. Captures 20 screenshots (5 screens × 4 states) + static code analysis + HTML report.

## When to invoke

- `/audit-ui`, "run ui audit", "check all screens"
- Before TestFlight submission
- After major UI refactors
- To establish visual regression baseline
- To verify Dark Mode + Dynamic Type parity

## Output

- `DoseSync/audit-ui-report.html` — single file with screenshot grid + defects table
- `DoseSync/audit-ui-screenshots/` — 20 PNG files (5 screens × 4 states)
- Console summary with defect counts

## States captured

| # | Appearance | Dynamic Type | Purpose |
|---|-----------|--------------|---------|
| A | Light | Normal (.large) | Baseline |
| B | Light | XXL (.accessibility3) | Overflow check |
| C | Dark | Normal (.large) | Dark parity |
| D | Dark | XXL (.accessibility3) | Dark + overflow |

## Screens captured

Defined in `screens.yaml`:

1. **Home** (tab 1) — HomeView with Hero Card + dose list
2. **Meds** (tab 2) — MedicationListView
3. **DoseLog** (tab 3) — DoseLogView with filters + stats band
4. **Family** (tab 4) — FamilyView with members
5. **Settings** (tab 5) — SettingsView

**v1 limitation:** tab bar level only — sheets, modals, Add flows deferred to v2.

## Execution Steps

### Step 1: Verify prerequisites

Check that these exist:
- [ ] `.claude/skills/audit-ui/screens.yaml` (this repo)
- [ ] Xcode project at `DoseSync/DoseSync.xcodeproj`
- [ ] Session defaults set (scheme=DoseSync, simulatorName=iPhone 17)

Run:
```
session_show_defaults
```

If missing, call:
```
session_set_defaults({
  projectPath: "/Users/vitalik/Documents/Projects/MobileApp/DoseSync/DoseSync.xcodeproj",
  scheme: "DoseSync",
  simulatorName: "iPhone 17"
})
```

### Step 2: Build + install app

```
build_sim() → check success
get_sim_app_path() → save path as $APP_PATH
get_app_bundle_id({appPath: $APP_PATH}) → save as $BUNDLE_ID
boot_sim() → wait for ready
install_app_sim({appPath: $APP_PATH})
```

### Step 3: Create output directory

```bash
mkdir -p DoseSync/audit-ui-screenshots
```

### Step 4: Capture 20 screenshots (5 screens × 4 states)

For each state combination (A/B/C/D):

#### 4.1 Set appearance (Light/Dark) via simctl

```bash
# Light mode:
xcrun simctl ui booted appearance light

# Dark mode:
xcrun simctl ui booted appearance dark
```

Use `Bash` tool to run this BEFORE launching app.

#### 4.2 Launch app with Dynamic Type args

**Normal Dynamic Type** — no launch args, default behaviour.

**XXL Dynamic Type** — launch with:
```
launch_app_sim({
  bundleId: $BUNDLE_ID,
  args: ["-UIPreferredContentSizeCategoryName", "UICTContentSizeCategoryAccessibilityXXL"]
})
```

Wait 2 seconds for app to stabilize.

#### 4.3 Navigate to each tab and capture

For each screen in `screens.yaml`:

1. Use `snapshot_ui()` to find tab bar button coordinates for this tab
2. Tap the tab using coordinates (via `gesture` tool if available, or via accessibility id)
3. Wait 1 second for transition
4. Call `screenshot({returnFormat: "path"})`
5. Move/rename screenshot to:
   ```
   DoseSync/audit-ui-screenshots/<screen>-<state>.png
   ```
   Example: `home-A-light-normal.png`, `home-B-light-xxl.png`, `home-C-dark-normal.png`, `home-D-dark-xxl.png`

After all 5 screens in current state, call `stop_app_sim()` before switching to next state.

**Performance optimization:** process all 5 screens in each state together before switching appearance — reduces appearance flip overhead.

### Step 5: Static code analysis

Scan `Views/` for defect patterns. For each, collect `file:line` + snippet.

#### 5.1 Missing accessibilityLabel on interactive elements

Grep for Button/ImageButton/Image without adjacent `.accessibilityLabel`:

```
Grep: 'Button\s*\{' in Views/ — for each hit, check if `.accessibilityLabel` appears within 10 lines below. If not → defect.
```

Known exempt:
- Buttons with `Text("...")` as label (auto-label from text)
- Buttons in `#Preview` blocks

#### 5.2 Fixed-size frames < 44pt

Grep:
```
'\.frame\(\s*(width|height):\s*(\d+)' in Views/
```

For each match where width or height < 44 AND element is interactive (Button, tap gesture), flag as touch target violation.

Known exempt:
- Decorative Images with `.accessibilityHidden(true)` nearby
- Icons in larger tappable wrappers (check 20 lines up for enclosing Button/tap)

#### 5.3 Hardcoded font sizes without Dynamic Type

Grep:
```
'\.font\(\.system\(size:\s*(\d+)' in Views/
```

Each match = hardcoded size that won't scale with Dynamic Type. Flag unless:
- Inside `AppStoreAssets/` or `MilestoneShareCardView` (fixed-size marketing/share render)
- Followed by `.dynamicTypeSize(...)` modifier that bounds scaling

#### 5.4 Missing Dark Mode colors

Grep:
```
'\.foregroundColor\(\.white\)' OR '\.foregroundColor\(\.black\)' OR 'Color\.white' OR 'Color\.black'
```

Each direct white/black usage in Views = potential dark mode issue. Flag unless:
- Used as `.foregroundStyle` on gradient/image (OK)
- In `AppStoreAssets/` (marketing)
- Wrapped in adaptive modifier

### Step 6: Generate HTML report

Write `DoseSync/audit-ui-report.html` with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>DoseSync UI Audit — {DATE}</title>
  <style>
    body { font-family: -apple-system, sans-serif; max-width: 1400px; margin: 40px auto; padding: 20px; }
    h1 { border-bottom: 2px solid #2C7A7B; padding-bottom: 8px; }
    .grid { display: grid; grid-template-columns: 200px repeat(4, 1fr); gap: 12px; align-items: start; margin-bottom: 40px; }
    .grid img { width: 100%; border: 1px solid #ddd; border-radius: 8px; }
    .state-label { font-weight: 600; text-align: center; padding: 8px; background: #f5f5f5; border-radius: 4px; }
    .screen-label { font-weight: 600; align-self: center; }
    .defects table { border-collapse: collapse; width: 100%; }
    .defects th, .defects td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
    .defects th { background: #f5f5f5; }
    .severity-high { color: #C53030; font-weight: 600; }
    .severity-medium { color: #D69E2E; font-weight: 600; }
    .severity-low { color: #2F855A; font-weight: 600; }
    .summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 20px 0; }
    .metric { background: #f5f5f5; padding: 16px; border-radius: 8px; text-align: center; }
    .metric-value { font-size: 32px; font-weight: bold; color: #2C7A7B; }
    .metric-label { font-size: 14px; color: #666; }
  </style>
</head>
<body>
  <h1>DoseSync UI Audit — {DATE}</h1>

  <div class="summary">
    <div class="metric"><div class="metric-value">{SCREENS}</div><div class="metric-label">Screens</div></div>
    <div class="metric"><div class="metric-value">{STATES}</div><div class="metric-label">States</div></div>
    <div class="metric"><div class="metric-value">{SCREENSHOTS}</div><div class="metric-label">Screenshots</div></div>
    <div class="metric"><div class="metric-value">{DEFECTS}</div><div class="metric-label">Defects</div></div>
  </div>

  <h2>Screenshot Grid</h2>
  <div class="grid">
    <div></div>
    <div class="state-label">A — Light / Normal</div>
    <div class="state-label">B — Light / XXL</div>
    <div class="state-label">C — Dark / Normal</div>
    <div class="state-label">D — Dark / XXL</div>

    <!-- Repeat for each screen -->
    <div class="screen-label">Home</div>
    <img src="audit-ui-screenshots/home-A-light-normal.png" />
    <img src="audit-ui-screenshots/home-B-light-xxl.png" />
    <img src="audit-ui-screenshots/home-C-dark-normal.png" />
    <img src="audit-ui-screenshots/home-D-dark-xxl.png" />
    <!-- ... Meds, DoseLog, Family, Settings ... -->
  </div>

  <h2>Defects ({N})</h2>
  <div class="defects">
    <table>
      <tr><th>Severity</th><th>Category</th><th>File:Line</th><th>Issue</th><th>Suggested fix</th></tr>
      <!-- rows generated from static analysis -->
    </table>
  </div>
</body>
</html>
```

### Step 7: Summary to user

Print concise summary:

```
UI Audit complete.

Screenshots: 20 captured ({count_success}/{count_total} successful)
Defects: {N} total
  - High (missing a11y labels on interactive): {count}
  - Medium (touch targets < 44pt): {count}
  - Medium (hardcoded font sizes): {count}
  - Low (direct white/black colors): {count}

Report: open DoseSync/audit-ui-report.html

Top 3 to fix:
1. {defect 1 with file:line}
2. {defect 2}
3. {defect 3}
```

## Limitations (v1)

- **Tab bar screens only** — sheets, modals, Add flows not captured
- **Grandparent Mode** not audited — v2
- **No VoiceOver audit** — requires XCUITest, v2
- **No automated contrast measurement** — pixel sampling in v2
- **Only Normal + XXL** — middle Dynamic Type sizes skipped

## v2 roadmap

- Sheet/modal navigation (Add Medication, Confirm Dose, paywall)
- Grandparent Mode separate audit
- VoiceOver audit via XCUITest
- Pixel-level contrast measurement (WCAG AA/AAA verification)
- Side-by-side diff vs previous audit (visual regression)

## Troubleshooting

**Simulator doesn't boot:** run `xcrun simctl list devices` to verify iPhone 17 exists. Adjust `simulatorName` in session_set_defaults.

**Screenshot files empty (0 bytes):** app may have crashed. Check `launch_app_sim` output for errors. Try `stop_app_sim` + relaunch.

**Tab bar coordinates wrong:** different device sizes have different tab bar positions. Use `snapshot_ui()` on first capture to get actual coordinates, then reuse.

**Dark mode doesn't apply:** restart simulator with `xcrun simctl shutdown booted && xcrun simctl boot "iPhone 17"`. Some iOS versions require fresh boot after appearance change.

**Dynamic Type XXL args ignored:** verify launch arg format. iOS accepts `UICTContentSizeCategoryAccessibilityXXL` (not `.xxxLarge` or `accessibility3`).
