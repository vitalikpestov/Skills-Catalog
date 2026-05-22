# Mobile Skills Catalog

> **Каталог скиллов для разработки мобильных приложений**
> Обновлено: 22 мая 2026
> Папка: `MASTER skills/_Mobile-Dev/`
> Структура: 11 разделов · ~70 mobile-related скиллов в `_Mobile-Dev/` + cross-refs на другие категории vault
> Навигатор по папке: см. `_Mobile-Dev/_index.md` (структура), `_Mobile-Dev/Android/_index.md` (Android), README в каждой подпапке.
>
> 🎯 **Быстрый старт:** [`top-13-design-picks.md`](top-13-design-picks.md) — курируемая выборка 13 design-скиллов с decision matrix и рекомендованными сочетаниями для разных сценариев.

---

## Быстрая навигация

| Задача | Скилл | Где |
|---|---|---|
| Native iOS HIG (Safe Areas, Dynamic Island, VoiceOver) | `claude-code-apple-skills` | `from-article-18-ui-ux/` |
| iOS 26+ / Liquid Glass / SwiftUI / SwiftData | `vabole-apple-skills` (36 скиллов) | `from-reddit-mobile-apps/` |
| Swift от Paul Hudson | `Swift-Agent-Skills` | `from-reddit-mobile-apps/` |
| Material Design 3 (Compose) | `material-3-skill` | `Android/from-hamen/` |
| Google Official Android (18 скиллов) | `android-skills` | `from-reddit-mobile-apps/` |
| Compose + MVVM (opinionated) | `claude-android-skill` | `from-reddit-mobile-apps/` |
| Expo Build Native UI (+46% adherence) | `expo-skills` | `from-reddit-mobile-apps/` |
| React Native + Vercel best practices | `agent-skills/react-native-skills` | `from-article-18-ui-ux/` |
| ASO Audit + Apple Search Ads | `aso-skills` | `from-reddit-mobile-apps/` |
| App Store Preflight (pre-submit) | `app-store-preflight-skills` | `from-reddit-mobile-apps/` |
| App icon AI generation | `snapai` + `code-with-beto-skills` | `from-reddit-mobile-apps/` |
| Paywall / Subscription / Retention | `product-monetization/*` | `from-vault-audit/` |
| Mobile attribution / UA | `marketing-mobile/*` | `from-vault-audit/` |
| 67 UI стилей с auto design system | `ui-ux-pro-max-skill` | `from-ui-ux-pro-max/` |
| 11 эстетик (Swiss, Brutalism, Glassmorphism…) | `frontend-design-pro-demo` | `from-article-18-ui-ux/` |
| APK reverse engineering | `android-reverse-engineering-skill` | `from-reddit-mobile-apps/` |
| Universal agentic framework | `superpowers` | `Android/from-superpowers/` |
| Awesome list поиск | `voltagent` · `composio` · `travisvn` | разные |

---

## 📱 iOS / Swift / SwiftUI / SwiftData

### Native iOS — основные

| Скилл | Источник | ⭐ | Описание |
|---|---|---|---|
| `claude-code-apple-skills` | [rshankras](https://github.com/rshankras/claude-code-apple-skills) | 217 | iOS HIG: Safe Areas, Dynamic Island, Tab Bars, Modals, Dark Mode (semantic colors), Dynamic Type, VoiceOver. Активация: `"iOS app"`, `"iPhone interface"`, `"SwiftUI design"`, `"HIG compliance"` |
| `Swift-Agent-Skills` | [twostraws (Paul Hudson)](https://github.com/twostraws/Swift-Agent-Skills) | 1,588 | От автора Hacking with Swift. Swift, SwiftUI, SwiftData, modern Apple frameworks. Identifies and fixes common mistakes AI agents make when writing SwiftUI |
| `vabole-apple-skills` | [vabole](https://github.com/vabole/apple-skills) | — | **iOS 26+, Liquid Glass.** 36 скиллов — самое детальное покрытие Apple ecosystem |
| `patrickserrano-skills` | [patrickserrano](https://github.com/patrickserrano/skills) | — | iOS, Swift, SwiftUI collection |
| `keskinonur-claude-code-ios-dev-guide` | [keskinonur](https://github.com/keskinonur/claude-code-ios-dev-guide) | — | PRD-driven workflows, ultrathink, planning modes для SwiftUI |

### vabole/apple-skills — 36 скиллов (детально)

> Все в `from-reddit-mobile-apps/vabole-apple-skills/skills/`

**Apple frameworks:**
| Скилл | Назначение |
|---|---|
| `appintents` | App Intents (Siri integration, iOS 16+) |
| `backgroundtasks` | Background tasks API |
| `combine` | Combine reactive framework |
| `core-animation` | Core Animation, CALayer |
| `corehaptics` | Haptic feedback (iPhone 8+) |
| `eventkit` | Calendar / Reminders |
| `healthkit` | HealthKit integration |
| `mapkit` | MapKit, Apple Maps |
| `photosui` | PhotosUI, PHPicker |
| `simulator-utils` | iOS Simulator helpers |
| `storekit` | StoreKit 2 (in-app purchases) |
| `swiftdata` | SwiftData (Core Data successor) |
| `swiftui` | SwiftUI general |
| `tipkit` | TipKit (iOS 17+ user education) |
| `uikit` | UIKit fallbacks |
| `usernotifications` | Push + local notifications |
| `widgetkit` | WidgetKit (Home Screen widgets) |
| `xcuitest` | XCUITest UI testing |
| `swift-concurrency` | async/await, actors |
| `swift-testing` | Swift Testing framework (replaces XCTest) |

**Guides (deep-dive):**
| Скилл | Назначение |
|---|---|
| `guide-macos-spm-packaging` | macOS Swift Package Manager packaging |
| `guide-swift-concurrency` | async/await deep guide |
| `guide-swift-testing` | Swift Testing patterns |
| `guide-swiftdata` | SwiftData best practices |
| `guide-swiftui-animations` | SwiftUI animations |
| `guide-swiftui-charts` | Swift Charts |
| `guide-swiftui-performance-audit` | SwiftUI perf audit |
| `guide-swiftui-ui-patterns` | UI patterns |
| `guide-swiftui-view-refactor` | View refactoring |

**Special / design-focused:**
| Скилл | Назначение |
|---|---|
| `hig` | Apple HIG strict compliance |
| `apple-aso` | ASO Audit |
| `apple-docs-index` | Apple docs search index |
| `ios-design-consultant` | UI/UX consulting на iOS |
| `ios-dev` | General iOS dev workflow |
| `ios-liquid-glass` | **iOS 26+ Liquid Glass material** |
| `ios-ui-craft` | UI craft / polish |

### iOS из vault audit (Focus Buddi / Sipper)

> Все в `from-vault-audit/ios-dev/`

| Скилл | Назначение |
|---|---|
| `app-clips` | iOS App Clips (lightweight приложения через QR / NFC) |
| `app-icon-optimization` | Оптимизация иконки приложения |
| `appstore-screens` | Генерация App Store скриншотов (`screenshot-specs.yaml`) |
| `arch-check` | Architecture check |
| `figma-ios-design-pipeline` | Figma → iOS pipeline (references + scripts) |
| `in-app-events` | In-App Events (App Store discoverability) |
| `stripe-integration-expert` | Stripe для iOS |
| `svg-animations` | SVG анимации |
| `test-gaps` | Test coverage gaps |
| `tokens-sync` | Design tokens sync (`mapping.yaml`) |

### iOS базовые (исходные)

> В `_Mobile-Dev/iOS/`

| Скилл | Назначение |
|---|---|
| `AI ASO` | AI-powered ASO: keyword research, competitor analysis |
| `app-store-optimization` | Полный ASO toolkit: metadata, конверсия, рейтинги |
| `Adam Lyttle/` | SwiftUI репозитории: onboarding, paywall, OpenAI wrapper, notchy, ASO screenshots |

---

## 🤖 Android / Kotlin / Compose

### Google Official `android/skills` — 18 скиллов

> [github.com/android/skills](https://github.com/android/skills) (4,516⭐) — `from-reddit-mobile-apps/android-skills/`

**Jetpack Compose:**
| Скилл | Назначение |
|---|---|
| `jetpack-compose/adaptive` | Adaptive layouts (foldables, tablets) |
| `jetpack-compose/migration/migrate-xml-views-to-jetpack-compose` | Миграция XML → Compose |
| `jetpack-compose/theming/styles` | Compose theming |
| `wear/jetpack-compose-m3` | Wear OS + Compose M3 |
| `xr/display-glasses-with-jetpack-compose-glimmer` | XR / glasses |

**System / Performance:**
| Скилл | Назначение |
|---|---|
| `system/edge-to-edge` | Edge-to-edge UI (Android 15) |
| `performance/r8-analyzer` | R8 analyzer |
| `profilers/perfetto-trace-analysis` | Perfetto trace analysis |
| `profilers/perfetto-sql` | Perfetto SQL queries |
| `build/agp/agp-9-upgrade` | Android Gradle Plugin 9 upgrade |

**Navigation / Camera / Devtools:**
| Скилл | Назначение |
|---|---|
| `navigation/navigation-3` | Navigation 3 (новая версия) |
| `camera/camera1-to-camerax` | Camera1 → CameraX миграция |
| `devtools/android-cli` | Android CLI |
| `testing/testing-setup` | Testing setup (JUnit, Espresso, Compose tests) |

**Play / Identity / Device AI:**
| Скилл | Назначение |
|---|---|
| `play/play-billing-library-version-upgrade` | Play Billing upgrade (in-app purchases) |
| `play/engage-sdk-integration` | Engage SDK |
| `identity/verified-email` | Verified email identity |
| `device-ai/appfunctions` | App Functions (on-device AI) |

### Material Design 3

| Скилл | Источник | ⭐ | Описание |
|---|---|---|---|
| `material-3-skill` | [hamen](https://github.com/hamen/material-3-skill) | — | **Material Design 3 (Material You).** Primary: Jetpack Compose Material3 (MaterialTheme, components, adaptive layout). Также Flutter и limited web (@material/web, maintenance mode). Покрывает tokens, 30+ компонентов, layout, theming, M3 Expressive, accessibility. Активация: `"material design"`, `"MD3"`, `"material you"`, `"Jetpack Compose"`, `"MaterialTheme"` |

### Android — community

| Скилл | Источник | ⭐ | Назначение |
|---|---|---|---|
| `claude-android-skill` | [dpconde](https://github.com/dpconde/claude-android-skill) | 198 | Production-ready Compose + MVVM, **opinionated** — fewer options, better defaults |
| `android-skills-mcp` | [skydoves](https://github.com/skydoves/android-skills-mcp) | 178 | Packages Google's `android/skills` как **MCP server** через npx. Offline access, MCP-compatible agents |
| `android-reverse-engineering-skill` | [SimoneAvogadro](https://github.com/SimoneAvogadro/android-reverse-engineering-skill) | 5,440 | **APK reverse engineering** — decompile, smali bytecode, hidden endpoints, embedded API keys |

---

## ⚛️ React Native + Expo

| Скилл | Источник | ⭐ | Описание |
|---|---|---|---|
| `expo-skills` | [expo official](https://github.com/expo/skills) | 1,837 | **Expo Build Native UI.** +46% adherence к native UI patterns (внутренний бенчмарк Expo). Navigation, gestures, native modules, EAS, iOS 18 / iOS 26 / Android 16 |
| `agent-skills/skills/react-native-skills/` | [vercel-labs](https://github.com/vercel-labs/agent-skills) | 25,800 | Vercel: React Native — мобильная оптимизация с FlashList, GPU-ускоренные анимации |
| `agent-skills/skills/composition-patterns/` | Vercel | — | Compound components, scalable component architecture (применимо к RN) |
| `agent-skills/skills/react-best-practices/` | Vercel | — | 57 правил React в 8 категориях — общие best practices (применимы к RN) |

> **Flutter:** dedicated скиллов в нашем vault нет. Использовать `material-3-skill` (поддерживает Flutter MD3) и общие `voltagent-awesome-agent-skills` для поиска Flutter-скиллов.

---

## 🎨 UI/UX дизайн (cross-platform)

### Mega skills

| Скилл | Источник | ⭐ | Описание |
|---|---|---|---|
| `ui-ux-pro-max-skill` | [nextlevelbuilder](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 71k | **Самый популярный community-скилл.** Design system generator. 67 UI стилей (Glassmorphism, Claymorphism, Brutalism, Neumorphism, Swiss…), 161 цветовая палитра, 57 комбинаций шрифтов, 99 UX-гайдлайнов. Platforms: React, Next.js, Vue, Nuxt, Svelte, **Flutter**, **SwiftUI**, **React Native** |
| `taste-skill` | [Leonxlnx](https://github.com/Leonxlnx/taste-skill) | 13.3k | 9 variants + 3 imagegen скилла. 3 регулируемых параметра (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY). **`imagegen-frontend-mobile`** — экраны iOS/Android с mockup телефона |
| `designer-skills` | [Owl-Listener](https://github.com/Owl-Listener/designer-skills) | 833 | 63 скилла + 27 команд в 8 плагинах. Полный процесс: design-research, design-systems, ux-strategy, ui-design, interaction-design, prototyping-testing, design-ops, designer-toolkit, visual-critique |
| `frontend-design-pro-demo` | [claudekit](https://github.com/claudekit/frontend-design-pro-demo) | 212 | 11 эстетик с production-ready кодом: Swiss Minimalism, Neumorphism, Glassmorphism, Brutalism, Claymorphism, Aurora/Mesh Gradient, Retro-Futurism/Cyberpunk, 3D Hyperrealism, Vibrant Block/Maximalist, Dark OLED Luxury, Organic/Biomorphic |
| `interface-design` | [Dammyjay93](https://github.com/Dammyjay93/interface-design) | 4.7k | **Persistent design system** через `.interface-design/system.md` — сохраняется между сессиями. Решает проблему стилистического дрейфа |
| `bencium-claude-code-design-skill` | [bencium](https://github.com/bencium/bencium-claude-code-design-skill) | 189 | 28k+ chars UX reference. Два варианта: **Innovative** (смелые творческие выборы) и **Controlled** (согласованность и стандарты). Файлы: ACCESSIBILITY.md (WCAG 2.1/2.2), RESPONSIVE-DESIGN.md, MOTION-SPEC.md, DESIGN-SYSTEM-TEMPLATE.md |

### Утилитарные

| Скилл | Источник | ⭐ | Описание |
|---|---|---|---|
| `refactoring-ui-skill` | [LovroPodobnik](https://github.com/LovroPodobnik/refactoring-ui-skill) | 15 | Применяет систему Refactoring UI (Adam Wathan + Steve Schoger). Аудит иерархии, отступов, теней, цветов |
| `wondelai-skills/ux-heuristics/` | [wondelai](https://github.com/wondelai/skills) | 752 | **10 эвристик Нильсена** автоматически + принципы «Don't Make Me Think» Стива Круга. Severity scoring |
| `wondelai-skills/hooked-ux/` | wondelai | 752 | **Hook Model** Нира Эяля: trigger / action / reward / investment — где цикл удержания прерывается |
| `wondelai-skills/design-sprint/` | wondelai | 752 | 5-day Google Ventures Design Sprint в одном скилле |
| `emilkowalski-skill` | [emilkowalski](https://github.com/emilkowalski/skill) | — | Motion design, microinteractions, page transitions — для polish уровня Awwwards |
| `gstack` | [garrytan](https://github.com/garrytan/gstack) | — | **Design Rating 0-10** от CEO Y Combinator. Типографика, spacing, color, hierarchy, accessibility + AI Slop Detection |

### Universal Anthropic (в `anthropics-skills/`)

| Скилл | Назначение |
|---|---|
| `frontend-design` | Официальный Anthropic Frontend Design (118.3k⭐ — также в `_Engineering/`) |
| `theme-factory` | 10 курируемых тем (также в `_AI-Automation/`) |
| `brand-guidelines` | Brand guidelines enforcement |
| `canvas-design` | Visual art в .png/.pdf (также в `_Product-Apps/`) |

### UI/UX из vault audit

> В `from-vault-audit/quality/`

| Скилл | Назначение |
|---|---|
| `taste-check` | UI taste check |
| `audit-ui` | UI audit |
| `stop-slop` | Stop AI slop в дизайне |
| `impeccable` | Impeccable check |

---

## 🛍 ASO + App Store / Play Store

| Скилл | Источник | ⭐ | Описание |
|---|---|---|---|
| `aso-skills` | [Eronred](https://github.com/Eronred/aso-skills) | 1,159 | **App Store Listing Audit** + Apple Search Ads. Анализ listing quality, keyword presence, balance brand vs search, character waste, comparison с конкурентами |
| `app-store-preflight-skills` | [truongduy2611](https://github.com/truongduy2611/app-store-preflight-skills) | 1,133 | **Pre-submit scan** Xcode проекта: privacy manifests, undeclared entitlements, off-spec screenshots, deprecated SDKs, IAP configurations. Также для Mac App Store |
| `app-store-screenshots` | [ParthJadhav](https://github.com/ParthJadhav/app-store-screenshots) | — | Каркасит Next.js проект, создаёт рекламные дизайны с device-mockups, экспортирует во всех Apple resolution |
| `snapai` | [betomoedano](https://github.com/betomoedano/snapai) | 1,801 | Open-source CLI: AI icon generation через OpenAI image models, "nano banana" preset. Производит iOS 18 / iOS 26 / Android icons в один проход |
| `code-with-beto-skills` | [Code-with-Beto](https://github.com/Code-with-Beto/skills) | 77 | App Icon skill (uses SnapAI). Just tell Claude "generate an icon for X" — output ready для Icon Composer в Xcode 26 |

### ASO из vault audit + iOS-dev

| Скилл | Путь | Назначение |
|---|---|---|
| `appstore-screens` | `from-vault-audit/ios-dev/` | App Store скриншоты (с `screenshot-specs.yaml`) |
| `in-app-events` | `from-vault-audit/ios-dev/` | In-App Events (App Store discoverability feature) |
| `app-icon-optimization` | `from-vault-audit/ios-dev/` | App icon optimization workflow |
| `AI ASO`, `app-store-optimization` | `iOS/` | ASO базовые |
| `apple-aso` | `vabole-apple-skills/skills/` | ASO Audit от vabole |

---

## 📣 Mobile Marketing

> Все в `from-vault-audit/marketing-mobile/` (из App Dev Studio твоих проектов)

| Скилл | Назначение |
|---|---|
| `apple-search-ads` | Apple Search Ads campaigns |
| `ua-campaign` | **User Acquisition** campaigns |
| `attribution-setup` | **Mobile attribution** (Adjust, AppsFlyer, Branch) |
| `web-to-app-funnel` | Web → app conversion funnel |
| `meta-ads-skill` | Meta Ads для mobile |
| `review-management` | App reviews management |
| `launch-strategy` | Product launch plan |
| `press-and-pr` | Press + PR для запуска |

---

## 💳 Monetization / Subscription / Paywall

> Все в `from-vault-audit/product-monetization/`

| Скилл | Назначение |
|---|---|
| `paywall-optimization` | Paywall design optimization |
| `paywall-upgrade-cro` | **Paywall CRO** (conversion rate optimization) |
| `subscription-lifecycle` | Subscription lifecycle management |
| `retention-optimization` | Retention strategies |
| `churn-prevention` | Cancel flows, save offers, exit surveys, dunning |
| `onboarding-cro` | Onboarding conversion |
| `onboarding-optimization` | Onboarding flow optimization |
| `pricing-strategy` | Pricing decisions |
| `monetization-strategy` | Overall monetization |
| `saas-metrics-coach` | MRR, ARR, LTV, CAC, NRR |
| `ab-test-setup` | A/B testing |
| `position-me` | Product positioning |

### Связанные из Google android-skills

| Скилл | Назначение |
|---|---|
| `play/play-billing-library-version-upgrade` | Play Billing upgrade (Android in-app purchases) |

### Связанные из vabole-apple-skills

| Скилл | Назначение |
|---|---|
| `storekit` | StoreKit 2 (iOS in-app purchases) |

---

## 🛡 Quality / Pre-ship / Localization

> Все в `from-vault-audit/quality/`

| Скилл | Назначение |
|---|---|
| `ship-gate` | **Pre-production audit** — комплексный pre-ship check |
| `taste-check` | UI taste check |
| `audit-ui` | UI audit |
| `stop-slop` | Stop AI slop |
| `impeccable` | Impeccable code check |
| `i18n-translator` | i18n translation |
| `localization` | Localization workflow |

### Тестирование (cross-platform)

| Скилл | Откуда | Назначение |
|---|---|---|
| `test-gaps` | `from-vault-audit/ios-dev/` | Test coverage gaps |
| `xcuitest` | `vabole-apple-skills/skills/` | iOS XCUITest UI testing |
| `swift-testing` + `guide-swift-testing` | vabole | Swift Testing framework |
| `testing/testing-setup` | `android-skills/` (Google) | Android testing setup (JUnit, Espresso, Compose tests) |

---

## 🔐 Security (mobile-relevant)

| Скилл | Откуда | Назначение |
|---|---|---|
| `android-reverse-engineering-skill` | `from-reddit-mobile-apps/` | APK reverse engineering, security audits |
| Cross-ref → `_Engineering/security-reviewer/` | основной vault | General security review |
| Cross-ref → `_Engineering/env-secrets-manager/` | основной vault | .env safety, leak detection, key rotation |
| Cross-ref → `new-plugins/compliance-regulatory/gdpr-dsgvo-expert` | new-plugins | GDPR / DSGVO compliance (важно для App Store / Play Store submission) |

---

## 📚 Awesome Lists & Universal Frameworks

| Скилл | Источник | ⭐ | Описание |
|---|---|---|---|
| `voltagent-awesome-agent-skills` | [VoltAgent](https://github.com/VoltAgent/awesome-agent-skills) | 20,009 | **Самый большой awesome list.** 1000+ скиллов с `npx skills add`. Mobile секция включает Fastlane, Apple Developer certificates, RN bridging modules |
| `composio-awesome` | [ComposioHQ](https://github.com/ComposioHQ/awesome-claude-skills) | — | Curated awesome list |
| `travisvn-awesome-claude-skills` | [travisvn](https://github.com/travisvn/awesome-claude-skills) | — | Curated awesome list (Android/) |
| `superpowers` | [obra (Jesse Vincent)](https://github.com/obra/superpowers) | — | **Universal agentic framework.** Поддерживает Claude+Codex+Cursor+OpenCode через отдельные plugin-папки. 146 файлов. Хорош для параллельного запуска агентов на mobile PR, bug-hunting, workflow automation |
| `wondelai-skills` (parent) | [wondelai](https://github.com/wondelai/skills) | 752 | Целая директория скиллов: ux-heuristics, hooked-ux, design-sprint и др. |
| `anthropics-skills` (parent) | [anthropics](https://github.com/anthropics/skills) | — | Официальные Anthropic skills включая frontend-design, theme-factory, brand-guidelines |

---

## 🔗 Cross-ref: mobile-relevant из других категорий vault

Скиллы лежат в других категориях `MASTER skills/`, но критичны для мобильной разработки:

### _Engineering/

| Скилл | Mobile-применение |
|---|---|
| `frontend-design` | Anthropic Frontend Design (118.3k⭐) — также в `_Mobile-Dev/from-article-18-ui-ux/anthropics-skills/` |
| `stripe-best-practices` | Stripe для in-app subscriptions (web fallback) |
| `supabase-developer` | Backend для mobile apps (Auth, Storage, Real-time, Edge Functions, RLS) |
| `claude-api` | Anthropic SDK интеграция в mobile app |
| `database-designer` | Schema design для mobile backend |
| `websockets-realtime` | Real-time для chat, multiplayer, body doubling |
| `security-reviewer` | Security audit мобильного приложения |
| `env-secrets-manager` | .env / API keys / Keychain |
| `error-handling-patterns` | Error handling patterns (Result types для Swift) |
| `nextjs-app-router` | Landing page для mobile app (web-to-app funnel) |

### _Product-Apps/

| Скилл | Mobile-применение |
|---|---|
| `figma` | Figma MCP для design-to-code (iOS, Android, RN) |
| `ux-researcher-designer` | UX research, persona, journey maps, usability testing |
| `product-manager-toolkit` | RICE, customer interviews, PRD templates |
| `product-requirements` | Interactive Product Owner для PRD |
| `decision-helper` | Tech stack / framework decisions |
| `AI legal` | Privacy Policy, ToS для app submission, COPPA, GDPR |
| `canvas-design` | App icon mockups, marketing visuals |

### _Marketing/

| Скилл | Mobile-применение |
|---|---|
| `app-store-optimization` | ASO base skill (есть копия в `_Mobile-Dev/iOS/`) |
| `AI ASO` | AI-powered ASO |
| `competitive-landscape` | Анализ mobile-конкурентов (Inflow, Goblin Tools, etc.) |
| `email-marketing` | Email funnel для mobile app users |
| `pricing-strategy` | Pricing |
| `referral-program` | Referrals для mobile growth |

### _AI-Automation/

| Скилл | Mobile-применение |
|---|---|
| `theme-factory` | 10 pre-set тем для marketing pages, app screenshots |
| `skill-creator` | Создать кастомный mobile-скилл |
| `mcp-builder` | Написать MCP server для mobile workflow |
| `humanizer-main` | Убрать AI-признаки из App Store описания / маркетингового контента |
| `Claude Code` | CLI hooks, slash commands для mobile dev workflow |

### new-plugins/

| Скилл | Mobile-применение |
|---|---|
| `engineering-pro/ios-design-pipeline` (если есть) | iOS design pipeline |
| `engineering-pro/mobile-development` (если есть) | Mobile dev workflow |
| `product-growth/saas-metrics-coach` | MRR/ARR/LTV для mobile subscriptions |
| `product-growth/landing-page-generator` | Landing page для mobile app |
| `marketing-pro/paywall-upgrade-cro` | Mobile paywall (есть и в `from-vault-audit/`) |
| `marketing-pro/onboarding-cro` | Mobile onboarding |
| `marketing-pro/ai-seo` | App Store SEO (AI Overviews) |
| `marketing-pro/programmatic-seo` | Programmatic pages для app keywords |
| `marketing-pro/app-store-optimization` | ASO |
| `compliance-regulatory/gdpr-dsgvo-expert` | GDPR compliance для app submission |
| `c-level-advisor/cpo-advisor` | Product vision для mobile apps |

### _Telegram/ (если делаешь Telegram mini-apps)

| Скилл | Mobile-применение |
|---|---|
| `telegram-mini-app` | Telegram Mini Apps (TWA): TON ecosystem, Web App API, payments, auth |
| `telegram-bot-builder` | Bot для onboarding mobile users |

---

## Источники mobile-hub'а

| # | Источник | Статус | Скиллов |
|---|---|---|---|
| 1 | `pearson9/sw-ios-skills` | ❌ auth required | 0 |
| 2 | `mcpmarket/mobile-design-system` | ⚠️ JS-rendered | 0 (README) |
| 3 | `nextlevelbuilder/ui-ux-pro-max-skill` | ✅ | 1 |
| 4 | [P. Pillitteri «18 UI/UX скиллов»](https://pasqualepillitteri.it/ru/news/888/claude-code-18-luchshikh-skill-dlya-ui-ux-dizayna) | ✅ | 13 |
| 5 | Reddit `1s2dacs` | ❌ blocked → [замещён P. Pillitteri «Mobile 2026»](https://pasqualepillitteri.it/en/news/1802/best-claude-skills-mobile-development-2026) | 15 |
| 6 | Аудит Focus Buddi / Sipper / AppDev | ✅ | 37 + 1 .skill |
| 7 | `dpconde/claude-android-skill` | ✅ (дубль) | linked |
| 8 | `hamen/material-3-skill` | ✅ | 1 |
| 9 | `Mob-App/obai-marketplace` | ❌ auth required | 0 |
| 10 | `Mob-App/obai-mcp` | ❌ auth required | 0 |
| 11 | `travisvn/awesome-claude-skills` | ✅ | 1 |
| 12 | `ComposioHQ/awesome-claude-skills` | ✅ (дубль) | linked |
| 13 | `obra/superpowers` | ✅ | 1 |

**Итого скиллов в `_Mobile-Dev/`:** ~70 (3 базовых + 32 склонированных репо + 37 из vault audit)
**Размер папки:** ~160 MB

---

## Security warning

> **Snyk ToxicSkills (упомянуто в статье 18 UI/UX):** 36% протестированных Claude-скиллов содержат prompt injection. В экосистеме найдено 1467 вредоносных пейлоадов.

**Перед использованием любого скилла — открой `SKILL.md` и прочитай инструкции.**

**Безопасные источники (high trust):**
- Anthropic (`anthropics/*`)
- Google (`android/skills`)
- Expo (`expo/skills`)
- Vercel (`vercel-labs/agent-skills`)
- Paul Hudson (`twostraws/Swift-Agent-Skills`)
- Jesse Vincent / obra (`obra/superpowers`)

**Из vault audit (твои собственные скиллы из App Dev Studio):** проверены тобой при сборке проектов.
