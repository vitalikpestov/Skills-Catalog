---
name: email-marketing/deliverability
description: >
  Email deliverability (how it works, getting out of spam, IP warming), complete
  metrics reference (open rate problem, CTOR, bounce types, business outcomes),
  Gmail Promotions tab, and MIME/email technical structure. Reference this when
  diagnosing deliverability issues or explaining email metrics.
---

# Deliverability and Metrics

## Email Deliverability

### How Deliverability Actually Works

Deliverability is the ability to get emails into the inbox rather than the spam folder or blocked entirely. It's determined primarily by sender reputation, not content.

**The main signals inbox providers evaluate:**

| Signal | Weight | What it measures |
|---|---|---|
| Engagement rate | Very high | Do recipients open, click, reply, move to inbox? |
| Spam complaint rate | Very high | Do recipients mark as spam? Keep below 0.1% |
| Bounce rate | High | Are you sending to valid addresses? |
| Unsubscribe rate | Medium | Are subscribers unhappy enough to opt out? |
| Authentication (SPF/DKIM/DMARC) | High | Are you who you claim to be? |
| Sending consistency | Medium | Regular patterns vs. sudden large spikes |
| Domain/IP reputation | High | Historical reputation of your sending infrastructure |

### The Spam Word Myth

The idea that specific "spam words" (FREE, ACT NOW, LIMITED TIME) will cause emails to land in spam is largely outdated.

Modern inbox providers use machine-learning filters evaluating hundreds of signals. Engagement history is the dominant signal. A sender with strong engagement history can use almost any language. A sender with weak engagement will be filtered regardless of vocabulary.

Content does matter, but at the level of: does this look like a legitimate communication? Clean HTML, real domain links, working unsubscribe link, physical address, consistent from address. Not word-level paranoia.

**The reliable path to inbox placement:**
1. Clean, permission-based list
2. Proper SPF/DKIM/DMARC
3. Consistent sending cadence (don't go from 0 to 100k sends with no warmup)
4. Relevant content that drives genuine engagement
5. Suppress hard bounces, unsubscribes, and spam complaints immediately
6. Never buy lists

### Getting Out of the Spam Folder

If you're landing in spam:

1. Check authentication (SPF, DKIM, DMARC) first — misconfiguration is a common cause
2. Check your spam complaint rate in your ESP's report
3. Check your bounce rate — high hard bounces indicate list quality problems
4. Check your engagement — if open rates are very low, ISP's treat this as a reputation signal
5. Consider IP warming if you recently changed ESP or sending infrastructure
6. Check if your domain or IP is on a blocklist (use MXToolbox)
7. Reduce send volume to your most engaged subscribers only; gradually re-expand

### IP Warming

When you start sending from a new IP address (new ESP, new dedicated IP), inbox providers have no reputation history for it. Sudden large sends from an unknown IP are treated with suspicion.

IP warming = gradually increasing send volume over weeks, starting with small sends to your most engaged subscribers, to build positive reputation history before sending at full volume.

Most large ESP's handle this automatically on shared IPs. If you're on a dedicated IP, you need to manage this explicitly.

---

## Email Metrics: Complete Reference

### Core Sending Metrics

| Metric | Definition | Formula |
|---|---|---|
| Sent | Total emails attempted | — |
| Bounced | Emails not delivered | — |
| Delivered | Successfully delivered | Sent − Bounced |
| Delivery Rate | Delivered as % | (Delivered / Sent) × 100 |

**Bounce classification:**

- **Soft bounce:** Temporary issue. Address likely valid. Causes: full mailbox, out of office, server timeout. Do not suppress immediately; retry.
- **Hard bounce:** Permanent failure. Address invalid or non-existent. Suppress immediately and permanently.
- **Block bounce:** Receiving server rejected the email. Causes: failed authentication (SPF/DKIM), IP or domain on a blocklist. Indicates a deliverability infrastructure problem, not just a bad address.

**Important:** "Delivered" includes emails that landed in spam folders. Delivery rate flatters your actual inbox placement picture.

### Engagement Metrics

| Metric | Definition | Formula |
|---|---|---|
| Opens | Unique recipients who opened | — |
| Total Opens | All open events (non-unique) | — |
| Open Rate | Unique opens as % of delivered | (Opens / Delivered) × 100 |
| Clicks | Unique recipients who clicked any link | — |
| Total Clicks | All click events (non-unique) | — |
| Click Rate (CTR) | Unique clicks as % of delivered | (Clicks / Delivered) × 100 |
| Click-to-Open Rate (CTOR) | Clicks relative to openers | (Clicks / Opens) × 100 |

**CTOR is the better engagement metric.** It measures how well the email content performed given that someone opened it. Less susceptible to open rate noise.

### Health and Negative Metrics

| Metric | Definition | Formula |
|---|---|---|
| Unsubscribes | Recipients who opted out | — |
| Unsubscribe Rate | As % of delivered | (Unsubscribes / Delivered) × 100 |
| Spam Complaints | Marked as spam by recipient | — |
| Spam Rate | As % of delivered | (Spam / Delivered) × 100 |

**Critical:** Gmail does not report spam complaints to ESP's. All spam complaint rates are undercounts. Keep reported spam rate below 0.1%. If it's approaching this, investigate immediately.

A list with zero unsubscribes is suspicious, not healthy. Some churn is normal.

### Business Outcome Metrics

| Metric | Definition | Formula |
|---|---|---|
| Conversions | Unique business outcomes from the campaign | From analytics platform (not ESP) |
| Conversion Rate | As % of delivered | (Conversions / Delivered) × 100 |
| Revenue per Subscriber | Revenue efficiency of the send | Revenue / Delivered |

Conversions require additional technical setup (Google Analytics or similar, UTM parameters on links). They're the metrics that actually matter for business impact.

### The Open Rate Problem

**How opens are tracked:** Marketing emails contain a tracking pixel, a 1×1 transparent GIF uniquely generated per campaign and per recipient. When the email HTML is parsed and external images fetched, the pixel fires and an open is recorded.

**Why this is unreliable:**

- Recipients with images disabled → genuine opens not counted (false negatives)
- Corporate spam filters that pre-fetch all external resources → phantom opens and clicks recorded (false positives)
- Apple Mail Privacy Protection (iOS 15+) → pre-fetches all pixels regardless of whether the user actually opened the email
- Gmail → often prefetches and caches all pixels, regardless of real open behaviour
- Bots and security scanners → generate false opens and clicks

**Practical guidance:** Use open rates for trend analysis across time. Don't report them with false precision. Don't make significant strategic or statistical decisions based on small open rate differences.

---

## Gmail's Promotions Tab

The industry panicked when Gmail introduced tabbed inboxes in 2013. The panic was not warranted.

### What It Is

Gmail categorises incoming email into tabs: Primary, Social, Promotions, Updates, and Forums. The algorithm uses a combination of content signals, sender reputation, and user behaviour to categorise each email.

### The Actual Impact

Open rates dipped slightly after launch. Deliverability was not meaningfully harmed. The Promotions tab became a secondary inbox that users check when they're in a mode to browse offers.

**The case for embracing it:**
- Users who open Promotions tab emails are often in higher purchase intent mode
- Fewer spam complaints (users expect promotional content there; it's not a surprise)
- Competition is with other promotional emails, not personal/transactional email
- Easier to stand out with good subject lines than in a cluttered primary inbox

**The genuine challenges:**
- High competition for attention among many promotional emails
- Subject lines must work harder than in the primary tab
- Some subscribers never check it

### Practical Guidance

**On getting to Primary tab:** Ask subscribers to move your email in the welcome message ("Drag this to your Primary tab if you'd like to make sure you see our emails"). Don't build a strategy around it. Most won't act.

**Gmail Annotations:** Gmail allows senders to add preview cards in the Promotions tab showing deal price, expiration date, and an image. Visible before opening. High-value for ecommerce brands running time-limited promotions. Worth implementing.

**Key metric:** Use CTOR (click-to-open rate), not open rate, to evaluate Promotions tab performance. Someone who opens from the Promotions tab was motivated enough to choose it; whether they click is the real signal.

**What to avoid:** Don't try to trick the Gmail algorithm into routing to Primary. Keyword stuffing or formatting tricks that briefly work will be countered and may harm reputation. Focus on quality and engagement signals instead.

### Why It Categorises How It Does

Gmail's algorithm considers: keyword signals in content and subject line, sender reputation and history, previous engagement from this recipient with this sender, and formatting/visual signals (heavy image use, certain link patterns). It's not deterministic and not fully transparent. The best influence on tab placement is genuine engagement from real subscribers.

---

## MIME and Email Technical Structure

Understanding this helps diagnose deliverability and rendering issues.

### What MIME Is

Multipurpose Internet Mail Extensions. The standard that extends email beyond plain text to support HTML, images, video, attachments, and interactive content.

### Multipart Email (the Important Part for Practitioners)

Marketing emails are typically sent as `multipart/alternative` messages: a plain text version and an HTML version bundled together in the same email. The recipient's email client renders whichever it supports (always HTML in modern clients; plain text as fallback).

**Why this matters:**
- Clean multipart structure is a positive deliverability signal
- Accessibility: screen readers and some corporate environments use the plain text version
- Auto-generated plain text versions from ESP's are often poorly formatted (broken URLs, wall of text)
- Always write or review the plain text version of important campaigns

**Common MIME types in email:**

| MIME Type | Use |
|---|---|
| `text/plain` | Plain text version |
| `text/html` | HTML formatted version |
| `multipart/alternative` | Container holding both plain text and HTML versions |
| `multipart/mixed` | Container for emails with attachments |
| `multipart/related` | HTML with embedded (inline) images |
| `image/jpeg`, `image/png`, `image/gif` | Image attachments or embedded images |
| `text/x-amp-html` | AMP for Email content |

### AMP for Email

A Google-backed format enabling genuinely interactive email content: live carousels, in-email forms, real-time content updates. Uses `text/x-amp-html` MIME type.

**Support:** Gmail, Yahoo Mail, Mail.ru. Not Outlook, Apple Mail, or most other clients.
**Implementation:** Requires AMPHTML knowledge and strict validation. Emails are sent as `multipart/alternative` with AMP, HTML, and plain text versions; non-supporting clients receive the HTML fallback.
**Use cases:** Product carousels, in-email purchasing, live surveys, event RSVPs, dynamic content that updates post-send.
**Current status:** Interesting capability, not mainstream. Most email programmes don't need it yet. Worth flagging as a future direction for advanced senders.

### Deliverability Implications

- Broken HTML negatively affects deliverability
- Image-to-text ratio: emails that are primarily images with minimal text can trigger filters
- Executable attachments (`.exe`, `.js`, etc.) are near-universal spam filter triggers
- Proper multipart structure is a positive signal
