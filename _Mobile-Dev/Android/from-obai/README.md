# Mob-App/obai-* — НЕДОСТУПЕН

> **Источники:**
> - https://github.com/Mob-App/obai-marketplace
> - https://github.com/Mob-App/obai-mcp
>
> **Дата проверки:** 22 мая 2026
> **Статус:** ❌ Оба репо требуют авторизацию

---

## Что было попробовано

1. `git clone https://github.com/Mob-App/obai-marketplace.git` → `fatal: could not read Username for 'https://github.com'`
2. `git clone https://github.com/Mob-App/obai-mcp.git` → то же самое
3. `WebFetch` обоих URL → пустой ответ (404 или приватные)
4. `WebSearch "obai-marketplace OR obai-mcp Mob-App github claude"` → не найдено упоминаний

## Возможные причины

- Репо приватные (требуют доступа от Mob-App)
- Репо удалены или переименованы
- Источник (Reddit) содержал ошибочные URL — Reddit-тред заблокирован, проверить точное имя невозможно
- Mob-App организация может скрывать свои репо до релиза

## Что делать

**Если у тебя есть доступ:**
1. Авторизуйся через `gh auth login` или `git config --global credential.helper`
2. Повтори `git clone` сюда вручную

**Если нет доступа — функциональные альтернативы для Android:**

| Что мог бы дать `obai-marketplace` (Android plugin marketplace) | Замена |
|---|---|
| Marketplace плагинов | `_Mobile-Dev/Android/from-awesome-lists/travisvn-awesome-claude-skills/` |
| Курируемая коллекция | `_Mobile-Dev/from-reddit-mobile-apps/voltagent-awesome-agent-skills/` (20k⭐) |
| Anthropic official | `_Mobile-Dev/from-article-18-ui-ux/anthropics-skills/` |

| Что мог бы дать `obai-mcp` (Android MCP server) | Замена |
|---|---|
| Google skills как MCP | `_Mobile-Dev/from-reddit-mobile-apps/android-skills-mcp/` (skydoves/178⭐) |
| Generic mobile MCP | См. `_AI-Automation/mcp-builder/` для написания своего |

Папка остаётся пустой как маркер «проверено, недоступно — не качаем снова».
