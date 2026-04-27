# DoseSync — Reddit Content Bank

**Стратегия:** Comment-first → Story posts → Launch post
**Правило:** 9 полезных комментариев на 1 упоминание продукта
**Тайминг постов:** Вт/Ср/Чт, 9–11am EST
**Аккаунты:** 2 штуки × $41 = $82 (Comment Karma, 3 года, 200–277 karma)

| Аккаунт | Фокус | Тир | Нейминг |
|---------|-------|-----|---------|
| **A — "Человек"** | Caregiving, parents, pets | Tier 1–2–5 | Нейтральное имя: `caring_for_gran`, `vit_family`, `just_vitalik` |
| **B — "Строитель"** | Tech, indie, biohackers | Tier 3–4 | Founder-style: `vitalik_builds`, `vp_founder`, `vitalik_dev` |

⚠️ Никогда не использовать в username: dose, sync, med, pill, health, care

---

## ПОСТЫ

---

### ПОСТ 1 — Прогревочный (без ссылки на приложение)
**Саб:** r/caregivers
**Статус:** ✅ Готов
**Цель:** Сбор инсайтов от комьюнити, узнаваемость, прогрев перед лончем

**Title:** My grandmother takes 11 pills a day. Three of us manage her schedule. None of us are ever fully sure. So I started building something.

---

My grandmother is 79. She takes 11 pills a day — different ones at different times, some with food, some without, some that can't be taken together.

Three of us manage her schedule: my mom, her sister, and me. We all live nearby. We all try to stay on top of it.

Here's what our "system" actually looks like:

Notes on the fridge. WhatsApp messages that get buried under everything else. Phone calls that start with "hey, did she already take the evening ones? Because I'm not sure if mom handled it before she left." Someone drove over just to check. Someone else called twice in one day about the same dose.

Nobody is careless. Nobody is irresponsible. We're all trying. There's just no shared source of truth — and that gap creates a specific kind of anxiety that's hard to explain to someone who hasn't lived it. You walk in and you genuinely don't know. And the wrong answer in either direction has real consequences.

A few months ago I came across [this thread](https://www.reddit.com/r/caregivers/comments/1pqguaa/what_systems_actually_prevent_doubledosing_when/) by **u/azamat_valitov** in this sub — someone else asking the exact question we keep asking each other. The responses were solid: MAR sheets, pharmacy blister packs, rotating dispensers. All legitimate. All built for professional settings with consistent schedules and trained staff. None of them workable for three adults with day jobs and irregular hours.

And then I noticed: I have the same problem with my *own* medications.

I start a course of antibiotics. I feel better on day 4. I stop taking them. We all do this — there's no friction in stopping, no one holding you accountable, and "I feel fine" beats "I should finish the course" every time. The infection comes back, and I act surprised.

So I'm dealing with both ends of this: coordinating meds for someone who can't manage it alone, and failing to manage my own even when I can.

The CDC estimates **125,000 people die annually in the US from medication errors**. There are **63 million family caregivers** in this country right now, up **19% since 2020**. The average family coordinating care for a sick or elderly relative does it across 2–4 people — with sticky notes and group chats.

I looked for an app built specifically for this. There wasn't one — or at least nothing that handled the coordination layer between people, not just reminders for one person.

**If you've found something that actually solves the shared confirmation problem between caregivers, I genuinely want to know — drop it in the comments.** Because if it exists and I missed it, I'd rather use it than build it.

So I started building one. Working name: **DoseSync**.

I'm building it for my grandmother. For my mom and her sister. For the 11pm phone call that shouldn't have to happen. And honestly — for myself.

Before I go further, I want to ask the people who actually live this:

**1.** What's the last time your system failed — not in theory, but actually? What happened?

**2.** Who else is involved in managing meds in your household — and who's the weakest link in the chain? (No judgment — in ours it's me.)

**3.** Would you actually use an app for this — or does it feel like one more thing to maintain? What would need to be true for it to stick?

I'm reading everything.

---

### ПОСТ 2 — Лонч-пост (со ссылкой на App Store)
**Саб:** r/caregivers
**Статус:** ✅ Готов
**Цель:** Первые скачивания, фидбек от целевой аудитории

**Title:** This thread from a few months ago described my problem better than I could. Nobody had a clean answer. So I built one.

---

A few months ago I came across [this post](https://www.reddit.com/r/caregivers/comments/1pqguaa/what_systems_actually_prevent_doubledosing_when/) by **u/azamat_valitov** in this sub.

I wasn't the one who asked it. But I could have been.

I was in the same situation: coordinating medications for a family member across three people — myself, my spouse, and a home nurse. The fear wasn't missing a dose. It was the gap between us — two people trying to be careful, no shared source of truth, and a moment at 11pm where nobody was fully certain whether a dose had already been given.

I read through every response in that thread. People suggested real systems: MAR sheets, rotating dispensers, pre-packaged pharmacy blister packs. I looked into all of them.

Every single one had the same failure point in a home setting. They require either professional infrastructure, strict shift discipline, or someone who never forgets to write things down — under stress, at 2am, when a family member is in pain.

What I actually needed wasn't a reminder system. It was **shared certainty** — one place where anyone on the care team could confirm a dose in two seconds, and that everyone else could see instantly. Not a shared notes app. Not a text thread. Real-time confirmation that eliminates the "did someone already give it?" question entirely.

I looked for an app that did this. There wasn't one. Every medication app is built for one person tracking themselves. The multi-caregiver coordination layer — not shared reminders, but shared real-time confirmation — simply didn't exist as a consumer product.

So I spent three months building it.

**DoseSync** is an iOS app for families and small care teams:
- Anyone confirms a dose → everyone else sees it immediately
- Double-dose alert if something was already logged in the safety window
- Guest access via shared link or QR code — no account needed for a sibling or home nurse
- Full timestamped log: who gave what, when

It's live on the App Store now. Free to download.

I wanted to post here first — because this community is where I realized I wasn't the only one dealing with this. If you're in a caregiving situation, I'd genuinely value your feedback. Especially edge cases I haven't thought through.

[App Store link]

---

### ПОСТ 3 — r/Parenting
**Статус:** ✅ Готов

**Title:** "Did you already give the Tylenol?" — this question nearly caused a double-dose at 2am in our house

---

Our son had a fever. I gave him Tylenol around 1am and went back to sleep.

At 2:30am my wife got up. He was still warm. She couldn't remember if I'd given it.

She woke me up to ask. I was half-asleep and honestly not 100% sure either. We sat there going back and forth for five minutes before deciding to wait and see.

He was fine. But that moment stayed with me — because the stakes were real, and the uncertainty was completely unnecessary.

This isn't just a sleep-deprived parents problem. It happens when grandparents are watching the kids. When a nanny is covering a shift. When one parent is traveling and the other is managing everything alone and texting updates into a thread nobody's reading carefully.

Kids' medications have dosing windows. Doubling up on acetaminophen or ibuprofen isn't harmless. And verbal confirmation at 2am from someone half-asleep is not a system.

We tried the whiteboard. We tried texting each other. Both worked until they didn't.

I couldn't find an app that solved the actual coordination problem — not reminders, but shared real-time confirmation. So I built one.

**DoseSync**: you confirm a dose, your co-parent or caregiver sees it instantly. Double-dose alert if something was already logged in the safety window. No account needed for grandma or the nanny — they join via a link or QR code.

Free on the App Store.

Do you have a system that actually works for this? I'd genuinely like to hear what's held up for other families.

[App Store link]

---

### ПОСТ 4 — r/getdisciplined
**Статус:** ✅ Готов

**Title:** I tested every system for tracking medications across multiple caregivers. Here's exactly where each one broke down.

---

When I was coordinating medications for a family member across three people, I tried to build a reliable system. Here's the honest breakdown:

**Paper log on the fridge** — held up until someone was rushing and skipped it. Or the home nurse had her own log and they diverged.

**Shared Google Sheet** — nobody opened it in the moment. Too many steps between "give medication" and "log it."

**WhatsApp group** — actually worked for a while. Until the thread got busy and finding whether a dose was logged meant scrolling back through 30 messages at 11pm.

**Pill organizer with daily sections** — solves forgetting, not coordination. The pill being present doesn't mean it wasn't already given by someone else.

**Verbal check-ins** — the default fallback. Works fine until 2am when memory gets unreliable.

The failure pattern across all of them: any system requiring a separate step to *check* breaks down under stress or fatigue. Confirm the dose is one action. Verify someone else already did it is a second action. That gap is where mistakes happen.

What I needed was a system where confirming a dose *was* the notification — one action, instantly visible to everyone.

I couldn't find an app built for this. So I built it: **DoseSync**. Confirm a dose, everyone on the care team sees it in real time. Double-dose alert within the safety window. No account needed for secondary caregivers.

Free on the App Store.

If you've built a tighter system for this kind of coordination — especially across shift-based or part-time caregivers — I'd genuinely like to hear what worked.

[App Store link]

---

### ПОСТ 5 — r/SideProject
**Статус:** ✅ Готов

**Title:** I asked r/caregivers how families actually prevent double-dosing across multiple caregivers. Nobody had a clean answer. Spent 3 months building one.

---

A few months ago I posted this in r/caregivers: [link]

The situation: coordinating medications for a family member across multiple people — and the hardest part wasn't forgetting a dose. It was not knowing if someone else had already given it.

We had near-misses. Not from carelessness — from having too many people trying to help with no shared source of truth.

The thread got solid responses. People shared what works in professional settings: MAR sheets, rotating dispensers, pharmacy blister packs. All legitimate. All with the same catch — they require professional infrastructure or perfect discipline. In a home setting with a spouse, a sibling, and an occasional nurse, none of them held up.

What I needed wasn't a reminder. It was **shared certainty** — one place anyone on the care team could update in two seconds, and everyone else could see instantly.

I looked for an app that did this. There wasn't one. Every medication app is built for one person tracking their own meds. The multi-caregiver real-time coordination layer didn't exist as a consumer product.

So I built DoseSync over 3 months.

**What it does:**
- Confirm a dose → everyone on the care team sees it in real time
- Double-dose alert if something's already logged within the safety window
- Guest access via shared link or QR code — no account needed for a sibling or home nurse
- Timestamped log: who gave what, when, any notes
- Grandparent mode — simplified UI for the care recipient to self-confirm

Stack: Swift/SwiftUI, Supabase Realtime, CloudKit. Live on the App Store, free to download.

Happy to talk through any product decisions — onboarding friction, real-time sync architecture, or go-to-market. Also: what am I missing as a consumer health product?

[App Store link]

---

## ИДЕИ ДЛЯ КОММЕНТАРИЕВ

*(Комментарии пишутся от первого лица, без упоминания DoseSync в первые 2 недели)*

---

### КОМ-1 — Ответ на вопросы про координацию лекарств
**Где:** r/caregivers, r/AgingParents, r/dementia
**Триггер:** Кто-то спрашивает "how do you manage meds between multiple caregivers?"

> We went through everything — paper log on the fridge, a shared Google Sheet, a WhatsApp group. Each one worked until it didn't. The paper log broke down when someone was in a hurry. The Google Sheet nobody opened in the moment. WhatsApp became a 60-message thread where finding the last dose update meant scrolling forever.
>
> What finally helped us: treating the confirmation itself as the notification. One person does it, everyone else knows immediately. We haven't found a great app for it, but even a simple shared note that updates in real time is better than any of the above.
>
> What's your care team setup? That usually determines which system has a chance of actually working.

---

### КОМ-2 — Ответ на страх двойной дозы
**Где:** r/Parenting, r/Mommit, r/daddit
**Триггер:** "Did I already give the Tylenol?" / "afraid of double dosing"

> That 2am uncertainty is one of the worst feelings. We had the same thing with our kids' fever meds — two people both trying to be careful, neither fully sure.
>
> The thing that helped most was separating "did someone give it?" from "who should give it next." They're different questions and most systems only answer the second one.
>
> For us it came down to: whoever gives the dose has to leave some kind of timestamped trail that the other person can see without having to ask. Text message works, but it gets buried. Sticky note works, but only if you're both home.
>
> Have you tried keeping a dedicated note in something shared — even just Apple Notes with both of you on it? Not perfect, but faster to check than a text thread.

---

### КОМ-3 — Ответ на пост про забытые курсы лечения
**Где:** r/getdisciplined, r/productivity, r/AskReddit
**Триггер:** "I always stop taking antibiotics when I feel better"

> Same. I've done this probably a dozen times. The problem is the feedback loop is completely backwards — you stop taking the meds exactly when your body is sending you the "everything is fine" signal.
>
> The only thing that's worked for me: turning it into a tracking habit instead of a discipline habit. If I can see the streak of days I've taken it, missing a day feels like breaking something concrete rather than just... not doing a thing.
>
> Also having someone else know you're on a course helps. Not to remind you, just the awareness that there's a shared record somewhere.

---

### КОМ-4 — Ответ про пожилых родителей и сложные расписания
**Где:** r/AgingParents, r/dementia, r/SandwichGeneration
**Триггер:** Managing meds for elderly parent with complex schedule

> This is the exact situation we're in with my grandmother — 11 different medications, three of us managing her schedule, nobody ever 100% certain what's been given.
>
> The hardest part isn't the complexity of the schedule itself. It's the handoff between people. When my mom leaves and her sister arrives, there's a 10-minute window where nobody knows what's happened in the last hour. That's where the risk lives.
>
> What's helped us is being really explicit about the handoff moment — treating it like a shift change in a hospital. "Here's what she took, here's what's next, here's anything unusual." We do it over text now but it's clunky. Would love to find something built specifically for this.
>
> How many people are on your care team?

---

### КОМ-5 — Ответ в r/Biohackers / r/Peptides про точность логирования
**Где:** r/Biohackers, r/Nootropics, r/Peptides
**Триггер:** Tracking complex supplement/peptide protocols

> The logging problem in serious stacks is underrated. Most apps are built for simple daily meds — they fall apart the moment you have cycling protocols, off-period tracking, or anything where the "when" matters as much as the "what."
>
> The other gap: sharing your log with a coach or training partner. There's no clean way to give someone read access to your stack history without just screenshotting a notes app.
>
> What are you using for timestamped logging right now? I've been looking at this problem from a different angle (family caregiving) but the underlying need seems identical.

---

### КОМ-6 — Ответ на ADHD / forgetting meds
**Где:** r/ADHD, r/ChronicIllness, r/productivity
**Триггер:** "I keep forgetting to take my meds" / "how do you stay consistent with medication"

> The consistency problem with ADHD meds is its own loop — the thing that helps you remember is the thing you keep forgetting to take.
>
> What helped me most: making the confirmation a social action, not a solo one. When there's even one other person who can see whether you took it, the accountability changes completely. Doesn't have to be a caregiver — could just be a partner glancing at a shared log.
>
> Streaks also help. Not gamification for its own sake, but having a visible number that breaks if you miss — that creates real friction around skipping.
>
> What's worked for you?

---

### КОМ-7 — Ответ в r/coparenting про координацию лекарств
**Где:** r/coparenting, r/Parenting
**Триггер:** "How do you track meds between two houses?" / "ex gives different doses"

> This is one of the harder coordination problems because you can't just put a note on the fridge. The information has to travel between households in real time.
>
> We ran into this with a family member — not co-parenting but similar dynamic: two separate households, both responsible for the same person's medications, no shared system.
>
> The only thing that actually worked: one shared log both sides can update and see instantly. Doesn't matter who's with the kid — whoever gives the dose logs it, the other parent sees it immediately. No "did you give it?" texts.
>
> What are you currently using?

---

### КОМ-8 — Ответ в r/nursing / r/HomeHealthAide
**Где:** r/nursing, r/HomeHealthAide
**Триггер:** Home care coordination, MAR systems for non-institutional settings

> The MAR system gap in home care is real. Everything professional-grade assumes a facility — shift structure, dedicated staff, consistent handoffs. None of that maps onto a family home where you've got a mix of professional aides and family members sharing responsibility.
>
> In institutional settings the coordination is built into the workflow. In home care it's usually verbal + paper, which means it's only as reliable as the person who last touched the chart.
>
> Curious what systems you've seen actually work in home settings — not SNF or hospital, but residential?

---

## МОНИТОРИНГ — Инструменты для отслеживания триггеров

### F5Bot (бесплатно)
Email-уведомления при упоминании ключевых слов на Reddit. Настроить алерты на:
- `medication tracker`
- `double dose`
- `caregiver app`
- `who gave the medicine`
- `forgot to take meds`
- `coordinating medications`
- `pill reminder family`

👉 https://f5bot.com

### GummySearch
Анализ Reddit-сообществ: поиск pain points, частых запросов, языка аудитории. Использовать для изучения r/ADHD, r/ChronicIllness, r/caregivers перед написанием постов.

👉 https://gummysearch.com

---

## ФОРМАТЫ ПОСТОВ (расширенные)

### Формат A — "Я решил эту проблему" (organic story)
Личная история → попытки решить → gap → начал строить. Без прямой ссылки на продукт. Заканчивается вопросом к комьюнити.
**Лучшие сабы:** r/CaregiverSupport, r/AgingParents, r/caregivers

### Формат B — Ответ на чужой пост
Мониторить через F5Bot → находить релевантные треды → отвечать с реальной пользой → упоминать DoseSync как одну из опций (не единственную).
**Правило:** всегда давать альтернативы, не только свой продукт.

### Формат C — AMA / Launch post
"I built a free medication coordination app for caregivers after almost double-dosing my grandmother. AMA"
**Лучшие сабы:** r/SideProject, r/iOSProgramming, r/AlphaandBetausers

### Формат D — Полезный контент без продукта
Checklists, guides, цифры — без упоминания DoseSync в посте. Ссылка на приложение только в профиле.
Примеры тем:
- "5 ways to prevent double-dosing when multiple caregivers are involved"
- "Medication coordination checklist for families with elderly parents"
- "Why 125,000 Americans die from medication errors annually — and what families can do"

**Лучшие сабы:** r/AgingParents, r/ChronicIllness, r/CaregiverSupport

---

## КОНТЕНТ-ПЛАН

| Неделя | Действие | Саб | Статус |
|--------|----------|-----|--------|
| 1–2 | Комментарии только (КОМ-1 – КОМ-8) | Tier 1 + Tier 2 | 🔴 |
| 3 | Прогревочный пост (ПОСТ 1) | r/caregivers | 🔴 |
| 3 | Формат D — полезный контент | r/AgingParents, r/ChronicIllness | 🔴 |
| 4 | Комментарии Tier 3 + Tier 4 | r/ADHD, r/Biohackers, r/nursing | 🔴 |
| 5 | Лонч-пост (ПОСТ 2) | r/caregivers | 🔴 |
| 5 | Параллельные посты | r/Parenting, r/SideProject | 🔴 |
| 6 | Посты Tier 3 | r/ADHD, r/Biohackers, r/getdisciplined | 🔴 |
| 6 | AMA пост | r/AlphaandBetausers, r/iOSProgramming | 🔴 |

---

## ПОШАГОВЫЙ ПЛАН: СЕЙЧАС → РЕЛИЗ → ПОСЛЕ

> Релиз DoseSync v1.0 — **10 июня 2026**
> Сегодня: 7 апреля 2026 → до релиза **9 недель**

---

### 🔧 ФАЗА 0 — Подготовка (Сейчас, эта неделя)

**Разовые действия — делаем один раз:**

- [ ] Купить 2 аккаунта на redaccs.com ($82) — Comment Karma, 3 года
- [ ] Перед покупкой: проверить историю каждого аккаунта на reddit.com/u/[username] — нужны нейтральные или health/family темы
- [ ] Выбрать никнеймы (не содержат: dose/sync/med/pill/health/care)
- [ ] Заполнить профили: аватар, краткое bio без упоминания DoseSync, 1-2 нейтральных поста-интро ("just moved to Reddit after years of lurking")
- [ ] Настроить **F5Bot** (бесплатно) — алерты на: `medication tracker`, `double dose`, `caregiver app`, `who gave the medicine`, `forgot meds`, `coordinating medications`
- [ ] Опционально: GummySearch на 1 месяц ($79) для анализа языка аудитории в r/ADHD и r/ChronicIllness

---

### 💬 ФАЗА 1 — Прогрев аккаунтов (Недели 1–2, 7–20 апреля)

**Только комментарии. DoseSync не упоминается вообще.**

| Аккаунт | Сабреддиты | Шаблоны | Цель кармы |
|---------|-----------|---------|------------|
| A — "Человек" | r/caregivers, r/AgingParents, r/CaregiverSupport, r/Parenting | КОМ-1, КОМ-2, КОМ-4, КОМ-7 | 50+ karma |
| B — "Строитель" | r/SideProject, r/indiehackers, r/Biohackers, r/ADHD | КОМ-3, КОМ-5, КОМ-6 | 50+ karma |

**Темп:** 3–4 комментария в день на каждый аккаунт
**Время:** 20–30 минут/день
**F5Bot:** реагировать на все триггеры в течение 24 часов

---

### 📝 ФАЗА 2 — Первый пост (Неделя 3, 21–27 апреля)

- [ ] Аккаунт A: опубликовать **ПОСТ 1** (бабушка, 11 таблеток) в r/caregivers
  - Вторник или среда, 9–11am EST
  - Мониторить комментарии первые 48 часов — отвечать на каждый
- [ ] Аккаунт A: параллельно — **Формат D** (чеклист без продукта) в r/AgingParents
- [ ] Аккаунт B: продолжает только комментарии в Tier 3–4
- [ ] Записать: сколько комментариев, какие вопросы задали → инсайты в продукт

---

### 📣 ФАЗА 3 — Расширение (Недели 4–5, 28 апреля – 11 мая)

- [ ] Аккаунт A: ПОСТ 1 адаптированный → r/Parenting ("Tylenol at 2am")
- [ ] Аккаунт A: ПОСТ 1 адаптированный → r/coparenting
- [ ] Аккаунт B: первый пост в r/SideProject (ПОСТ 5 — builder story)
- [ ] Оба аккаунта: активно мониторим F5Bot, отвечаем на триггеры КОМ-1–8
- [ ] Аккаунт B: пост в r/EntrepreneurRideAlong — "building DoseSync, week N update"
- [ ] Подготовить финальный лонч-пост (ПОСТ 2) с App Store ссылкой

---

### 🚀 ФАЗА 4 — Релиз (Неделя 6, ~10 июня)

**День релиза (10 июня) — публикуем всё в один день с разбивкой по времени:**

| Время (EST) | Действие | Аккаунт |
|-------------|----------|---------|
| 9:00 | ПОСТ 2 (лонч) → r/caregivers | A |
| 10:00 | ПОСТ 3 → r/Parenting | A |
| 11:00 | ПОСТ 5 → r/SideProject | B |
| 13:00 | AMA-пост → r/AlphaandBetausers | B |
| 15:00 | Show & Tell → r/iOSProgramming | B |

- [ ] Мониторить все треды каждые 2 часа первый день
- [ ] Отвечать на каждый комментарий в течение 6 часов
- [ ] Зафиксировать: downloads per post, conversion rate

---

### 📈 ФАЗА 5 — После релиза (Недели 7–10, июнь–июль)

**Не останавливаемся — комьюнити-присутствие нужно поддерживать:**

- [ ] r/InternetIsBeautiful — один пост "useful app" (огромный трафик при апвоутах)
- [ ] r/ADHD — ПОСТ про forgetting meds + DoseSync как решение
- [ ] r/Biohackers — аналитический пост про log + share use case
- [ ] r/EntrepreneurRideAlong — еженедельные апдейты о росте (build in public)
- [ ] r/seniordogs / r/dogs — pet meds use case пост
- [ ] r/nursing / r/HomeHealthAide — профессиональный use case
- [ ] r/RoastMyStartup — один раз, для честного фидбека + трафика
- [ ] Продолжать F5Bot мониторинг — органические ответы дают downloads ещё недели после релиза

---

### 📊 KPI — Как измеряем успех

| Метрика | Цель к неделе 6 | Цель к неделе 10 |
|---------|----------------|-----------------|
| Karma Аккаунт A | 150+ | 500+ |
| Karma Аккаунт B | 100+ | 300+ |
| Комментариев написано | 80+ | 200+ |
| Постов опубликовано | 5 | 15+ |
| Downloads с Reddit | 200+ | 1000+ |
| Сабреддитов охвачено | 10 | 25+ |

---

*Последнее обновление: 7 апреля 2026*
