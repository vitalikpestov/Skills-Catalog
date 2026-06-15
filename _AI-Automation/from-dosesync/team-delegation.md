---
name: team-delegation
description: Use this skill when delegating a task to a team agent (ios-developer, backend-developer, qa-reviewer, marketing specialists). Provides 3 templates (single agent, split task with dependencies, manual prerequisite for user) and ensures inbox format consistency. Trigger when user says "делегируй", "поставь задачу агенту", "раздели работу между", "положи в inbox", or when PM needs to route work to team.
---

# Team Delegation

Шаблоны и чеклист для делегирования работы в команде DoseSync. Обеспечивает консистентный формат задач в inbox-ах агентов, правильную обработку зависимостей, и чёткие ручные чеклисты для пользователя.

## Когда использовать

- PM ставит задачу одному агенту → **Template A: Single agent**
- Задача требует backend + iOS с зависимостями → **Template B: Split task**
- Задача требует ручных действий пользователя (ASC, Vercel, Apple Developer) → **Template C: Manual prerequisite**

## Что всегда делать

1. **Проверить что задача ещё не сделана** — grep в inbox-ах по ключевым словам + git log последние 7 дней
2. **Найти правильный inbox:** `DoseSync/.claude/agents/{category}/inbox-{agent-slug}.md`
3. **Придумать Task ID** — формат `{PREFIX}-{NUMBER}`: `IOS-V12-1`, `BE-05`, `MKT-12`, `QA-FIX4c`
4. **Добавить в секцию "Входящие задачи"** (не в архив)
5. **Использовать "Вы"-форму** в русском тексте задачи
6. **Отчитаться пользователю** какой файл + какой Task ID создан

## Template A: Single agent task

```markdown
- [ ] **{TASK-ID}: {Короткое название}** ({P0/P1/P2}) — {YYYY-MM-DD}
  - **Цель:** что решаем одной строкой
  - **Файлы:**
    - `path/to/file.swift:42-80` — что здесь трогаем
  - **Acceptance criteria:**
    1. Измеримый результат 1
    2. Измеримый результат 2
    3. Тест (если применимо)
  - **Reference:** ссылки на Apple/Supabase docs, audit findings, screenshots
  - **Effort:** оценка в часах
```

**Пример:** iOS task с чёткой спецификой:
```markdown
- [ ] **IOS-POLISH-5: Shimmer на Dose Log loading state** (P2) — 2026-04-18
  - **Цель:** убрать спиннер, показать shimmer-placeholder
  - **Файлы:**
    - `DoseSync/Views/DoseLog/DoseLogView.swift:34-58`
  - **Acceptance criteria:**
    1. В `.loading` state рендерить 3 placeholder rows с shimmer
    2. Переход loading → loaded плавный (fade)
    3. Reduce Motion — убирает shimmer, показывает статичные placeholder
  - **Reference:** DESIGN.md section "Loading states"
  - **Effort:** 45 мин
```

## Template B: Split task (dependencies between agents)

Когда задача требует backend + iOS:

1. Создать задачу для **backend** с `**Blocks:** {iOS-TASK-ID}` внизу
2. Создать задачу для **iOS** с `**Зависит от:** {BE-TASK-ID}` вверху
3. Сказать пользователю: iOS стартует после того, как backend endpoint задеплоен в staging

**Пример:** BE-03 → IOS-PROMO-1 (Promotional Offers, из текущего спринта)

Backend inbox:
```markdown
- [ ] **BE-03: Edge Function `sign-promotional-offer`** (P1) — 2026-04-18
  - **Цель:** server signing для StoreKit Promotional Offers
  - **Prerequisites (ручные):** см. задачу ASC-03 для Vitalik
  - **Acceptance criteria:** ...
  - **Effort:** 2-3ч
  - **Blocks:** IOS-PROMO-1
```

iOS inbox:
```markdown
- [ ] **IOS-PROMO-1: Интеграция Promotional Offers в Drip Funnel** (P1) — 2026-04-18
  - **Зависит от:** BE-03 (Edge Function `sign-promotional-offer`)
  - **Цель:** показывать "50% off" badge на paywall + применять оффер при покупке
  - **Файлы:** StoreKitService, DripFunnelService, PaywallPlansScreen
  - **Acceptance criteria:** ...
  - **Effort:** 2-3ч после того как BE-03 задеплоен
```

## Template C: Manual prerequisite (ручные задачи пользователя)

Для вещей требующих доступа к Apple Developer Portal, App Store Connect, Vercel, Supabase dashboard.

**Формат:** отдельный блок в конце обычной задачи + чеклист пользователю в ответе.

```markdown
**Prerequisites (ручные задачи Vitalik в {ASC/Apple Developer/Vercel}):**
1. {Шаг с точным местом в UI}
2. {Что скопировать/скачать}
3. {Куда положить (Supabase secrets / .env / ASC field)}
```

**Пример:** из BE-03 prerequisites:
```markdown
**Prerequisites (ручные задачи Vitalik в ASC):**
1. ASC → Users and Access → Keys → In-App Purchase → Generate Subscription Key
2. Скачать `.p8` file, сохранить Key ID + Issuer ID
3. Положить в Supabase secrets: `APP_STORE_PROMO_KEY_P8` (base64), `APP_STORE_PROMO_KEY_ID`, `APP_STORE_ISSUER_ID`
4. В ASC на каждом продукте создать Promotional Offer (код "50OFF_FIRST_MONTH")
```

**В ответе пользователю** — повторить как чеклист-таблицу:

| # | Задача | Где | Что делать |
|---|--------|-----|------------|
| 1 | Generate Subscription Key | ASC → Users and Access → Keys | In-App Purchase → Generate |
| 2 | Скачать .p8 + Key ID + Issuer ID | Сохрани в password manager | Один раз, потом недоступен |
| 3 | Supabase secrets | dashboard → Project → Secrets | 3 ключа |

## Agent inbox locations

| Category | Agents |
|----------|--------|
| `dev/` | ios-developer, backend-developer, qa-reviewer, web-developer, android-developer |
| `legal/` | compliance, lawyer |
| `product/` | cpo, bizanal, findir, researcher, vcr |
| `marketing/` | director, content-creator, growth-hacker, seo-specialist, social-media-strategist, tiktok-strategist, instagram-curator, twitter-engager, linkedin-content-creator, reddit-community-builder, podcast-strategist, app-store-optimizer, video-optimization-specialist, short-video-editing-coach, ai-citation-strategist, carousel-growth-engine |
| `design/` | ui-ux-designer |
| `support/` | support |

Путь: `DoseSync/.claude/agents/{category}/inbox-{agent-slug}.md`

## Task ID convention

| Prefix | Agent | Example |
|--------|-------|---------|
| `IOS-*` | ios-developer | `IOS-POLISH-5`, `IOS-PROMO-1`, `IOS-SEC-003` |
| `BE-*` | backend-developer | `BE-03`, `BE-SEC1` |
| `QA-*` | qa-reviewer | `QA-FIX4c`, `QA-OB12` |
| `CP-*` | compliance | `CP-03` |
| `PM-*` | cpo | `PM-01` |
| `VC-*` | vcr | `VC-02` |
| `MKT-*`, `SEO-*`, `CAR-*`, `POD-*`, `VID-*`, `EDIT-*`, `SM-*`, `AEO-*` | marketing agents | — |

## Priority convention

- **P0** — блокер TestFlight / production launch / security critical
- **P1** — важно, но не блокирует релиз
- **P2** — nice to have, backlog

## Self-check перед тем как сказать "готово"

- [ ] Task ID уникален (нет дубликата в inbox)
- [ ] Приоритет выставлен (P0/P1/P2)
- [ ] Acceptance criteria измеримые
- [ ] Effort указан
- [ ] Если есть prerequisite — пользователю дан чеклист в ответе
- [ ] Если есть зависимость от другого агента — оба файла обновлены
- [ ] "Вы"-форма в русском тексте
