---
name: email-marketing/automation-and-sequences
description: >
  Automation trigger types, best practices, and all sequence types: welcome,
  onboarding, abandoned cart, re-engagement, and others. Includes the full
  welcome programme build process and campaign goal-setting framework. Reference
  this when designing automations or multi-email sequences.
---

# Automation and Sequences

## Automation

### What Automation Is

Sending emails automatically in response to a trigger. Unlike a one-time campaign, an automation runs continuously on an as-needed basis.

**Key distinction:** Campaigns are sent to a defined audience at a point in time. Automations run indefinitely, enrolling subscribers as they meet the trigger criteria.

### Automation Trigger Types

| Trigger Type | Description | ESP Support | Example Use |
|---|---|---|---|
| New subscriber added to list | Fires when contact added to a list | Universal | Welcome sequences |
| Subscriber field/tag changed | Fires when a field value or tag is updated | Very common | Lifecycle stage transitions |
| Date-based | Fires at a threshold relative to a date field | Common | Birthday emails, renewal reminders, anniversary sequences |
| Import-based | Triggered by periodic CSV file import to secure FTP | Enterprise ESP's only | Legacy systems integration |
| Event/API-based | Triggered by custom event sent via API | Common | Feature usage triggers, in-app milestones, purchase events |
| RSS-based | Triggered when RSS feed is updated | Less common | Auto-send when new blog post published |

Not every ESP supports every type. Creativity can compensate: a date-based trigger can often replicate what an API trigger would do if you update subscriber fields via import.

### Automation Best Practices

- **Set a clear objective before building.** What is this automation trying to achieve?
- **Map the logic before building in the ESP.** Diagram it first.
- **Test thoroughly before going live.** Automation errors can send incorrect emails to thousands of people before anyone notices.
- **Monitor regularly.** Automations are not "set and forget." Check performance, check for errors, check that triggers are still firing correctly.
- **Have an exit condition.** What removes someone from the automation? Make sure it's defined.

---

## Email Sequences and Drip Campaigns

Sequences are two or more automated emails triggered by the same starting event, sent over time.

### Welcome Sequences

The highest-value automation any email programme can build. Open rates on welcome emails consistently outperform standard marketing campaigns. Subscribers are at peak engagement.

**A good welcome sequence:**
- Delivers on any lead magnet promise immediately (first email, no exceptions)
- Thanks the subscriber and sets expectations about what's coming
- Has a clear overarching goal (sell a product, onboard to a feature, build a relationship)
- Uses the opportunity to learn more about the subscriber (preferences, goals, context)
- Maintains consistent tone and design language across all emails
- Uses sender name and address that match the brand subscribers signed up for (not noreply@, not Employee Bob)

**Data point:** According to Mailchimp data, a welcome series generates on average 51% more revenue than a single welcome email.

### Building a Welcome Programme: The Full Process

Building a welcome programme is distinct from building a single welcome email. Here is the correct process:

#### Step 1: Define the Objective

"I want to sell more widgets" is a fine starting point. Get more specific. A welcome programme without a measurable objective is theatre. Examples of good objectives:
- Increase paid conversion within 30 days of sign-up by X%
- Reduce first-month churn by proactively addressing common objections
- Increase feature adoption (specific feature) in the first two weeks

#### Step 2: Map the Entry Points

How will people enter this programme? Website form, retail, trade show, referral programme, lead generation ad? Different entry points may mean different expectations. Decide whether you need variants or a single generic programme.

#### Step 3: Identify the Opportunities

Break the objective into specific questions your new subscribers are likely to have. If you want to sell more product, what does a new subscriber need to know to feel confident buying? Talk to sales and customer service — they know what objections and questions come up repeatedly.

Real example: A company discovered through CS that new customers were shocked by their first bill because the billing cycle was poorly communicated. Adding a billing explanation email to the welcome programme improved first-month NPS and reduced CS call volume simultaneously.

#### Step 4: Build the Copy and Sequence

- First email: Thank them, deliver any lead magnet, set expectations
- Subsequent emails: Address the opportunities identified in Step 3, one per email
- Consistent tone, design language, and sender identity throughout
- Don't over-rely on copy; video can work exceptionally well in welcome sequences
- Consider inviting replies in the first email (not from noreply@): breaks through the automation feeling, creates real relationship signals

#### Step 5: Launch

Go live. You'll rarely be happy with everything. Ship it.

#### Step 6: Optimise Continuously

Measure against the objective. The data will tell you what to change. Don't be precious about what you built — radical changes sometimes produce radical results.

### Onboarding Sequences

Closely related to welcome sequences but purpose-built for getting a new customer or user to their first meaningful engagement with your product. Goal is activation, not just relationship-building. Often appropriate for SaaS, apps, digital products.

### Abandoned Cart Sequences

For ecommerce. Send when a subscriber adds items to cart and leaves without purchasing. One of the highest-ROI automations in ecommerce email.

**Sequence structure (typical):**
- Email 1: Reminder (2–4 hours after abandonment)
- Email 2: Social proof / urgency (24 hours later)
- Email 3: Incentive if warranted (48–72 hours later)

**Caution on discount codes:** Savvy shoppers will deliberately abandon carts to trigger discount sequences. If you include a discount, make it the last email, not the first, and consider only offering it to first-time buyers.

### Re-engagement Sequences

Target subscribers who have gone inactive (no opens/clicks in 90, 180, or 365 days, depending on your send frequency). Goal is to re-activate them or gracefully remove them from the active list.

**Why it matters:** Harvard Business Review data suggests acquiring a new customer costs five to twenty-five times more than retaining an existing one. Re-engagement is commercially valuable.

**Sequence structure:**
- Email 1: Check-in / "We miss you" angle
- Email 2: Value proposition reminder / what's changed since they last engaged
- Email 3: Explicit opt-in request / "Should we keep sending?"
- Suppression: Remove non-responders from active campaigns after sequence completes

### Other Valuable Sequence Types

- Post-purchase sequences (cross-sell, review request, loyalty programme introduction)
- Lead nurturing sequences (B2B: moving prospects through the funnel)
- Customer feedback / NPS sequences
- Upsell/upgrade sequences (for subscription businesses)
- Event/webinar sequences (pre-event and post-event)

---

## Campaign Goal-Setting

This is a foundational step that is frequently skipped. Enforce it.

**Before building any campaign or automation, a goal must be defined.**

A campaign designed to sell a product looks completely different from one designed to increase feature adoption in a SaaS product. An automation onboarding new customers has different logic to one re-engaging dormant ones.

**Goal-setting framework:**
1. What specific outcome do you want this email/sequence to achieve?
2. How will you measure whether it achieved it?
3. What does the subscriber need to believe or feel to take that action?

Without a clear answer to all three, the campaign lacks focus. Unfocused campaigns produce poor results regardless of execution quality.

**Common goal types by business context:**

| Business Type | Example Goals |
|---|---|
| Ecommerce | Drive purchase of product X; recover abandoned carts; increase AOV |
| SaaS | Increase trial-to-paid conversion; drive feature adoption; reduce churn |
| Media/content | Increase content consumption; drive paid subscription upgrade |
| B2B/services | Generate qualified leads; book discovery calls; nurture to proposal stage |
| Ecommerce (retention) | Increase repeat purchase rate; grow loyalty programme enrolment |
