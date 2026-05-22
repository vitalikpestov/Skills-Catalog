# _Mobile-Dev — навигатор

> Hub скиллов для разработки мобильных приложений (iOS, Android, React Native, Flutter).
> Создан 22 мая 2026. Заменил старую категорию `_iOS/`.

> 📖 **Полный каталог скиллов с описаниями:** [`mobile-skills-catalog.md`](mobile-skills-catalog.md) — этот файл больше про структуру папки, каталог — про сами скиллы с фактическими данными.

---

## Структура папки

```
_Mobile-Dev/
├── _index.md                       ← ты тут
├── iOS/                            ← существующие до миграции (3 шт.)
│   ├── AI ASO/
│   ├── Adam Lyttle/                ← SwiftUI репозитории
│   └── app-store-optimization/
│
├── Android/                        ← Android-specific hub (создан 22 мая 2026)
│   ├── _index.md                   ← навигатор по Android + ссылки на дубли
│   ├── from-hamen/                 ← material-3-skill (Compose)
│   ├── from-awesome-lists/         ← travisvn awesome list
│   ├── from-superpowers/           ← obra/superpowers (universal agentic)
│   └── from-obai/                  ← README: Mob-App/obai-* недоступны
│
├── from-ui-ux-pro-max/             ← Источник: nextlevelbuilder GitHub
│   └── ui-ux-pro-max-skill/        ← 71k stars, 67 UI стилей
│
├── from-article-18-ui-ux/          ← Источник: статья Pasquale Pillitteri (18 UI/UX скиллов)
│   ├── README.md                   ← навигатор по 18 + статусы
│   ├── claude-code-apple-skills/   ← rshankras, iOS HIG
│   ├── app-store-screenshots/      ← ParthJadhav, App Store ассеты
│   ├── agent-skills/               ← Vercel Labs (React Native)
│   ├── taste-skill/                ← Leonxlnx, imagegen-frontend-mobile
│   ├── interface-design/           ← Dammyjay93
│   ├── frontend-design-pro-demo/   ← claudekit (11 эстетик)
│   ├── designer-skills/            ← Owl-Listener (63 скилла)
│   ├── bencium-claude-code-design-skill/
│   ├── wondelai-skills/            ← ux-heuristics + hooked-ux + design-sprint
│   ├── refactoring-ui-skill/
│   ├── emilkowalski-skill/         ← motion / анимации
│   ├── gstack/                     ← Garry Tan (Y Combinator)
│   └── anthropics-skills/          ← официальные Anthropic (brand-guidelines)
│
├── from-reddit-mobile-apps/        ← Источник: Reddit заблокирован → статья Pasquale (mobile-specific)
│   ├── README.md
│   ├── aso-skills/                 ← Eronred, ASO Audit + Apple Search Ads
│   ├── app-store-preflight-skills/ ← truongduy2611, pre-submit
│   ├── code-with-beto-skills/      ← Beto Moedano (App Icon)
│   ├── snapai/                     ← SnapAI CLI для иконок
│   ├── expo-skills/                ← Expo official (+46% native UI)
│   ├── voltagent-awesome-agent-skills/  ← VoltAgent (1000+ скиллов)
│   ├── android-skills/             ← Google Official Android
│   ├── android-reverse-engineering-skill/ ← APK reverse
│   ├── claude-android-skill/       ← dpconde, Compose+MVVM
│   ├── android-skills-mcp/         ← Google skills as MCP server
│   ├── Swift-Agent-Skills/         ← Paul Hudson
│   ├── patrickserrano-skills/      ← iOS/Swift collection
│   ├── vabole-apple-skills/        ← iOS 26+, Liquid Glass
│   ├── keskinonur-ios-guide/       ← Claude Code + iOS workflow
│   └── composio-awesome/           ← awesome list
│
├── from-mobile-design-system/      ← Источник: MCP Market (JS-rendered, недоступно)
│   └── README.md                   ← описание + ссылки + альтернативы
│
└── from-vault-audit/               ← Найдено в Projects/Focus Buddi & Sipper
    ├── README.md
    ├── ios-dev/                    ← 10 нативных iOS скиллов
    ├── product-monetization/       ← 12 mobile-монетизация
    ├── marketing-mobile/           ← 8 mobile-маркетинг
    ├── quality/                    ← 7 quality/UI
    └── figma-ios-design-pipeline.skill ← zip-архив
```

---

## Быстрая навигация по задачам

### iOS / Swift / SwiftUI

| Задача | Скилл | Путь |
|---|---|---|
| Native iOS с HIG (Safe Areas, Dynamic Island, VoiceOver) | `claude-code-apple-skills` | `from-article-18-ui-ux/claude-code-apple-skills/` |
| Swift/SwiftUI от Paul Hudson | `Swift-Agent-Skills` | `from-reddit-mobile-apps/Swift-Agent-Skills/` |
| iOS 26+ / Liquid Glass | `vabole-apple-skills` | `from-reddit-mobile-apps/vabole-apple-skills/` |
| PRD + ultrathink для SwiftUI | `keskinonur-ios-guide` | `from-reddit-mobile-apps/keskinonur-ios-guide/` |
| iOS Swift коллекция | `patrickserrano-skills` | `from-reddit-mobile-apps/patrickserrano-skills/` |
| App Clips | `app-clips` | `from-vault-audit/ios-dev/app-clips/` |
| Figma → iOS pipeline | `figma-ios-design-pipeline` | `from-vault-audit/ios-dev/figma-ios-design-pipeline/` |
| Design tokens sync | `tokens-sync` | `from-vault-audit/ios-dev/tokens-sync/` |
| SwiftUI шаблоны (paywall, onboarding) | `Adam Lyttle/` | `iOS/Adam Lyttle/` |

### Android

> 📁 **Полный навигатор:** [`Android/_index.md`](Android/_index.md)

| Задача | Скилл | Путь |
|---|---|---|
| **Material Design 3 для Compose** | `material-3-skill` | `Android/from-hamen/material-3-skill/` |
| Google Official Android (Compose, AGP 9) | `android-skills` | `from-reddit-mobile-apps/android-skills/` |
| Compose + MVVM (opinionated) | `claude-android-skill` | `from-reddit-mobile-apps/claude-android-skill/` |
| Google skills как MCP server | `android-skills-mcp` | `from-reddit-mobile-apps/android-skills-mcp/` |
| APK reverse engineering | `android-reverse-engineering-skill` | `from-reddit-mobile-apps/android-reverse-engineering-skill/` |
| **Universal agentic framework** | `superpowers` (obra) | `Android/from-superpowers/superpowers/` |
| **Awesome list (поиск скиллов)** | `travisvn-awesome-claude-skills` | `Android/from-awesome-lists/` |

### React Native + Expo

| Задача | Скилл | Путь |
|---|---|---|
| Expo Official (+46% native UI) | `expo-skills` | `from-reddit-mobile-apps/expo-skills/` |
| React Native best practices | `agent-skills` (Vercel) | `from-article-18-ui-ux/agent-skills/` |

### App Store / ASO / Маркетинг

| Задача | Скилл | Путь |
|---|---|---|
| ASO Audit + Apple Search Ads | `aso-skills` | `from-reddit-mobile-apps/aso-skills/` |
| App Store Preflight (pre-submit) | `app-store-preflight-skills` | `from-reddit-mobile-apps/app-store-preflight-skills/` |
| App Store скриншоты | `app-store-screenshots` | `from-article-18-ui-ux/app-store-screenshots/` |
| Apple Search Ads (свой) | `apple-search-ads` | `from-vault-audit/marketing-mobile/apple-search-ads/` |
| UA Campaign | `ua-campaign` | `from-vault-audit/marketing-mobile/ua-campaign/` |
| Mobile Attribution Setup | `attribution-setup` | `from-vault-audit/marketing-mobile/attribution-setup/` |
| Web → App funnel | `web-to-app-funnel` | `from-vault-audit/marketing-mobile/web-to-app-funnel/` |
| App icon generation (AI) | `snapai` + `code-with-beto-skills` | `from-reddit-mobile-apps/snapai/` |
| App icon optimization | `app-icon-optimization` | `from-vault-audit/ios-dev/app-icon-optimization/` |
| App Store screens (свой) | `appstore-screens` | `from-vault-audit/ios-dev/appstore-screens/` |
| In-App Events (App Store feature) | `in-app-events` | `from-vault-audit/ios-dev/in-app-events/` |

### Monetization / Subscription / Retention

| Задача | Скилл | Путь |
|---|---|---|
| Paywall optimization | `paywall-optimization` | `from-vault-audit/product-monetization/paywall-optimization/` |
| Paywall CRO | `paywall-upgrade-cro` | `from-vault-audit/product-monetization/paywall-upgrade-cro/` |
| Subscription lifecycle | `subscription-lifecycle` | `from-vault-audit/product-monetization/subscription-lifecycle/` |
| Retention | `retention-optimization` | `from-vault-audit/product-monetization/retention-optimization/` |
| Churn prevention | `churn-prevention` | `from-vault-audit/product-monetization/churn-prevention/` |
| Onboarding CRO | `onboarding-cro` / `onboarding-optimization` | `from-vault-audit/product-monetization/` |
| SaaS / mobile metrics | `saas-metrics-coach` | `from-vault-audit/product-monetization/saas-metrics-coach/` |
| Pricing strategy | `pricing-strategy` | `from-vault-audit/product-monetization/pricing-strategy/` |
| A/B testing | `ab-test-setup` | `from-vault-audit/product-monetization/ab-test-setup/` |

### UI/UX дизайн (универсальные, применимы к mobile)

| Задача | Скилл | Путь |
|---|---|---|
| 67 UI стилей, авто design system | `ui-ux-pro-max-skill` | `from-ui-ux-pro-max/ui-ux-pro-max-skill/` |
| 11 эстетик (Swiss, Brutalism, Glassmorphism…) | `frontend-design-pro-demo` | `from-article-18-ui-ux/frontend-design-pro-demo/` |
| Регулируемые параметры (variance/motion/density) | `taste-skill` | `from-article-18-ui-ux/taste-skill/` |
| Persistent design system | `interface-design` | `from-article-18-ui-ux/interface-design/` |
| 63 design-скилла (полный процесс) | `designer-skills` | `from-article-18-ui-ux/designer-skills/` |
| 28k chars UX reference | `bencium-claude-code-design-skill` | `from-article-18-ui-ux/bencium-claude-code-design-skill/` |
| Refactoring UI (Adam Wathan) | `refactoring-ui-skill` | `from-article-18-ui-ux/refactoring-ui-skill/` |
| Nielsen 10 эвристик audit | `wondelai-skills/ux-heuristics/` | `from-article-18-ui-ux/wondelai-skills/` |
| Hook Model retention | `wondelai-skills/hooked-ux/` | `from-article-18-ui-ux/wondelai-skills/` |
| 5-day Design Sprint | `wondelai-skills/design-sprint/` | `from-article-18-ui-ux/wondelai-skills/` |
| Motion / микроинтеракции | `emilkowalski-skill` | `from-article-18-ui-ux/emilkowalski-skill/` |
| Design rating 0-10 + AI slop detection | `gstack` | `from-article-18-ui-ux/gstack/` |
| UI taste-check | `taste-check` | `from-vault-audit/quality/taste-check/` |
| UI audit | `audit-ui` | `from-vault-audit/quality/audit-ui/` |

### Quality / Localization / Pre-ship

| Задача | Скилл | Путь |
|---|---|---|
| Pre-ship gate | `ship-gate` | `from-vault-audit/quality/ship-gate/` |
| Stop AI slop | `stop-slop` | `from-vault-audit/quality/stop-slop/` |
| Impeccable check | `impeccable` | `from-vault-audit/quality/impeccable/` |
| i18n translation | `i18n-translator` | `from-vault-audit/quality/i18n-translator/` |
| Localization | `localization` | `from-vault-audit/quality/localization/` |
| Test gaps | `test-gaps` | `from-vault-audit/ios-dev/test-gaps/` |

---

## Источники

| # | Источник | Статус | Скиллов |
|---|---|---|---|
| 1 | https://github.com/pearson9/sw-ios-skills | ❌ требует auth (приватный/удалён) | 0 |
| 2 | https://mcpmarket.com/tools/skills/mobile-design-system | ⚠️ JS-rendered, скачать нельзя | 0 (только README) |
| 3 | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | ✅ | 1 |
| 4 | https://pasqualepillitteri.it/.../18-skill-ui-ux | ✅ распарсена | 13 склонировано |
| 5 | https://reddit.com/r/ClaudeCode/.../mobile_apps | ❌ блок-лист → замещено | 15 склонировано (mobile-spec статья того же автора) |
| 6 | Аудит Focus Buddi / Sipper / AppDev | ✅ | 37 + 1 .skill |

**Итого склонировано репо:** 29 + 3 в Android/ (material-3, travisvn-awesome, superpowers) = **32**
**Итого скиллов из vault audit:** 37 (+1 .skill архив)
**Размер `_Mobile-Dev/`:** ~160 MB

### Android-расширение (22 мая 2026)

| # | Источник | Статус | Куда |
|---|---|---|---|
| A1 | `dpconde/claude-android-skill` | ✅ уже было | `from-reddit-mobile-apps/claude-android-skill/` |
| A2 | `hamen/material-3-skill` | ✅ скачан | `Android/from-hamen/` |
| A3 | `mcpmarket/mobile-design-system` | ⚠️ уже README | `from-mobile-design-system/` |
| A4 | `anthropics/skills/frontend-design` | ✅ уже было | `from-article-18-ui-ux/anthropics-skills/` + дубль `_Engineering/frontend-design/` |
| A5 | `Mob-App/obai-marketplace` | ❌ auth required | `Android/from-obai/README.md` |
| A6 | `Mob-App/obai-mcp` | ❌ auth required | `Android/from-obai/README.md` |
| A7 | `pasqualepillitteri.it/.../1807` (RU) | ✅ уже распарсена (EN 1802 = same content) | `from-reddit-mobile-apps/README.md` |
| A8 | `travisvn/awesome-claude-skills` | ✅ скачан | `Android/from-awesome-lists/` |
| A9 | `ComposioHQ/awesome-claude-skills` | ✅ уже было | `from-reddit-mobile-apps/composio-awesome/` |
| A10 | reddit `1s2dacs` | ❌ blocked | — |
| A11 | `obra/superpowers` | ✅ скачан (universal) | `Android/from-superpowers/` |

---

## Дубликаты с остальным vault'ом

Эти скиллы пересекаются с тем, что у тебя уже есть в других категориях. Использовать оригинал из основной категории, в `_Mobile-Dev/` они представлены как часть курируемых сборников от авторов (не дублирующие записи):

| Скилл из _Mobile-Dev | Оригинал в vault |
|---|---|
| anthropics-skills/frontend-design | `_Engineering/frontend-design/` |
| anthropics-skills/theme-factory | `_AI-Automation/theme-factory/` |
| anthropics-skills/skill-creator | `_AI-Automation/skill-creator/` |
| anthropics-skills/canvas-design | `_Product-Apps/canvas-design/` |
| anthropics-skills/figma-to-code | `_Product-Apps/figma/` |
| from-vault-audit/quality/gdpr-dsgvo-expert (NOT copied) | `new-plugins/compliance-regulatory/gdpr-dsgvo-expert` |
| stripe-integration-expert | `_Engineering/stripe-best-practices/` |

---

## Security note (важно)

По данным ToxicSkills от Snyk (упомянуто в статье 18 UI/UX):
- **36%** протестированных Claude-скиллов содержат prompt injection
- В экосистеме найдено **1467 вредоносных пейлоадов**

**Перед использованием любого скилла из этой папки — открой `SKILL.md` и прочитай инструкции.** Особенно для скиллов из неизвестных авторов.

Безопасные источники: Anthropic, Vercel, Google (android/skills), Expo.
