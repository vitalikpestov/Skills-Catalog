# Android — навигатор

> Hub скиллов для **Android-разработки** (Kotlin, Jetpack Compose, Material 3, RN-Android, ASO Google Play).
> Создан 22 мая 2026. Симметричен `_Mobile-Dev/iOS/`.

---

## Структура

```
_Mobile-Dev/Android/
├── _index.md                       ← ты тут
├── from-hamen/
│   └── material-3-skill/           ← Material Design 3 (Compose)
├── from-obai/
│   └── README.md                   ← Mob-App/obai-* — НЕДОСТУПЕН (auth)
├── from-awesome-lists/
│   └── travisvn-awesome-claude-skills/  ← awesome list
└── from-superpowers/
    └── superpowers/                ← obra/superpowers (universal agentic framework)
```

---

## Что лежит в этой папке (новое — из новых источников)

| Скилл | Источник | Тема | Файлы |
|---|---|---|---|
| `material-3-skill` | [hamen](https://github.com/hamen/material-3-skill) | Material Design 3 для Jetpack Compose | 14 |
| `travisvn-awesome-claude-skills` | [travisvn](https://github.com/travisvn/awesome-claude-skills) | Awesome list — индекс по всем скиллам, в т.ч. Android | 3 |
| `superpowers` | [obra/superpowers](https://github.com/obra/superpowers) | Universal agentic framework (Claude+Codex+Cursor+OpenCode) | 146 |
| `obai-marketplace` | — | ❌ недоступен (см. `from-obai/README.md`) | — |
| `obai-mcp` | — | ❌ недоступен | — |

---

## Уже скачано ранее (в `_Mobile-Dev/from-reddit-mobile-apps/`)

**Не дублирую — указываю путь.** Эти Android-скиллы лежат в более ранней папке, потому что попали через mobile-обзор (статья P. Pillitteri):

| Скилл | ⭐ | Где | Назначение |
|---|---|---|---|
| `android-skills` | 4,516 | `../from-reddit-mobile-apps/android-skills/` | **Google Official** — Compose, Navigation 3, AGP 9, R8, edge-to-edge, NowInAndroid |
| `claude-android-skill` | 198 | `../from-reddit-mobile-apps/claude-android-skill/` | dpconde — Compose + MVVM, opinionated |
| `android-skills-mcp` | 178 | `../from-reddit-mobile-apps/android-skills-mcp/` | skydoves — Google skills как MCP server (для offline и multi-agent) |
| `android-reverse-engineering-skill` | 5,440 | `../from-reddit-mobile-apps/android-reverse-engineering-skill/` | APK reverse engineering, smali, hidden endpoints |
| `voltagent-awesome-agent-skills` | 20,009 | `../from-reddit-mobile-apps/voltagent-awesome-agent-skills/` | Awesome list с Android-секцией (1000+ скиллов) |
| `composio-awesome` | — | `../from-reddit-mobile-apps/composio-awesome/` | ComposioHQ awesome list |
| `expo-skills` | 1,837 | `../from-reddit-mobile-apps/expo-skills/` | **React Native + Expo** (включая Android targets) |
| `agent-skills` (Vercel) | 25,800 | `../from-article-18-ui-ux/agent-skills/` | React Native + Android best practices |

---

## Универсальные UI/UX, применимые к Android

Из `from-article-18-ui-ux/`:

| Скилл | Где | Применимо к Android? |
|---|---|---|
| `ui-ux-pro-max-skill` | `../from-ui-ux-pro-max/` | ✅ 67 стилей, явно поддерживает Compose/RN |
| `taste-skill` | `../from-article-18-ui-ux/taste-skill/` | ✅ `imagegen-frontend-mobile` для iOS/Android/RN |
| `designer-skills` | `../from-article-18-ui-ux/designer-skills/` | ✅ Universal UX (research → handoff) |
| `interface-design` | `../from-article-18-ui-ux/interface-design/` | ✅ Cross-platform design system |
| `wondelai-skills/ux-heuristics/` | `../from-article-18-ui-ux/wondelai-skills/` | ✅ Nielsen эвристики — platform-agnostic |

---

## Быстрая навигация по задачам

### Material Design 3 / Compose

| Задача | Скилл | Путь |
|---|---|---|
| Material 3 для Compose | `material-3-skill` | `from-hamen/material-3-skill/` |
| Google official Compose patterns | `android-skills` | `../from-reddit-mobile-apps/android-skills/` |
| Opinionated MVVM | `claude-android-skill` | `../from-reddit-mobile-apps/claude-android-skill/` |

### Архитектура / MVVM / Clean

| Задача | Скилл |
|---|---|
| Clean architecture | `android-skills` (Google) |
| MVVM + Compose | `claude-android-skill` (dpconde) |
| Multi-module | `android-skills` (NowInAndroid patterns) |

### MCP / агентные frameworks

| Задача | Скилл | Путь |
|---|---|---|
| Google skills как MCP server | `android-skills-mcp` | `../from-reddit-mobile-apps/android-skills-mcp/` |
| Universal agentic (Claude+Codex+Cursor) | `superpowers` | `from-superpowers/superpowers/` |
| Поиск Android-скиллов в awesome list | `travisvn-awesome-claude-skills` | `from-awesome-lists/` |
| Mega awesome (20k⭐) | `voltagent-awesome-agent-skills` | `../from-reddit-mobile-apps/` |

### Security / Audit

| Задача | Скилл | Путь |
|---|---|---|
| APK reverse engineering | `android-reverse-engineering-skill` | `../from-reddit-mobile-apps/android-reverse-engineering-skill/` |
| Security audit | `_Engineering/security-reviewer/` | основной vault |

### Cross-platform (React Native, Flutter)

| Задача | Скилл | Путь |
|---|---|---|
| RN + Expo native UI | `expo-skills` | `../from-reddit-mobile-apps/expo-skills/` |
| RN best practices | `agent-skills` (Vercel) | `../from-article-18-ui-ux/agent-skills/` |
| Flutter | — нет dedicated. См. `voltagent-awesome-agent-skills` | — |

---

## Universal — Superpowers (obra)

`from-superpowers/superpowers/` — **не Android-специфичный**, но мощный agentic framework. Помечаю отдельно:

- Поддерживает Claude, Codex, Cursor, OpenCode (см. `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `.opencode/`)
- 146 файлов, 2 MB
- Author: Jesse Vincent (obra) — известный Claude Code разработчик
- README, CLAUDE.md, AGENTS.md, CODE_OF_CONDUCT.md — production-quality

Хорош для:
- Параллельного запуска агентов на Android PR
- Bug-hunting на нескольких уровнях (security, perf, accessibility)
- Workflow automation вне привязки к платформе

Подробности — в `from-superpowers/superpowers/README.md`.

---

## Источники

| # | Источник | Статус | Скиллов |
|---|---|---|---|
| 1 | https://github.com/dpconde/claude-android-skill | ✅ (уже в `from-reddit-mobile-apps/`) | linked |
| 2 | https://github.com/hamen/material-3-skill | ✅ | 1 |
| 3 | https://mcpmarket.com/tools/skills/mobile-design-system | ⚠️ JS-rendered (уже в `from-mobile-design-system/`) | linked |
| 4 | https://github.com/anthropics/skills/tree/main/skills/frontend-design | ✅ (внутри `anthropics-skills/` + дубль в `_Engineering/`) | linked |
| 5 | https://github.com/Mob-App/obai-marketplace | ❌ auth required | 0 |
| 6 | https://github.com/Mob-App/obai-mcp | ❌ auth required | 0 |
| 7 | https://pasqualepillitteri.it/.../1807 (RU) | ✅ распарсена EN-версия (статья 1802) — тот же контент | linked |
| 8 | https://github.com/travisvn/awesome-claude-skills | ✅ | 1 |
| 9 | https://github.com/ComposioHQ/awesome-claude-skills | ✅ (в `from-reddit-mobile-apps/composio-awesome/`) | linked |
| 10 | https://reddit.com/r/ClaudeCode/.../1s2dacs | ❌ blocked (см. предыдущую заметку в `../from-reddit-mobile-apps/README.md`) | 0 |
| 11 | https://github.com/obra/superpowers | ✅ | 1 |

**Итого новых скиллов в этой папке:** 3 (material-3-skill + travisvn-awesome + superpowers)
**Уже доступных Android-скиллов в `_Mobile-Dev/`:** 8 (через `from-reddit-mobile-apps/` и `from-article-18-ui-ux/`)
**Размер `_Mobile-Dev/Android/`:** ~2.5 MB

---

## Security note

`superpowers` и `material-3-skill` от известных авторов (obra, hamen) — относительно безопасны.
`travisvn-awesome-claude-skills` — это README со ссылками; следуй security warning перед установкой любого упомянутого скилла.
`obai-*` — не скачаны, проверка не требуется.

Перед использованием — открой `SKILL.md` / `README.md` каждого скилла.
