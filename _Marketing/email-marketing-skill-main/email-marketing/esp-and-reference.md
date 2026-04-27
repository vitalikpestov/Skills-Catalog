---
name: email-marketing/esp-and-reference
description: >
  ESP evaluation framework (five factors: features, cost, support, integrations,
  expandability), legislation quick reference (CAN-SPAM, GDPR, CASL, CCPA),
  common mistakes table, and full glossary. Reference this when comparing
  platforms, checking legal requirements, or looking up terminology.
---

# ESP Selection and Reference

## Finding and Evaluating an ESP

Over 220 email platforms exist (per ChiefMartec). Most beginners overthink this. For small lists, most entry-level platforms are functionally similar. Pick one that feels intuitive and move on.

For serious evaluation, use this five-factor framework in priority order:

### 1. Features

Must-have checklist:
- Visual email editor (quality matters; template library helps)
- Automation support (autoresponders at minimum; full drip campaign builder preferred)
- Segmentation capabilities (dynamic segments based on engagement and custom fields)
- List growth tools (embedded forms, popup forms, exit intent)
- Personalisation tools (merge tags, conditional content blocks)
- A/B testing (subject line testing at minimum; content and send time testing preferred)
- Reporting quality (can you export data? Is the analytics dashboard useful?)

Know your must-haves vs nice-to-haves before starting comparisons.

### 2. Cost

Key questions:
- Can you afford the monthly subscription at your current list size?
- How do costs scale as your list grows? Are there per-contact or per-send limits?
- Are must-have features available at your price point, or locked behind more expensive tiers (push pricing)?
- Is there a free tier for small lists?

### 3. Support

Key questions:
- Is there live chat, ticketing, or phone support?
- How responsive are they? Check G2, Capterra, or Twitter mentions.
- Is there a comprehensive help documentation site?
- Is there a large user community generating helpful tutorials?

More important for less technical users. Less important if you're technically confident and self-sufficient.

### 4. Integrations

Key questions:
- Does it integrate with your CRM, ecommerce platform, website CMS?
- Are integrations native or via Zapier/Make (native is always more reliable)?
- Does the integration do what you actually need, or just a basic sync?

Only matters if you have specific integration requirements. Don't over-engineer this.

### 5. Expandability

The least important factor. Migrating between ESP's is easier now than it used to be. Don't pay for features you don't need yet on the promise you'll need them later. Start on the tier that serves your current needs.

**For beginners:** Most entry-level platforms (Mailchimp, Kit/ConvertKit, MailerLite, Brevo) are broadly similar under 1,000 subscribers. Many are free at that scale. Pick the one that feels most intuitive and get started. Stop researching.

---

## Legislation Quick Reference

Email marketing is regulated across most markets. This is not legal advice; treat it as orientation, then get proper counsel for your specific situation.

| Regulation | Jurisdiction | Consent model | Key requirements |
|---|---|---|---|
| CAN-SPAM | USA | Opt-out (no prior consent required for B2C) | Honest subject lines, physical address, working unsubscribe (10 days), sender identified |
| GDPR | EU + EEA | Opt-in (explicit consent or legitimate interest for existing customers) | Lawful basis required, data subject rights, privacy notice, records of consent |
| UK GDPR + PECR | UK | Opt-in for individuals; legitimate interest possible for corporate contacts | Similar to EU GDPR; PECR specifically covers electronic marketing |
| CASL | Canada | Opt-in (express or implied consent) | Express consent is explicit; implied consent has time limits (2yr purchase, 6mo inquiry) |
| CCPA | California, USA | Opt-out for sale of data; disclosure required | Right to know, right to delete, right to opt out of data sale |

**Practical minimum compliance:**
- Get consent before emailing (or have a documented legitimate interest basis)
- Include physical postal address in every marketing email
- Include a working, clearly visible unsubscribe link
- Honour opt-outs immediately (not in 10 days)
- Keep records of how/when consent was obtained
- Be honest about who you are and what you're sending

**Highest-risk scenarios:**
- Buying or renting email lists
- Continuing to email after an unsubscribe
- Adding contacts to marketing lists without their knowledge
- Sending marketing email to EU/UK subscribers without proper consent records

---

## Quick Reference: Common Mistakes and How to Avoid Them

| Mistake | Why it matters | Fix |
|---|---|---|
| Missing SPF/DKIM | Deliverability problems, block bounces | Set up authentication before first send |
| Not suppressing hard bounces | Damages sender reputation, increases bounce rate | Auto-suppress hard bounces immediately; never re-send to them |
| Ignoring mobile display | 50%+ of email opens are on mobile | Test all emails on mobile before sending |
| Not having a goal for campaigns | Can't measure success, can't improve | Define objective before building |
| Over-segmenting small lists | Small audiences, unreliable test results, human error | Wait until list is in low thousands before heavy segmentation |
| Discount codes in welcome/abandoned cart sequences | Trains customers to game the system | Offer discounts last, not first; for first-time buyers only |
| Sending from noreply@ | Kills reply engagement signals, bad practice | Use a monitored address |
| Not delivering lead magnet in first email | Breaks trust immediately | First email must fulfil the promise |
| Trusting open rates as precise metrics | Systematically inaccurate due to pixel tracking issues | Treat as directional; use CTOR as better content metric |
| Not testing automations before going live | Errors run at scale silently | Always test trigger, content, and timing before activating |

---

## Glossary

| Term | Definition |
|---|---|
| ESP | Email Service Provider — the platform used to send marketing email (Mailchimp, Klaviyo, etc.) |
| Deliverability | The ability to get emails into the inbox (not spam folder or blocked) |
| Sender reputation | ISP's assessment of your sending quality, based on engagement signals, bounce rates, spam complaints |
| Suppression list | List of addresses that should never receive email (hard bounces, unsubscribes, spam complaints) |
| Dynamic content | Content blocks in an email that display differently based on subscriber data |
| Merge tag | A placeholder in email copy that gets replaced with subscriber-specific data at send time |
| Drip campaign | A series of automated emails sent over time; also called an email sequence |
| A/A test | Sending the same email to two randomly split groups to validate that your test setup is unbiased before running A/B tests |
| UTM parameters | Tags appended to URLs to track source, medium, and campaign in analytics platforms |
| CTOR | Click-to-open rate: clicks divided by opens. Measures content engagement independent of open rate noise |
| RFM | Recency, Frequency, Monetary — a customer value scoring model |
| Zero-party data | Data a customer voluntarily and proactively shares with you |
| First-party data | Data collected from direct customer interactions with your own platforms |
| GDPR | General Data Protection Regulation — EU data privacy law |
| CAN-SPAM | US law governing commercial email; less strict than GDPR |
| Tracking pixel | A 1×1 transparent GIF image embedded in emails to track opens |
| Block bounce | Email rejected by receiving server, typically due to authentication failure or sender blocklist |
| Hard bounce | Permanent delivery failure due to invalid/non-existent address |
| Soft bounce | Temporary delivery failure; address likely valid |
| Double opt-in | Two-step subscription process requiring email confirmation before adding to active list |
| Lead magnet | An incentive offered in exchange for an email address |
| Welcome programme | A series of automated emails sent to new subscribers to achieve a defined objective |
| Dynamic segment | A list segment that updates automatically as subscriber data changes |
| Static segment | A list segment with fixed membership set at creation time |
