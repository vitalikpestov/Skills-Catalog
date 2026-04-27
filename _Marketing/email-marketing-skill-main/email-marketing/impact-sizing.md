---
name: email-marketing/impact-sizing
description: >
  How to size the potential impact of email and lifecycle marketing experiments.
  Covers model types, formula mechanics, input gathering, sample size planning,
  and common mistakes. Reference this when estimating how many incremental
  actions a campaign or experiment will drive, or when prioritizing experiments.
---

# Impact Sizing for Email Campaigns

## Why Impact Sizing Matters

Every experiment competes for resources — engineering time, design, copy, QA. Without a sizing model, prioritization happens by gut feel, seniority, or whoever talks loudest in the meeting. Impact sizing replaces opinion with arithmetic.

A good impact model answers one question: **"How many incremental actions will this experiment drive?"** That number lets you rank experiments against each other, set expectations with stakeholders, and retroactively evaluate whether an experiment delivered what it suggested.

Impact sizing is not forecasting. You're not predicting the future. You're building a calculator that says "if we achieve X% lift on Y metric for Z users, the result is N incremental actions." The model is only as good as its inputs, but even rough inputs produce useful signal for prioritization.

## Three Model Types

Not every experiment is sized the same way. I suggest three distinct patterns here.

### Single-Metric (the default)

Most experiments target one metric: activation rate, feature adoption rate, conversion rate. The model is simple: take the audience, apply the baseline rate, apply a lift, calculate the incremental actions.

Use this when the metric you're trying to move is the metric you care about. No funnel, no promo mechanics — just "we want to increase X."

### Two-Metric (funnel)

Some experiments target an upfunnel action that feeds a downstream outcome. For example: increasing onboarding completion (upfunnel) because it drives paid conversion (downstream). Sizing this requires two rates — the upfunnel action rate and the downstream conversion rate of users who completed the upfunnel action.

Use this when someone says "we want to improve X because it drives Y." If there's a "because" connecting two metrics, it's a funnel model.

### Promotional (revenue viability)

Promos — free months, discounts, credits — need a different model entirely. The question isn't "how many incremental actions" but "will we gain more from offering this promotion than it costs us? How much more, and on what time frame?" This requires plan mix, per-plan gross profit, promotion cost, and a retention adjustment for promo-acquired users (who typically churn faster than organic).

Use this when there's a cost attached to the incentive.

## The Core Formula

All single-metric and funnel models share the same foundation:

**Non-actors** = Audience × (1 − Baseline rate)

**Target rate** = Baseline rate × (1 + Relative lift)

**Incremental actions** = (Target rate − Baseline rate) × Non-actors

The relative lift percentage is the single variable you change to model scenarios. Everything else is an observed input.

For funnel models, add one step:

**Incremental downstream actions** = Incremental upfunnel actions × Downstream conversion rate

For promotional models, the formula shifts to:

**Incremental subs** = Audience × Baseline activation rate × Projected lift

**Net incremental value** = (Incremental subs × Retention-adjusted GP) − (Incremental subs × Weighted promo cost)

Revenue-positive if net incremental value > 0.

## Getting the Inputs Right

Impact sizing is only as good as its inputs, and getting clean inputs is where most models go wrong.

### Metric definition

The most common failure mode is building a technically correct model on a misunderstood metric. "Subscription rate" means different things at different companies. Always confirm the exact formula: numerator, denominator, and time window. A rate measured over 7 days produces a very different model than the same rate measured over 30 days.

### Baseline rate

Ask where it came from and when it was measured. Conversion rates shift seasonally and after product changes. A baseline pulled from a holiday period or a week after a major product launch will skew the model. The more recent and representative the baseline, the better.

### Audience size and cadence

This is the distinction most people miss. Some experiments target a **flow** — new users entering each week. Others target a **stock** — a fixed pool of existing users in a particular state. Flow models produce incremental actions per week. Stock models produce a total from the addressable pool. Mixing these up inflates or deflates the estimate dramatically.

### Segment definitions

Always confirm whether segments overlap. "Free users" and "users who haven't completed onboarding" are not mutually exclusive. Adding overlapping segments together double-counts the audience. Ask explicitly: are these segments mutually exclusive?

### Lift target

If there's precedent from a past experiment, use it. If not, 5% relative lift is a reasonable conservative default — but flag it clearly as an assumption. Overpromising on lift is the fastest way to lose credibility with stakeholders.

## Sample Size and Test Duration

A sizing model without a sample size estimate is incomplete. It tells you what you *could* achieve but not whether you can *detect* it.

The standard approach is a two-proportion z-test: one-sided, 80% power, 95% confidence. The formula:

**Users per variant** = (Z_α + Z_β)² × (p1(1−p1) + p2(1−p2)) / (p2 − p1)²

Where Z_α = 1.6449 and Z_β = 0.8416 (giving (Z_α + Z_β)² ≈ 6.18).

**Total test duration** = (Users per variant × 2) / Users entering per week

This matters because a model might show a compelling opportunity that requires 16 weeks of test time to detect — at which point you need to decide whether the opportunity justifies that commitment, or whether resources are better spent on a faster test.

## Common Mistakes

**Sizing without defining the metric first.** The model looks precise but measures the wrong thing. Always start with the metric definition - what's the timeframe over which you're measuring conversion? What counts as a conversion?

**Using stale baselines.** A baseline from six months ago may not reflect current performance. Insist on recent data.

**Ignoring the flow vs. stock distinction.** A model that shows "500 incremental activations" means very different things depending on whether that's per week or total.

**Over-segmenting small audiences.** Splitting a 2,000-person audience into four segments means each segment is too small to detect meaningful lift. Resist the urge to over-segment.

**Treating the model output as a commitment.** Impact sizing is for prioritization, not for setting OKR targets. The model says "this is plausible if our assumptions hold." It does not say "this will happen."

## Promotional Model Defaults

When sizing promos, two assumptions often need defaults:

| Input | Default | Rationale |
|---|---|---|
| Promo-acquired retention rate | 85% of organic | Promo-acquired users tend to churn faster. Conservative starting point. |
| Target lift (no precedent) | 5% relative | Conservative default. Flag as assumption. |
