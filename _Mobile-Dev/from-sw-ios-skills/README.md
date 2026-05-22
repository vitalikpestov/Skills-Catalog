# sw-ios-skills — НЕДОСТУПЕН

> **Источник:** https://github.com/pearson9/sw-ios-skills
> **Дата проверки:** 22 мая 2026
> **Статус:** ❌ Репозиторий требует авторизацию — приватный, удалён или ошибка в URL

---

## Что было попробовано

1. `git clone https://github.com/pearson9/sw-ios-skills.git` →
   `fatal: could not read Username for 'https://github.com': No such device or address`
2. `WebFetch https://github.com/pearson9/sw-ios-skills` → пустой ответ
3. Поиск автора `pearson9` на GitHub — несколько профилей с этим именем, ни один не публикует репо `sw-ios-skills` публично на дату проверки

## Что делать

**Вариант 1 — спросить владельца:** если ты знаешь автора, попроси сделать репо публичным или получить приглашение.

**Вариант 2 — функциональные замены:** для iOS-разработки в нашем `_Mobile-Dev/` уже есть отличные альтернативы:

| Что мог бы дать `sw-ios-skills` | Замена |
|---|---|
| Swift/SwiftUI patterns | `from-reddit-mobile-apps/Swift-Agent-Skills/` (Paul Hudson, 1.6k⭐) |
| iOS HIG | `from-article-18-ui-ux/claude-code-apple-skills/` |
| iOS 26+ / Liquid Glass | `from-reddit-mobile-apps/vabole-apple-skills/` |
| Полный workflow | `from-reddit-mobile-apps/keskinonur-ios-guide/` |

Папка остаётся пустой как маркер «проверено, недоступно — не качаем снова».

> Если из-за `git clone --depth 1` остался пустой `.git/` каталог — это артефакт mounted folder restriction (не удаляется через `rm -rf`), безопасно игнорируется.
