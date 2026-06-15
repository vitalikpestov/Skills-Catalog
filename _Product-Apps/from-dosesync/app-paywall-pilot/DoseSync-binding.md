# DoseSync binding — app-paywall-pilot skill

> Adapter layer. Vendored skill (MIT, Nikolai Iakubovskii) stays untouched for clean updates. DoseSync-specific guardrails + locked decisions live here. Agents: read this BEFORE acting on skill output.

**Installed:** 2026-06-11. **Source:** github.com/Nikolai-Iakubovskii/app-paywall-pilot (v4.0.0, MIT). **Confidence on its benchmarks:** medium (single curator, 26★) — spot-checked 3/3 H&F numbers vs our RC SOSA anchor (D35 paid 2.9%, refund 4.2%, Day-0 ~82-86%) = consistent.

---

## Where it fits (use cases)

1. **Pre-submit Apple-compliance audit** (до 2026-07-18): прогнать `docs/audit-checklist.md` по `PaywallOfferView` + `PaywallPlansScreen` + Final CTA. Ловит Guideline 3.1.1/3.1.2 реджекты (см. `runbook-app-store-rejection.md` Track C). ⚡ Highest-value use сейчас.
2. **Post-launch paywall-A/B design** (gated 1000 trial starts, `volume-gate.md`): teardowns + decision-trees как источник гипотез.
3. **Benchmark supplement** к `conversion-framework.md` / `pre-launch-metrics.md`.

## Hard guardrails (НЕ нарушать — наши locked decisions перебивают skill)

| Skill может предложить | DoseSync правило (WINS) |
|------------------------|--------------------------|
| Сменить цены / SKU / структуру | **FROZEN** — Solo $5.99wk/$59.99yr, Family $7.99wk/$99.99yr. CPO-DEC PRICING-V2. Менять только через CPO + volume-gate |
| Free tier / freemium | **Запрещено** — hard paywall only ([[feedback_no_free_tier]]). «Free» = только trial |
| Trial на weekly / 3-day trial | **annual-only 7-day** (CPO-DEC PAYWALL-TRIAL-ANNUAL-ONLY-1). Не трогать |
| «Improves adherence / prevents harm» в копи | **Medical-claim red line** (`tone-of-voice.md`). Координация/напоминание, НЕ медрекомендация |
| Promo/discount ladder в drip | **≤10% promo** (SOSA target). Save-offer = goodwill, не скидка (`save-offer-ladder`) |
| Его H&F-бенчмарки как таргеты | **Наш якорь = RC SOSA** (`pre-launch-metrics.md` §2 baseline-freeze). Skill-числа = supplement, не override frozen targets |

## Honesty alignment

Skill's own rules («every numeric claim needs source ID or lower-confidence label», «Apple docs > vendor advice») совпадают с `honesty-constraints.md`. При использовании его чисел в решениях — cite source ID из `sources.json` + спот-чек ключевых против primary (RC SOSA / Adapty / AppsFlyer) перед commit.

## Stack note

DoseSync paywall = **native StoreKit 2** (`StoreKitService`, server-authoritative — RT-01 hardening). Skill упоминает RevenueCat/Adapty/Superwall — у нас их НЕТ как зависимостей (Nami тоже отклонён 2026-06-11). Игнорировать SDK-specific советы; брать только design/compliance/benchmark-слой.

## Invoke

`/app-paywall-pilot` (user-invocable). Default mode router в `SKILL.md`. Для нашего кейса: audit mode → category=Health & Fitness → пример `examples/audit-h-and-f-app.md`.
