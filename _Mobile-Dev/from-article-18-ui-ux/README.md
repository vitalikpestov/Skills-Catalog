# 18 UI/UX скиллов из статьи Pasquale Pillitteri

**Источник:** https://pasqualepillitteri.it/ru/news/888/claude-code-18-luchshikh-skill-dlya-ui-ux-dizayna
**Дата статьи:** 15/04/2026
**Дата скачивания:** 22 мая 2026

---

## TL;DR

Статья описывает 18 design-скиллов для Claude Code + ещё 5 официальных Anthropic. Не все одинаково полезны для **мобильной разработки** — ниже разметка по приоритету для нашего vault'а.

Лëгенда: **MOBILE** = критически важно для iOS/мобильной разработки, **UNIVERSAL** = универсальный UI/UX, **DUPLICATE** = уже есть в твоём vault.

---

## Полный список с приоритетами

| # | Скилл | Stars | GitHub | Приоритет | Статус |
|---|---|---|---|---|---|
| 1 | Anthropic Frontend Design | 118.3k | [anthropics/claude-code](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) | UNIVERSAL | DUPLICATE (`_Engineering/frontend-design`) |
| 2 | UI/UX Pro Max | 71k | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | UNIVERSAL | DUPLICATE (`from-ui-ux-pro-max/`) |
| 3 | Taste Skill | 13.3k | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | MOBILE (есть imagegen-frontend-mobile) | TO CLONE |
| 4 | Interface Design | 4.7k | [Dammyjay93/interface-design](https://github.com/Dammyjay93/interface-design) | UNIVERSAL | TO CLONE |
| 5 | Frontend Design Pro Demo | 212 | [claudekit/frontend-design-pro-demo](https://github.com/claudekit/frontend-design-pro-demo) | UNIVERSAL | TO CLONE |
| 6 | Designer Skills (63 шт.) | 833 | [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) | UNIVERSAL | TO CLONE |
| 7 | Bencium UX | 189 | [bencium/bencium-claude-code-design-skill](https://github.com/bencium/bencium-claude-code-design-skill) | UNIVERSAL | TO CLONE |
| 8 | Vercel Agent Skills | 25.8k | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | **MOBILE** (есть React Native) | TO CLONE |
| 9 | Refactoring UI | 15 | [LovroPodobnik/refactoring-ui-skill](https://github.com/LovroPodobnik/refactoring-ui-skill) | UNIVERSAL | TO CLONE |
| 10 | UX Heuristics | 752 | [wondelai/skills/ux-heuristics](https://github.com/wondelai/skills/tree/main/ux-heuristics) | UNIVERSAL | TO CLONE (один репо) |
| 11 | **iOS HIG Design** | 217 | [rshankras/claude-code-apple-skills](https://github.com/rshankras/claude-code-apple-skills) | **MOBILE — must-have** | TO CLONE |
| 12 | Hooked UX | 752 | [wondelai/skills/hooked-ux](https://github.com/wondelai/skills/tree/main/hooked-ux) | UNIVERSAL | TO CLONE (с wondelai) |
| 13 | Design Sprint | 752 | [wondelai/skills/design-sprint](https://github.com/wondelai/skills/tree/main/design-sprint) | UNIVERSAL | TO CLONE (с wondelai) |

### Бонус: 5 официальных Anthropic Skills

| # | Скилл | GitHub | Статус |
|---|---|---|---|
| 14 | Figma to Code | [anthropics/skills --skill figma](https://github.com/anthropics/skills) | DUPLICATE (`_Product-Apps/figma`) |
| 15 | Theme Factory | [anthropics/skills --skill theme-factory](https://github.com/anthropics/skills) | DUPLICATE (`_AI-Automation/theme-factory`) |
| 16 | Brand Guidelines | [anthropics/skills --skill brand-guidelines](https://github.com/anthropics/skills) | TO CLONE (anthropics/skills целиком) |
| 17 | Canvas Design | [anthropics/skills --skill canvas-design](https://github.com/anthropics/skills) | DUPLICATE (`_Product-Apps/canvas-design`) |
| 18 | Skill Creator | [anthropics/skills --skill skill-creator](https://github.com/anthropics/skills) | DUPLICATE (`_AI-Automation/skill-creator`) |

### Доп. 3 скилла (упомянуты в статье)

| # | Скилл | GitHub | Приоритет |
|---|---|---|---|
| 19 | Emil Kowalski Design (motion) | [emilkowalski/skill](https://github.com/emilkowalski/skill) | UNIVERSAL — анимации |
| 20 | **App Store Screenshots** | [ParthJadhav/app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots) | **MOBILE — must-have** |
| 21 | GStack (design rating 0-10) | [garrytan/gstack](https://github.com/garrytan/gstack) | UNIVERSAL |

### Маркетплейсы (мета)

- [github.com/wondelai/skills](https://github.com/wondelai/skills) — самая большая директория
- [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills) — комьюнити
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) — альтернативный awesome
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — Claude Code awesome
- [Smithery.ai](https://smithery.ai) — маркетплейс с поиском

---

## Что клонируем в этот vault (план)

**Mobile-specific (приоритет 1):**
1. rshankras/claude-code-apple-skills → `iOS-HIG-design/`
2. ParthJadhav/app-store-screenshots → `app-store-screenshots/`
3. vercel-labs/agent-skills → `vercel-agent-skills/` (есть React Native)
4. Leonxlnx/taste-skill → `taste-skill/` (есть imagegen-frontend-mobile)

**UI/UX универсальные (приоритет 2):**
5. Dammyjay93/interface-design
6. claudekit/frontend-design-pro-demo
7. Owl-Listener/designer-skills
8. bencium/bencium-claude-code-design-skill
9. wondelai/skills (содержит ux-heuristics + hooked-ux + design-sprint)
10. LovroPodobnik/refactoring-ui-skill
11. emilkowalski/skill
12. garrytan/gstack

**Дубли пропускаем** (уже есть в vault) — отмечены в таблице выше.

**Anthropic skills (общий репо):**
13. anthropics/skills — клонируем целиком, оттуда нужен `brand-guidelines` (остальное дубли)

---

## Security warning из статьи

> Согласно исследованию ToxicSkills от Snyk, 36% протестированных скиллов содержат prompt injection, и в экосистеме было найдено 1467 вредоносных пейлоадов. **Всегда просматривайте файл SKILL.md** перед установкой скилла из непроверенных источников.

Перед использованием любого скачанного скилла — открой `SKILL.md` и прочитай инструкции, прежде чем активировать.
