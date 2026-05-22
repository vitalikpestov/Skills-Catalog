---
name: appstore-screens
description: "Generates App Store preview screenshots for DoseSync via SwiftUI ImageRenderer. v2.0 supports 15 screens × 3 CPPs × 4 locales (EN/RU/FR/ES) with theme presets, canvas-relative typography, layout rotation matrix, and brand-canonical color (#00C896). Path B chosen vs ParthJadhav Next.js skill (see audit 33). Outputs RGB-flat PNG at iPhone 6.9\" (1290×2796), naming: iphone-69-{cpp}-{order}-{slug}-{locale}.png."
---

# App Store Screens — DoseSync (v2.0)

> **Updated 2026-04-19 (v2.0):** scaled from 5-screen single-CPP EN-only к 15 screens × 3 CPPs × 4 locales matching [Brief.md v3.2](../../../DoseSync/Marketing/App-Store-Screenshots-Brief.md). Integrates [ParthJadhav skill audit findings](../../../Design/AAA-2026-04-18/33-appstore-screens-skill-gap-audit.md).

Generates App Store preview screenshots via SwiftUI `ImageRenderer`. Composes phone mockup + text overlay + brand surface into PNG files at Apple-required resolutions. **Path B chosen vs Next.js + html-to-image (ParthJadhav)** — real iOS UI ensures brand consistency with launched app.

## When to invoke

- "create app store screenshots", "generate appstore screens"
- "make launch screenshots", "build marketing previews"
- Before TestFlight submission
- When updating App Store assets after major UI changes

## Output (v2.0)

**60 PNG files minimum** (15 screens × 4 locales × 1 device = 6.9" iPhone).

| Device | Resolution | Required | File count |
|---|---|---|---|
| iPhone 6.9" (16 Pro Max) | 1290 × 2796 | **Yes** | 60 |
| iPhone 6.5" | 1284 × 2778 | Optional | +60 |
| iPhone 6.3" | 1206 × 2622 | Optional | +60 |

Output PNGs written to `DoseSync/AppStoreAssets/screenshots/` with naming:

```
iphone-{device}-{cpp}-{order}-{slug}-{locale}.png

Examples:
iphone-69-caregiver-01-replace-group-chat-en-US.png
iphone-69-caregiver-01-replace-group-chat-ru.png
iphone-69-grandparent-02-one-tap-no-confusion-fr-FR.png
iphone-69-parent-04-doctor-ready-pdf-es-ES.png
```

**CRITICAL:** PNGs must be RGB flat (no alpha channel) — App Store rejects alpha. See `flattenToRGB()` in renderer.

## Architecture (v2.0)

### 1. `ScreenshotComposerView.swift` (SwiftUI)

Reusable view consuming `ScreenshotSpec` struct, rendering one of 10 layout patterns:

```swift
struct ScreenshotSpec {
    let id: String              // "SS1.1"
    let cpp: CPP                // .caregiver / .grandparent / .parent
    let theme: ScreenshotTheme  // tokens: bg, fg, accent, muted
    let layout: ScreenshotLayout
    let headline: LocalizedStringKey
    let subtitle: LocalizedStringKey?
    let locale: Locale          // en-US / ru / fr-FR / es-ES
    let device: Device          // .iphone69 / .iphone65 / .iphone63
}

enum CPP: String { case caregiver, grandparent, parent }

enum ScreenshotLayout {
    case splitScreen(beforeImage: Image, afterImage: Image)
    case twoPhoneOverlay(back: Image, front: Image)
    case singleWithAlert(phone: Image, alertText: LocalizedStringKey)
    case heroElement(symbol: String)
    case fullBleedUI(screen: Image)
    case centeredPhoneWarmScene(phone: Image, sceneImage: Image)
    case contrast(headline: LocalizedStringKey)              // SS2.2, SS3.5
    case layeredNotification(phone: Image, overlay: Image)
    case statHero(badge: String, chainImage: Image)          // SS3.3 streak
    case bigNumber(number: String, caption: LocalizedStringKey)  // SS3.4 «97%»
}

struct ScreenshotTheme {
    let bg: Color
    let fg: Color
    let accent: Color   // ALWAYS Color.DS.V2.Brand.base (#00C896)
    let muted: Color

    static let caregiver = ScreenshotTheme(
        bg: .white,
        fg: Color(hex: 0x1A1A1A),
        accent: Color.DS.V2.Brand.base,
        muted: Color(hex: 0x6B7280)
    )
    static let grandparent = ScreenshotTheme(
        bg: Color(hex: 0xFAF7F2),
        fg: Color(hex: 0x1A1A1A),
        accent: Color.DS.V2.Brand.base,
        muted: Color(hex: 0x6B7280)
    )
    static let parent = ScreenshotTheme(
        bg: Color(hex: 0x0F172A),
        fg: .white,
        accent: Color.DS.V2.Brand.base,
        muted: Color(hex: 0x94A3B8)
    )
}
```

**Canvas-relative typography** (per ParthJadhav skill audit §G5):

```swift
private var canvasWidth: CGFloat { spec.device.dimensions.width }
private var headlineSize: CGFloat { canvasWidth * 0.085 }   // 110pt at 1290
private var subtitleSize: CGFloat { canvasWidth * 0.038 }   // 49pt at 1290
private var heroHeadlineSize: CGFloat { canvasWidth * 0.10 } // 129pt at 1290
private var bigNumberSize: CGFloat { canvasWidth * 0.40 }    // 516pt at 1290 — SS3.4 «97%»
```

**Composer body:**

```swift
var body: some View {
    ZStack {
        spec.theme.bg.ignoresSafeArea()

        switch spec.layout {
        case .splitScreen(let before, let after):
            splitScreenLayout(before: before, after: after)
        case .twoPhoneOverlay(let back, let front):
            twoPhoneLayout(back: back, front: front)
        case .singleWithAlert(let phone, let alert):
            singleWithAlertLayout(phone: phone, alertText: alert)
        case .heroElement(let symbol):
            heroElementLayout(symbol: symbol)
        case .fullBleedUI(let screen):
            fullBleedLayout(screen: screen)
        case .centeredPhoneWarmScene(let phone, let scene):
            warmSceneLayout(phone: phone, scene: scene)
        case .contrast(let headline):
            contrastLayout(headline: headline)
        case .layeredNotification(let phone, let overlay):
            layeredNotificationLayout(phone: phone, overlay: overlay)
        case .statHero(let badge, let chain):
            statHeroLayout(badge: badge, chain: chain)
        case .bigNumber(let number, let caption):
            bigNumberLayout(number: number, caption: caption)
        }
    }
    .environment(\.locale, spec.locale)
    .frame(width: spec.device.dimensions.width,
           height: spec.device.dimensions.height)
}
```

### 2. `ScreenshotRenderer.swift` (CLI/preview export)

Loops over (spec × locale × device), renders, flattens alpha, writes PNG:

```swift
@MainActor
func renderAllScreenshots() throws {
    let outputDir = URL(fileURLWithPath: "DoseSync/AppStoreAssets/screenshots")
    try FileManager.default.createDirectory(at: outputDir, withIntermediateDirectories: true)

    let specs = SpecLoader.load()  // from screenshot-specs.yaml
    let locales: [Locale] = [
        .init(identifier: "en-US"),
        .init(identifier: "ru"),
        .init(identifier: "fr-FR"),
        .init(identifier: "es-ES"),
    ]

    for spec in specs {
        for locale in locales {
            for device in spec.devices {
                let localized = spec.with(locale: locale, device: device)
                let view = ScreenshotComposerView(spec: localized)
                let renderer = ImageRenderer(content: view)
                renderer.scale = 3.0  // @3x for exact pixel count

                guard let uiImage = renderer.uiImage else { continue }
                let flattened = flattenToRGB(uiImage)  // CRITICAL — no alpha
                guard let data = flattened.pngData() else { continue }

                let filename = "iphone-\(device.shortCode)" +
                               "-\(spec.cpp.rawValue)" +
                               "-\(String(format: "%02d", spec.order))" +
                               "-\(spec.slug)" +
                               "-\(locale.identifier).png"
                try data.write(to: outputDir.appending(component: filename))
            }
        }
    }
}

/// CRITICAL: App Store rejects PNGs with alpha channel.
/// Flatten by drawing on opaque white background.
private func flattenToRGB(_ image: UIImage) -> UIImage {
    let format = UIGraphicsImageRendererFormat()
    format.opaque = true
    let renderer = UIGraphicsImageRenderer(size: image.size, format: format)
    return renderer.image { ctx in
        UIColor.white.setFill()
        ctx.fill(CGRect(origin: .zero, size: image.size))
        image.draw(at: .zero)
    }
}
```

### 3. `screenshot-specs.yaml` v2.0

15 screens × 3 CPPs × 4 locales — full spec. See [`screenshot-specs.yaml`](./screenshot-specs.yaml) for current state.

Sections:
- `target_devices` — iPhone 6.9" required, 6.5"/6.3" optional
- `locales` — EN/RU/FR/ES with per-locale length budgets
- `themes` — caregiver/grandparent/parent/contrast (token-driven)
- `typography` — canvas-relative formulas
- `mockup_iphone` — positioning metrics (5.2% / 89.8% / 12.6%)
- `layout_patterns` — 10 enum values
- `cpps` — 3 audiences with screens nested
- `persona_colors` + `persona_names` — Anna/Mike/Mom cross-screen
- `mock_medication_names` — generic per locale (no real drugs)
- `output` — naming convention + RGB flatten requirement
- `content_guardrails` — banned drugs/dosages/medical claims
- `brand_color_enforcement` — `#00C896` canonical, banned `#34C759`/`#0DBD8C`/`#007AFF`

## Execution Steps

When user invokes `/appstore-screens`:

### Step 1: Verify prerequisites

- [ ] `DoseSync/DoseSync/AppStoreAssets/ScreenshotComposerView.swift` exists (or offer to create it)
- [ ] `DoseSync/DoseSync/AppStoreAssets/ScreenshotRenderer.swift` exists
- [ ] `DoseSync/DoseSync/AppStoreAssets/SpecLoader.swift` exists (YAML→Swift bridge)
- [ ] `.claude/skills/appstore-screens/screenshot-specs.yaml` v2.0 present (15 screens × 3 CPPs)
- [ ] Source screen mockups in `DoseSync/AppStoreAssets/source/` (10 baseline iOS PNGs)

### Step 2: Capture source screens (if missing)

For each `source_screen` in YAML `source_screens.required` list:
1. Use XcodeBuildMCP `screenshot` to capture current app state from simulator
2. Navigate simulator to the right screen with mock data:
   - Mom dependent (no real name)
   - Generic «Morning vitamin» / «Evening drops» (no real drug names)
   - Anna/Mike/Mom caregivers (cross-screen persona system)
3. Save to `AppStoreAssets/source/<slug>.png`

**Guardrail check (automated):**
- Source screens must NOT show real medication names (`banned_in_mock_data` list)
- Source screens must NOT show dosages (regex `\d+\s*(mg|mcg|ml|g|IU)`)
- Run `copy-lint` skill to verify post-capture

### Step 3: Render compositions

Run `ScreenshotRenderer.renderAllScreenshots()` via Xcode preview export OR a command-line Swift script target.

**Output:** 60 PNGs in `DoseSync/AppStoreAssets/screenshots/` (15 screens × 4 locales × 1 device).

For optional 6.5" + 6.3" device variants: enable in YAML `target_devices` (180 PNGs total).

### Step 4: Validate output

For each generated PNG:

```bash
# Dimension check
sips -g pixelWidth -g pixelHeight file.png
# expect: 1290 × 2796 для iphone-69

# RGB flat check (no alpha)
pngcheck -v file.png | grep -i alpha
# expect: empty output (no alpha channel)

# File size check
du -h file.png
# expect: < 8MB per file
```

For each headline/subtitle:
- 1-second arm's-length test: open at Figma-equivalent 200% zoom, blur eyes — main words must register
- Thumbnail test: render at 280×624 (ASC grid view size) — headline still legible

### Step 5: Report

Print summary:
- Files generated (count + paths)
- Dimensions verified
- Alpha channels stripped (count)
- Locale coverage (4/4 EN/RU/FR/ES)
- CPP coverage (3/3 caregiver/grandparent/parent)
- Next step: upload via Xcode Organizer or App Store Connect (3 Custom Product Pages)

## Content Guidelines (per Brief v3.2 + skill audit)

### Headline rules
- **One idea per slide.** Никогда «and»-join.
- **3-5 words EN** (hero exception ≤6 для 1-2 slides).
- **Per-locale budgets:** EN ≤32 chars / RU ≤38 / FR ≤40 / ES ≤39.
- **3 approaches per CPP** (paint-moment / state-outcome / kill-pain) — каждый CPP должен использовать все 3.

### Layout rotation rule
- No 2 consecutive slides одинаковой композиции
- Минимум 2 contrast slides на 15-screen набор (SS2.2 + SS3.5)
- 1 big-number slide (SS3.4 «97%»)

### Tone per locale
- **EN:** «you / your», avoid «I» в push/CTA, gender-neutral
- **RU:** «Вы»-form only, never «ты». Run `python3 scripts/check_ru_tone.py` post-merge.
- **FR:** `vous` formal, non-breaking spaces перед `:`/`!`/`?`/`»`
- **ES:** `usted` 3rd-person formal, opening `¿`/`¡`

### Brand color enforcement
- **Canonical:** `#00C896` (`Color.DS.V2.Brand.base`) — same as iOS app + landing + press kit + email
- **Banned:** `#34C759` (system green), `#0DBD8C` (legacy), `#007AFF` (system blue для primary action)
- **Persona rings preserved:** `#3B82F6` Anna / `#F97316` Mike / `#A855F7` Mom — identity only, никогда не primary action

### Guardrails (medical compliance)
- 0 real drug names (use generic «Morning vitamin», «Evening drops»)
- 0 dosages (regex check)
- 0 medical claims («clinically proven», «FDA», «cures», «prescription»)
- Disclaimer на last screen каждого CPP: «DoseSync is a coordination tool, not a medical recommendation.»

## Typography (v2.0 — canvas-relative)

| Element | Formula | Size at cW=1290 | Weight | Line-height |
|---------|------|------|------|------|
| Hero headline | `cW × 0.10` | 129pt | 700 | 0.92 |
| Standard headline | `cW × 0.085` | 110pt | 700 | 1.0 |
| Subtitle | `cW × 0.038` | 49pt | 500 | 1.2 |
| Caption | `cW × 0.028` | 36pt | 600 | 1.3 |
| Big number (SS3.4) | `cW × 0.40` | 516pt | 800 | 1.0 |

**System font stack:** SF Pro (iOS native default). No custom typefaces in screenshot composition.

## Limitations

- **First-time setup** requires creating `AppStoreAssets/` group in Xcode project with target membership for a command-line или Preview target
- **Source screens** must be captured manually the first time (XcodeBuildMCP screenshot) — automation of simulator navigation is v3 work
- **A/B variants** — для A/B tests, duplicate spec в YAML с different headline/layout (variant-specific files have `-a` / `-b` suffix)
- **Hybrid composition layer** для contrast slides (SS2.2/SS3.5) — pure SwiftUI без real iOS screen, composer handles via `.contrast` layout case

## What this skill does NOT do

- Does not upload к App Store Connect — manual step via Xcode Organizer
- Does not auto-translate copy — Content Creator delivers final per-locale text via [appstore-screenshots-copy.md v3.2](../../../DoseSync/Marketing/appstore-screenshots-copy.md)
- Does not test on physical device — simulator render only
- Does not make design decisions — takes pre-defined specs from YAML as input
- Does not generate Android Play Store screenshots — iOS-only launch v1.0

## v3 roadmap (post-launch)

- iPad screenshot variants (12.9" 2064×2752 if iPad build shipped)
- Apple Watch companion screenshots
- 30s App Preview Video composition (separate from static screenshots)
- Automated simulator navigation для source screen capture
- A/B variant matrix support (multi-headline per slide for ASC experimentation)
- ASC upload automation via Fastlane integration

## Related docs

- **Canonical brief:** [App-Store-Screenshots-Brief.md v3.2](../../../DoseSync/Marketing/App-Store-Screenshots-Brief.md) — design + composition spec
- **Canonical copy:** [appstore-screenshots-copy.md v3.2](../../../DoseSync/Marketing/appstore-screenshots-copy.md) — 15 screens × 4 locales
- **Skill audit:** [33-appstore-screens-skill-gap-audit.md](../../../Design/AAA-2026-04-18/33-appstore-screens-skill-gap-audit.md) — ParthJadhav comparison
- **Implementation plan:** [34-appstore-screens-improvement-plan.md](../../../Design/AAA-2026-04-18/34-appstore-screens-improvement-plan.md) — 4 phases, ~14h total
- **Designer brief paste-ready:** [Designer-Brief-Paste-Ready.md](../../../DoseSync/Marketing/Designer-Brief-Paste-Ready.md) — Google Doc handoff
