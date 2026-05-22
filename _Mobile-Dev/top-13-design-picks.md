# Top-13 Design Skills — Quick Picks

> Курируемая выборка из ~70 design/UX скиллов в `_Mobile-Dev/`.
> Это «ready-to-use» навигатор для быстрого старта вместо листания всего каталога.
>
> Создан 22 мая 2026. Полный каталог: [`mobile-skills-catalog.md`](mobile-skills-catalog.md).

---

## Когда что брать (decision matrix)

| Хочу | Бери |
|---|---|
| Начать с одного «universal» скилла | **#13 Anthropic frontend-design** (официальный, 118k⭐) |
| Максимум стилей / автоматический design system | **#10 UI/UX Pro Max** (67 стилей, 71k⭐) |
| Тонкий контроль через параметры | **#9 Taste Skill** (3 равалайзера: variance/motion/density) |
| Исследовать 11 разных эстетик подряд | **#7 ClaudeKit 11 эстетик** |
| Дизайн-система, которая «помнит» решения между сессиями | **#12 Interface Design** (Dammyjay93) |
| Полный процесс от research до handoff | **#11 Designer Skills** (63 скилла, end-to-end) |
| Запустить 5-дневный design sprint в чате | **#1 Wondelai Design Sprint** |
| Проверить retention через Hook Model | **#2 Wondelai Hooked UX** |
| Audit по 10 эвристикам Нильсена | **#3 Wondelai UX Heuristics** |
| WCAG 2.2 + два разных подхода (innovative/controlled) | **#8 Bencium** |
| Аудит существующего UI (визуальная иерархия, spacing, теней) | **#5 Refactoring UI** |
| Performance + accessibility + React best practices (для RN) | **#6 Vercel agent-skills** (25.8k⭐) |
| Нативный iOS 26+ / Liquid Glass / HIG | **#4 rshankras Apple Skills** |

---

## Подробно

### 1. Design Sprint (Wondelai)

5-дневный Google Ventures Design Sprint в одном скилле: understand → sketch → decide → prototype → test.

- **Активация:** `"run a design sprint"`, `"ideation workshop"`, `"validate this idea"`
- **Путь:** `from-article-18-ui-ux/wondelai-skills/design-sprint/`
- **⭐:** 752 (родительский wondelai/skills)

### 2. Hooked UX (Wondelai)

Hook Model Нира Эяля: trigger / action / reward / investment. Диагностирует где цикл удержания прерывается.

- **Активация:** `"users aren't coming back"`, `"improve retention"`, `"habit loop"`, `"engagement"`
- **Путь:** `from-article-18-ui-ux/wondelai-skills/hooked-ux/`
- **⭐:** 752

### 3. UX Heuristics (Wondelai)

10 эвристик Нильсена автоматически + принципы «Don't Make Me Think» Стива Круга. Severity scoring для каждой проблемы.

- **Активация:** `"audit this for usability"`, `"heuristic review"`, `"UX issues"`
- **Путь:** `from-article-18-ui-ux/wondelai-skills/ux-heuristics/`
- **⭐:** 752

### 4. Apple Skills / Liquid Glass iOS (rshankras)

HIG: Safe Areas, Dynamic Island, Tab Bars, Modals, Dark Mode (semantic colors), Dynamic Type, VoiceOver. Всё с первого раза.

- **Активация:** `"iOS app"`, `"iPhone interface"`, `"SwiftUI design"`, `"HIG compliance"`
- **Путь:** `from-article-18-ui-ux/claude-code-apple-skills/`
- **⭐:** 217
- **Bonus:** для iOS 26+ Liquid Glass смотри также `from-reddit-mobile-apps/vabole-apple-skills/skills/ios-liquid-glass/`

### 5. Refactoring UI

Применяет систему Refactoring UI (Adam Wathan + Steve Schoger). Аудит визуальной иерархии, отступов, теней, цветов.

- **Активация:** `"my UI looks off"`, `"fix the design"`, `"visual hierarchy"`, `"color palette"`
- **Путь:** `from-article-18-ui-ux/refactoring-ui-skill/`
- **⭐:** 15 (LovroPodobnik) + дубль в `wondelai-skills/refactoring-ui/`

### 6. Vercel agent-skills (100+ правил веба)

Web Design Guidelines: 100+ правил доступности, производительности, UX. React Best Practices: 57 правил в 8 категориях. Composition Patterns. React Native skills.

- **Когда:** дополнение к визуальному скиллу. Vercel занимается **техническим качеством**, другой скилл — стилем.
- **Путь:** `from-article-18-ui-ux/agent-skills/skills/`
- **⭐:** 25,800

### 7. Frontend Design Pro Demo (ClaudeKit, 11 эстетик)

11 совершенно разных стилей с мастер-промптами и production-ready кодом: Swiss Minimalism, Neumorphism, Glassmorphism, Brutalism, Claymorphism, Aurora/Mesh Gradient, Retro-Futurism/Cyberpunk, 3D Hyperrealism, Vibrant Block/Maximalist, Dark OLED Luxury, Organic/Biomorphic.

- **Live demo:** https://claudekit.github.io/frontend-design-pro-demo/
- **Путь:** `from-article-18-ui-ux/frontend-design-pro-demo/`
- **⭐:** 212

### 8. Bencium UX (WCAG из коробки)

28k+ chars UX reference. **Два варианта** в одном пакете:
- **Innovative UX Designer** — смелые творческие выборы, эксперименты
- **Controlled UX Designer** — согласованность, контроль, стандарты

Документы: ACCESSIBILITY.md (WCAG 2.1/2.2), RESPONSIVE-DESIGN.md, MOTION-SPEC.md, DESIGN-SYSTEM-TEMPLATE.md.

- **Путь:** `from-article-18-ui-ux/bencium-claude-code-design-skill/`
- **Содержит:** bencium-impact-designer, bencium-aeo, bencium-innovative-ux-designer, bencium-controlled-ux-designer, bencium-code-conventions, adaptive-communication, design-audit, human-architect-mindset, negentropy-lens, organic-first-campaign, relationship-design, renaissance-architecture, typography, vanity-engineering-review
- **⭐:** 189
- **Эквивалент:** `bencium/bencium-marketplace` (тот же контент)

### 9. Taste Skill (Leonxlnx, эквалайзер вкуса)

Не один скилл — **набор из 9 specialized variants + 3 imagegen**. Система **3 регулируемых параметров** как аудио-эквалайзер:

- `DESIGN_VARIANCE` (1-10) — clean centered ↔ asymmetric modern
- `MOTION_INTENSITY` (1-10) — simple hover ↔ magnetic scroll-triggered
- `VISUAL_DENSITY` (1-10) — luxury airy ↔ compact dashboard

**Варианты:** taste-skill, gpt-taste, image-to-code-skill, redesign-skill, soft-skill, minimalist-skill, brutalist-skill, stitch-skill, output-skill.
**Imagegen:** imagegen-frontend-web, **imagegen-frontend-mobile** (iOS/Android mockup), brandkit.

- **Путь:** `from-article-18-ui-ux/taste-skill/`
- **⭐:** 13,300
- **Совместимость:** Claude Code, Cursor, Codex, Windsurf, Antigravity, Copilot
- **Site:** tasteskill.dev

### 10. UI/UX Pro Max (NextLevelBuilder, 67 стилей)

**Самый популярный community скилл** (71k⭐). Design System Generator: говоришь «fintech dashboard» → автоматически выбирает стиль, цвета, типографику.

- **67 UI стилей**: Glassmorphism, Claymorphism, Brutalism, Neumorphism, Swiss Design...
- **161 цветовая палитра** под индустрии
- **57 комбинаций шрифтов** с готовыми импортами Google Fonts
- **161 правило рассуждений** специфичных для индустрии
- **99 UX-гайдлайнов**

- **Путь:** `from-ui-ux-pro-max/ui-ux-pro-max-skill/`
- **Platforms:** React, Next.js, Vue, Nuxt, Svelte, **Flutter**, **SwiftUI**, **React Native** и др.

### 11. Designer Skills (Owl-Listener, end-to-end)

**63 скилла + 27 команд** в 8 плагинах. Покрывает весь дизайн-цикл от исследования до handoff:

| Плагин | Скиллов | Назначение |
|---|---|---|
| `design-research` | 10 | Persona, empathy map, journey map (`/discover`) |
| `design-systems` | 8 | Создание и управление дизайн-системами |
| `ux-strategy` | 8 | UX-стратегия (`/strategize`) |
| `ui-design` | 9 | UI-компоненты, accessible color palettes (`/color-palette`) |
| `interaction-design` | 7 | Паттерны взаимодействия, микроинтеракции |
| `prototyping-testing` | 8 | Прототипирование, usability testing |
| `design-ops` | 7 | Design workflow и процессы |
| `designer-toolkit` | 6 | Daily utilities, handoff (`/handoff`) |

- **Путь:** `from-article-18-ui-ux/designer-skills/`
- **⭐:** 833

### 12. Interface Design (Dammyjay93, память дизайна)

Решает проблему которую другие игнорируют: **согласованность между сессиями**. Сохраняет дизайн-решения в `.interface-design/system.md` — никакого стилистического дрейфа.

- **Predefined directions:** «Precision & Density», «Warmth & Approachability» и др.
- **Auto-enforcement:** Claude объявляет дизайн-решения перед каждым компонентом
- **Путь:** `from-article-18-ui-ux/interface-design/`
- **⭐:** 4,700

### 13. Anthropic Frontend Design (конец AI-шаблонов)

**Официальный** скилл от Anthropic, 118.3k⭐ — обязательная база. Работает как творческий бриф от арт-директора:

- **Смелая типографика** — явно запрещает Inter, Roboto, Arial, Space Grotesk («overused by AI»)
- **Цветовые палитры с CSS-переменными** — больше никаких generic фиолетовых градиентов
- **Асимметричные макеты** — ломает стандартную сетку
- **Намеренные анимации** — motion только там где имеет воздействие

- **Путь (2 копии):**
  - `_Engineering/frontend-design/` — отдельная копия в основном vault
  - `_Mobile-Dev/from-article-18-ui-ux/anthropics-skills/skills/frontend-design/` — в составе anthropics/skills

- **Установка из upstream:** `claude plugin add anthropic/frontend-design`

---

## Рекомендованные сочетания

| Сценарий | Стек |
|---|---|
| **iOS app с нуля** | #13 frontend-design + #4 Apple Skills + #6 Vercel (для тех. качества) |
| **Лендинг с уникальным стилем** | #10 UI/UX Pro Max или #7 ClaudeKit (выбрать эстетику) + #5 Refactoring UI (полировка) |
| **SaaS дашборд** | #13 frontend-design + #12 Interface Design (согласованность) + #6 Vercel |
| **Релиз нового продукта (валидация → дизайн → код)** | #1 Design Sprint → #11 Designer Skills → #10 UI/UX Pro Max |
| **Mature app — улучшаем retention** | #3 UX Heuristics (аудит) → #2 Hooked UX (диагноз) → #11 Designer Skills (фикс) |
| **Compliance проект (a11y, гос. сектор)** | #8 Bencium Controlled + #6 Vercel Web Design Guidelines |
| **Эксперимент, нужен полный контроль** | #9 Taste Skill (параметрический) + #12 Interface Design (память между sessions) |

---

## Чего НЕ покрывает этот pick

- **ASO / App Store** → см. отдельную секцию в `mobile-skills-catalog.md`
- **Mobile monetization (paywall, subscription)** → `from-vault-audit/product-monetization/`
- **Mobile attribution / UA / Apple Search Ads** → `from-vault-audit/marketing-mobile/`
- **Native Android (Material 3, Compose, Play Billing)** → `Android/_index.md`
- **Motion / микроинтеракции (premium polish)** → `from-article-18-ui-ux/emilkowalski-skill/`
- **Design rating 0-10 + AI Slop Detection** → `from-article-18-ui-ux/gstack/` (от CEO Y Combinator)

---

## Security note

По данным Snyk ToxicSkills: 36% Claude-скиллов содержат prompt injection. Перед использованием — открой `SKILL.md` и прочитай инструкции.

**High-trust в этом списке:** #6 Vercel (25.8k⭐), #13 Anthropic frontend-design (118.3k⭐), #10 UI/UX Pro Max (71k⭐).
