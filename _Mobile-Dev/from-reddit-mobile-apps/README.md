# Mobile Development Claude Skills

> **Reddit-тред заблокирован в WebFetch (`reddit.com` в блок-листе).**
> Вместо него использован более качественный источник того же тренда:
> **"Best Claude Skills for Mobile Development: 2026 Guide"** — Pasquale Pillitteri, 03/05/2026
> https://pasqualepillitteri.it/en/news/1802/best-claude-skills-mobile-development-2026

Это **mobile-специализированная** статья (англ. версия): фокус только на iOS / Android / React Native / ASO. Stars верифицированы на 03 мая 2026.

---

## Beto Moedano's 5 mobile skills

Beto Moedano (бывший Developer Success Engineer at Expo, создатель Inkigo — meditative drawing app, $650/мес на App Store).

| # | Скилл | GitHub | Stars | Назначение |
|---|---|---|---|---|
| 1 | **ASO Audit** | [Eronred/aso-skills](https://github.com/Eronred/aso-skills) | 1,159 | App Store listing audit + keyword analysis |
| 2 | **Apple Search Ads** | [Eronred/aso-skills](https://github.com/Eronred/aso-skills) | (same repo) | ASA campaign setup, keyword research with bids |
| 3 | **App Store Preflight** | [truongduy2611/app-store-preflight-skills](https://github.com/truongduy2611/app-store-preflight-skills) | 1,133 | Pre-submit scan: privacy manifests, entitlements, IAP |
| 4 | **App Icon** (uses SnapAI) | [Code-with-Beto/skills](https://github.com/Code-with-Beto/skills) | 77 | Generates iOS 18, iOS 26, Android icons via OpenAI |
| 4a | **SnapAI CLI** (dependency) | [betomoedano/snapai](https://github.com/betomoedano/snapai) | 1,801 | Open-source CLI for AI icon generation |
| 5 | **Expo Build Native UI** | [expo/skills](https://github.com/expo/skills) | 1,837 | +46% native UI adherence (Expo internal benchmark) |

## 6 mobile skills Beto не упоминает

| # | Скилл | GitHub | Stars | Назначение |
|---|---|---|---|---|
| 6 | **VoltAgent Awesome Agent Skills** | [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 20,009 | Курируемый сборник 1000+ скиллов с `npx skills add` |
| 7 | **Google Official Android Skills** | [android/skills](https://github.com/android/skills) | 4,516 | Compose, Navigation 3, AGP 9, R8, edge-to-edge, NowInAndroid patterns |
| 8 | **Android Reverse Engineering** | [SimoneAvogadro/android-reverse-engineering-skill](https://github.com/SimoneAvogadro/android-reverse-engineering-skill) | 5,440 | APK decompile, smali, hidden endpoints — security audits |
| 9 | **Claude Android Skill** | [dpconde/claude-android-skill](https://github.com/dpconde/claude-android-skill) | 198 | Production-ready Compose + MVVM (opinionated) |
| 10 | **Android Skills MCP** | [skydoves/android-skills-mcp](https://github.com/skydoves/android-skills-mcp) | 178 | Google's `android/skills` packaged as MCP server for offline/multi-agent |
| 11 | **Paul Hudson's Swift Agent Skills** | [twostraws/Swift-Agent-Skills](https://github.com/twostraws/Swift-Agent-Skills) | 1,588 | Swift, SwiftUI, SwiftData — от автора Hacking with Swift |

## Дополнительно из WebSearch

| # | Скилл | GitHub | Назначение |
|---|---|---|---|
| 12 | **Patrick Serrano iOS Skills** | [patrickserrano/skills](https://github.com/patrickserrano/skills) | iOS, Swift, SwiftUI collection |
| 13 | **vabole Apple Skills** | [vabole/apple-skills](https://github.com/vabole/apple-skills) | iOS 26+, SwiftUI, Liquid Glass |
| 14 | **Claude Code iOS Dev Guide** | [keskinonur/claude-code-ios-dev-guide](https://github.com/keskinonur/claude-code-ios-dev-guide) | PRD workflows, ultrathink for SwiftUI |
| 15 | **Composio Awesome Claude Skills** | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Awesome list |

---

## Матрица выбора скилла по стеку (от автора статьи)

| Stack | Need | Recommended skill |
|---|---|---|
| React Native + Expo | Build native UI | `expo/skills` (1,837) |
| Native Android | Compose + AGP 9 | `android/skills` (4,516) |
| Native iOS | SwiftUI/SwiftData | `Swift-Agent-Skills` (1,588) |
| Any | App already published, ASO audit | `aso-skills` (1,159) |
| iOS/macOS | Pre-submit check | `preflight` (1,133) |
| Everything | Generate app icon | `SnapAI` (1,801) |
| Everything | Explore the ecosystem | `awesome-agent-skills` (20,009) |
| Security/Audit | Reverse APK | `android-reverse-engineering` (5,440) |

**Rule of thumb:** start with the official skill for your stack (Expo, Android, Swift) + add `aso-skills` and `preflight` at release time.

---

## Что клонировано в эту папку

См. отдельные подпапки. Все клонированы без `.git/` (где возможно).
