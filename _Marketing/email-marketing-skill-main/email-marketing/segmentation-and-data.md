---
name: email-marketing/segmentation-and-data
description: >
  Segmentation strategy (basic, advanced, dynamic vs static, when not to segment),
  data types and hygiene, privacy compliance, and personalisation with merge tags.
  Reference this when advising on audience targeting, data quality, or personalisation.
---

# Segmentation and Data

## Segmentation

### The Core Case

Segmentation = sending a campaign to a subset of your list based on defined criteria. Benefits flow from one source: relevance. More relevant emails → better engagement → better deliverability → better outcomes.

ISP's track engagement signals (opens, clicks, replies, moves-to-inbox) to judge sender reputation. An email programme that consistently sends relevant content to engaged subscribers builds a positive reputation. One that blasts everyone with everything builds a negative one.

### Basic Segmentation Types

**Demographics:** Age, gender, location, job title, company size. Collected via sign-up forms or custom fields. Geo-targeting for location-specific promotions is underused.

**Engagement:** Open/click recency, engagement score, last active date. Create "active" and "inactive" segments. Treat them very differently. Never send the same content to both.

**Purchase history:** Products/categories purchased, frequency, average order value. The foundation of any ecommerce segmentation strategy.

### Advanced Segmentation Types

**RFM Analysis (Recency, Frequency, Monetary):** Three-dimensional customer value model.
- Recency: How recently did they last purchase?
- Frequency: How often do they purchase?
- Monetary: How much have they spent in total?

High-RFM customers deserve preferential treatment: early access, exclusive offers, loyalty rewards. Low-RFM customers need different nurturing or re-engagement. Some ESP's support RFM natively; otherwise build it with custom fields and dynamic segments.

**Lead Scoring:** Assigns point values to engagement actions. Aggregate score indicates purchase readiness and intent level. Requires ESP + CRM integration or a dedicated marketing automation platform. Useful for B2B email programmes where sales handoff matters.

**Psychographic Segmentation:** Interests, values, lifestyle. Collected through surveys, quizzes, and preference centres. Zero-party data is the ideal input. Higher quality than inferred behavioural data.

**Predictive Analytics:** ML models predicting future behaviour (purchase likelihood, churn risk, optimal send time). Increasingly available in higher-tier ESP's natively. Requires significant data volume to be reliable. Don't invest here before the basics are working.

### Dynamic vs Static Segments

**Dynamic segments** update automatically as subscriber data changes. Criteria are evaluated in real-time (or near-real-time) at send time.

- Use for: All ongoing campaign use; "active subscribers", "customers who haven't purchased in 90 days", "UK-based subscribers"
- Advantage: Set up once, reuse indefinitely. The list always reflects current reality.
- Default choice for most segmentation needs.

**Static segments** are fixed at creation. Membership doesn't change regardless of what happens to subscribers after.

- Use for: Historical cohorts, specific event-based groups, A/B test control/variant cells, incident response (customers affected by a bug on a specific date)
- Advantage: Precise control over membership; useful when you need a defined cohort that doesn't drift
- Use deliberately, not as default

### When Not to Segment

This is the part most email content skips. Segmentation has real costs:

- Time to define and build segments
- Time to create variant content
- Reduced audience sizes that compromise A/B test statistical power
- Increased execution complexity = increased human error risk (wrong segment selected at send)
- Echo chamber effect: subscribers never exposed to new aspects of your content

**Practical threshold:** Don't invest heavily in segmentation until total active list is in the low thousands. Below that, overhead typically exceeds benefit.

**Watch out for:** Sending an email to the wrong segment is a common and often damaging error. Always build in a verification step before sending segmented campaigns.

---

## Data Collection and Management

### Data Types

| Type | Definition | Quality | Collection Methods |
|---|---|---|---|
| Zero-party | Proactively and voluntarily shared by the subscriber | Highest — intent is explicit | Quizzes, surveys, preference centres, polls |
| First-party | Collected from direct interactions with your platforms | High | Website analytics, purchase data, ESP engagement data, CRM |
| Second-party | First-party data acquired through a partnership arrangement | Medium | Data sharing agreements with complementary businesses |
| Third-party | Purchased from external providers | Variable and declining | Data brokers, aggregators, marketplaces |

**Prioritise zero- and first-party data.** Third-party data quality is unreliable, ethical sourcing is uncertain, and regulatory risk is significant and growing.

### Data Hygiene

- Regular audits to identify inaccurate or outdated subscriber data
- Suppress hard bounces immediately and permanently
- Suppression lists: maintain and respect across all sends
- List cleaning: remove or re-permission subscribers who haven't engaged in 12+ months before they damage your sender reputation (use a proper definition of engagement, not just email engagement)
- Bounce management: monitor rates per campaign; sudden spikes indicate a problem (bought list, data quality issue, authentication failure)

### Privacy and Compliance

**GDPR (EU):** Requires a lawful basis for processing personal data; for marketing email, typically explicit consent. Strict rules on data collection, storage, use, and subject rights.

**CCPA (California):** Similar consumer rights framework; right to know, right to delete, right to opt out of sale.

**CAN-SPAM (US):** Requires honest subject lines, physical postal address in emails, and a functioning opt-out mechanism honoured within 10 business days. Less strict than GDPR.

**Practical minimums:**
- Be transparent about what you collect and how you use it
- Honour unsubscribes immediately (not 10 days later, immediately)
- Never sell subscriber data
- Include a physical address and unsubscribe link in every marketing email
- Use double opt-in in GDPR-regulated markets to have clean consent records

---

## Personalisation and Merge Tags

### Personalisation Spectrum

| Level | What it involves | Complexity |
|---|---|---|
| Basic | Merge tags (name, company, city) | Low — just requires data in subscriber fields |
| Mid-level | Segmented content blocks (show/hide based on subscriber attribute) | Medium — requires conditional logic in email builder |
| Advanced | Dynamic product recommendations, behavioural triggers, predictive content | High — requires data infrastructure and often third-party tools |

Build the base before the advanced. Most email programmes aren't using basic personalisation well before they try to build recommendation engines.

### Merge Tags: Implementation

Merge tags are placeholders replaced with subscriber-specific data at send time. Every ESP supports them; syntax varies:

| ESP | Syntax |
|---|---|
| Mailchimp | `*\|FNAME\|*` |
| Klaviyo | `{{ first_name }}` |
| ConvertKit/Kit | `{{ subscriber.first_name }}` |
| Campaign Monitor | `[firstname]` |

**Common uses:** First name, last name, company, city/country, last purchase date, product name, custom field values.

**Subject line personalisation:** Drives measurable open rate lifts in many contexts. Watch character count — adding a name eats into your 50-character budget for mobile display.

**Always set fallbacks.** If first name is empty and your email opens "Hi ," you've created a worse experience than "Hi there." Every merge tag needs a default value.

**Conditional content blocks:** Show content block A if field X equals Y; show block B otherwise. Powerful for location-specific content, customer-tier-specific messaging, or product interest-based content.
