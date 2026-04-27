# DoseSync — Контекст для Claude Code
## Handoff-документ от сессии Cowork, 7–8 апреля 2026

---

## КТО Я И ЧЕМ ЗАНИМАЮСЬ

Меня зовут Виталий. Я Business Development Manager & Partnership Lead в Web3. Помогаю фаундерам Web3-стартапов внедрять AI в revenue generation pipeline и BD-отделы.

Параллельно — строю собственный iOS-продукт **DoseSync**.

---

## ЧТО ТАКОЕ DOSESYNC

**DoseSync** — iOS-приложение для координации приёма лекарств между несколькими опекунами (семья, медсестра, няня). Не трекер здоровья — координатор опекунов. Один источник правды для всей семьи.

**Корневая боль:** когда несколько людей дают лекарства одному человеку — никто не знает наверняка, была ли доза уже дана. Результат: тревога, постоянные звонки, записки на холодильнике, риск двойной дозы.

**Откуда идея:** реальный тред на Reddit r/caregivers, опубликованный u/azamat_valitov:
https://www.reddit.com/r/caregivers/comments/1pqguaa/what_systems_actually_prevent_doubledosing_when/

**Личный контекст (для постов):** у меня есть бабушка (79 лет, 11 таблеток в день). За ней смотрят мама, её сестра и я. Наша «система» — записки на холодильнике, WhatsApp и звонки. Я сам бросаю курс антибиотиков, когда становится лучше. Делаю приложение для себя.

---

## ТЕХНИЧЕСКИЙ СТЕК V1.0

- **Platform:** iOS 17.0+, iPhone only
- **UI:** SwiftUI + MVVM + @Observable
- **Local storage:** SwiftData (offline-first, needsSync flag)
- **Backend:** Supabase (PostgreSQL + RLS)
- **Realtime:** Supabase Realtime (RealtimeChannelV2)
- **Auth:** Sign in with Apple + Magic Link (Email)
- **Payments:** StoreKit 2
- **Push:** APNs + Supabase Edge Functions
- **Guest access:** Supabase Edge Functions + временный токен 1–72ч
- **Localisation:** EN + RU + ES

---

## ФИЧИ V1.0 (ВСЁ УЖЕ В КОДЕ, задача — довести до production quality к 10 июня 2026)

1. Sign in with Apple + Magic Link
2. Онбординг 4–5 шагов (сценарий / реферальный код / paywall / trial reminder / thank you)
3. Создание семейного пространства
4. Приглашение по ссылке и QR-коду
5. Список участников с ролями
6. Добавление подопечных (имя, фото, заметки)
7. CRUD лекарств
8. Все 3 типа расписания (фиксированное / каждые N часов / по необходимости)
9. Today-дашборд: список доз по статусам
10. Подтверждение дозы (свайп + тап + из push)
11. Пропуск дозы
12. Защита от двойной дозы (клиент + server RLS)
13. Real-time синхронизация (все опекуны видят одновременно)
14. Push с actionable кнопками «Дала / Пропустить»
15. Badge на иконке = количество pending доз
16. Бабушкин режим (2 вкладки, крупный шрифт)
17. Гостевой доступ — режим няни (токен 1–72ч, без аккаунта)
18. Offline-first (SwiftData + needsSync + автосинхронизация)
19. StoreKit 2: Solo + Family планы
20. Paywall с 7-дневным триалом
21. Фото лекарств (Family план)
22. Экспорт истории в PDF (Family план)
23. Стрики (StreakService)
24. App Review prompt (после 10-й дозы / 7-дневной серии)
25. Локализация EN + RU + ES

**⚠️ ВАЖНО:** NFC-приглашения есть в коде (v1.0 roadmap), но в постах и маркетинге НЕ упоминать — не подтверждено как production-ready фича v1.0.

---

## REDDIT-СТРАТЕГИЯ — ЧТО МЫ ПОСТРОИЛИ

### Файлы (в папке "Prompt Engineer"):

| Файл | Содержимое |
|------|-----------|
| `DoseSync_Reddit_Tracker.xlsx` | 41 саб в 5 тирах, ссылки, стратегия, статусы, фазы |
| `DoseSync_Reddit_Content.md` | 5 готовых постов + 8 шаблонов комментариев + план 5 фаз |

---

### АККАУНТЫ

**Купить на redaccs.com — Comment Karma Accounts:**
- 2 аккаунта × $41 = **$82**
- Тип: 3 года, Post Karma ~1, Comment Karma 197–277
- ⚠️ Перед покупкой: проверить username на reddit.com/u/[name] — нужна нейтральная или health/family история, не аниме/геймерские

| Аккаунт | Персона | Тиры | Примеры имён |
|---------|---------|------|--------------|
| **A — "Человек"** | Тёплый, личный, семейный | Tier 1–2–5 | `caring_for_gran`, `just_vitalik`, `vit_family` |
| **B — "Строитель"** | Founder, аналитический | Tier 3–4 | `vitalik_builds`, `vp_founder`, `vitalik_dev` |

⚠️ Никогда в username: dose / sync / med / pill / health / care

---

### 41 САБРОЕДДИТ ПО ТИРАМ

**Tier 1 — Caregivers (прямая ЦА):**
r/caregivers, r/CaregiverSupport, r/AgingParents, r/dementia, r/Alzheimers

**Tier 2 — Родители:**
r/Parenting, r/Mommit, r/daddit, r/SandwichGeneration, r/coparenting, r/SpecialNeedsParents

**Tier 3 — Здоровье / Self-trackers:**
r/ChronicIllness, r/ADHD, r/diabetes, r/Epilepsy, r/Biohackers, r/Nootropics, r/Peptides, r/Supplements, r/longevity

**Tier 4 — Tech & Builders:**
r/SideProject, r/indiehackers, r/startups, r/AlphaandBetausers, r/InternetIsBeautiful, r/EntrepreneurRideAlong, r/MadeThis, r/RoastMyStartup, r/productivity, r/getdisciplined, r/nursing, r/HomeHealthAide, r/iOSProgramming, r/apple, r/ios, r/iPhone

**Tier 5 — Pets:**
r/dogs, r/cats, r/seniordogs, r/Pets, r/AskVet

---

### ПОШАГОВЫЙ ПЛАН (5 фаз, 9 недель до релиза)

**ФАЗА 0 — Сейчас (эта неделя):**
- Купить 2 аккаунта на redaccs.com
- Настроить F5Bot (бесплатно): алерты на "medication tracker", "double dose", "caregiver app", "forgot meds", "coordinating medications"
- Заполнить профили (без упоминания DoseSync)

**ФАЗА 1 — Прогрев (7–20 апреля):**
- Только комментарии, DoseSync не упоминается
- 3–4 комментария/день на каждый аккаунт
- Цель: 50+ karma каждый

**ФАЗА 2 — Первый пост (21–27 апреля):**
- Аккаунт A: прогревочный пост в r/caregivers (без ссылки на App Store)
- Тема: "My grandmother takes 11 pills a day. Three of us manage her schedule..."

**ФАЗА 3 — Расширение (28 апр – 11 мая):**
- r/Parenting, r/SideProject, r/coparenting
- Формат D: полезный контент без продукта

**ФАЗА 4 — Релиз (10 июня):**
- 5 постов в день релиза с разбивкой по времени
- r/caregivers (9:00), r/Parenting (10:00), r/SideProject (11:00), r/AlphaandBetausers (13:00), r/iOSProgramming (15:00)

**ФАЗА 5 — После релиза:**
- r/InternetIsBeautiful, r/ADHD, r/Biohackers, r/EntrepreneurRideAlong (еженедельно), pet subs

---

### ГОТОВЫЕ ПОСТЫ (5 штук, в Content.md файле)

1. **Прогревочный** (r/caregivers) — без App Store ссылки. Бабушка, 11 таблеток, три опекуна, боль координации + личная история с антибиотиками. Оканчивается тремя острыми вопросами к комьюнити.

2. **Лонч-пост** (r/caregivers) — со ссылкой. Нашёл тред u/azamat_valitov → примерил на себя → построил DoseSync.

3. **r/Parenting** — "Did you give the Tylenol?" история про 2am.

4. **r/getdisciplined** — разбор систем (бумажный лог / Google Sheet / WhatsApp / таблетница) — где каждая ломается.

5. **r/SideProject** — builder story, технический стек, фидбек.

### КЛЮЧЕВАЯ ФРАЗА ДЛЯ ВСЕХ ПОСТОВ
**"Shared certainty"** — переформулирует DoseSync из "reminder app" в новую категорию.

---

### ШАБЛОНЫ КОММЕНТАРИЕВ (8 штук, в Content.md файле)

КОМ-1: Ответ на вопросы про координацию (r/caregivers, r/AgingParents)
КОМ-2: Ответ на страх двойной дозы (r/Parenting, r/daddit)
КОМ-3: Ответ про незаконченные курсы лечения (r/getdisciplined)
КОМ-4: Ответ про пожилых родителей (r/AgingParents, r/dementia)
КОМ-5: Ответ в r/Biohackers про логирование стека
КОМ-6: Ответ в r/ADHD про забывчивость
КОМ-7: Ответ в r/coparenting про координацию между домами
КОМ-8: Ответ в r/nursing про home care gap

---

### МОНИТОРИНГ
- **F5Bot** (бесплатно): https://f5bot.com — email-алерты по ключевым словам
- **GummySearch** ($79/мес, первый месяц): анализ language аудитории

---

## KPI

| Метрика | Цель к релизу (нед. 6) | Цель к нед. 10 |
|---------|----------------------|----------------|
| Karma Аккаунт A | 150+ | 500+ |
| Karma Аккаунт B | 100+ | 300+ |
| Написано комментариев | 80+ | 200+ |
| Опубликовано постов | 5 | 15+ |
| Downloads с Reddit | 200+ | 1000+ |

---

## ПРЕДПОЧТЕНИЯ ПО РАБОТЕ

- Общение на русском
- Формат: сжатый + структурированный для планов, развёрнутый для контента
- Перед действием: задавать вопросы и составлять план
- Критиковать идеи аргументированно
- В постах для Reddit: никогда не упоминать фичи, которых нет в v1.0
- Эмодзи — в чате ок, в LinkedIn-контенте — никогда
- Вывод по умолчанию: чистый текст для копипасты

---

*Создан: 8 апреля 2026*
*Источник: сессия Cowork с Виталием*
