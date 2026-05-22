# Tracking & Measurement Reference

## The Dual Tracking Setup (Mandatory in 2025)

**Meta Pixel + Conversions API (CAPI) together** is the recommended setup. Neither alone is sufficient.

### Meta Pixel (Client-Side)
- JavaScript code on your website
- Fires when user takes actions (page view, add to cart, purchase)
- Captures real-time browser events and behavior signals
- **Limitations:** Blocked by ad blockers, iOS privacy (ATT), cookie restrictions, browser ITP
- Meta's 2025 data: Over 50% of browser-side conversions go untracked due to privacy restrictions
- **Setup:** Business Manager → Events Manager → Add Data Source → Facebook Pixel

### Conversions API / CAPI (Server-Side)
- Server-to-server tracking: sends event data directly from your server to Meta
- Bypasses browser restrictions, ad blockers, iOS privacy limits
- Can track offline conversions, delayed events, cross-device behavior
- More durable and accurate
- Recovers 20-30% of lost conversion data
- **Setup methods:**
  - Platform native integrations (Shopify, WordPress — often free)
  - CAPI Gateway (~$10-400+/month hosting)
  - Server-side GTM ($10-50/month)
  - Manual/Direct API implementation ($500-5000+ developer time)

### Why Use Both Together
- Dual path for event delivery — if one fails, other acts as backup
- Meta deduplicates data (won't count twice) using matching `event_id` values
- Most complete, future-proof setup available
- Significantly improves Event Match Quality (EMQ)
- Algorithm optimizes better with complete data → better ROAS

## Event Match Quality (EMQ)
- Score from 0 to 10 assigned to each conversion event
- Measures how well Meta matches server events to Facebook user profiles
- **Target: EMQ score above 8.0** for optimal ad delivery
- Improve by sending hashed user identifiers: email, phone, first name, last name, city, state, zip, country, external ID
- Higher EMQ = better attribution = better ad delivery = lower costs

## Standard Events

Key events to configure (in order of typical funnel priority):

| Event | Description | Usage |
|---|---|---|
| PageView | Page loaded | Basic tracking, retargeting |
| ViewContent | Product/content page viewed | Retargeting, optimization |
| AddToCart | Item added to cart | Mid-funnel optimization |
| InitiateCheckout | Checkout started | High-intent retargeting |
| Purchase | Transaction completed | Primary conversion event |
| Lead | Form submitted, signup | Lead gen optimization |
| CompleteRegistration | Registration completed | Signup tracking |
| Contact | Contact initiated | Service business tracking |
| Schedule | Appointment scheduled | Service business tracking |
| Search | Search performed | Intent signal |

**Value-Based Optimization:** Send actual order value (or customer LTV) with conversion events via CAPI. This teaches Meta which conversions matter most for revenue, moving beyond simple volume optimization.

## Event Deduplication

When running both Pixel and CAPI, events can be sent twice. Deduplication prevents double-counting:

1. Generate a unique `event_id` for each user action
2. Send the same `event_id` via both Pixel and CAPI
3. Meta matches events by `event_id` and keeps only one

**Critical:** Without deduplication, your reported conversions will be inflated and optimization will suffer.

## The fbclid Parameter

When user clicks a Meta ad, the URL contains an `fbclid` parameter:
- **Capture and store** this value with the contact record in your CRM at time of form submission
- When sending CRM conversion events through CAPI later, include the stored `fbc` value in `user_data`
- Without this, Meta cannot attribute downstream conversions (that happen days/weeks later) to the original ad click
- Essential for lead gen businesses with longer sales cycles

## Offline Conversions API — Discontinued

- **Permanently discontinued May 2025**
- All offline conversion tracking (in-store purchases, phone conversions, CRM events) now flows through standard Conversions API
- Migration issues reported: some advertisers saw up to 70% drop in accepted events
- Common migration fix: ensure parameters are correctly formatted, don't hash fbp/fbc values, verify event_time within 7-day window
- Third-party tools (Zapier, Segment) have updated connectors for standard CAPI
- In Zapier: select "Physical Store" as Action Source for offline events

## Attribution & Measurement

### Attribution Windows
- Default: 7-day click, 1-day view
- Can be configured per ad set
- "First Conversion" vs "All Conversions":
  - First Conversion: better for new customer acquisition
  - All Conversions: better for total revenue tracking and retargeting

### Incremental Attribution (April 2025)
- New metric showing true ad lift
- Reports 20%+ improvement in measuring real conversion impact
- Moves toward incrementality-based measurement as core model

### Value Rules (June 2025)
- Adjust bids for specific audience segments
- Based on placement, age, gender, location, or device
- **Caution:** Meta warns costs may increase 20-1000% if used incorrectly
- Test at small scale first

### Key Measurement Tools

**Events Manager:**
- Monitor event firing, diagnose issues
- View server event details
- Check EMQ scores
- Test server events
- Diagnostics tab for troubleshooting

**Ads Manager Reporting:**
- Campaign, ad set, and ad level metrics
- Custom columns for specific KPIs
- Breakdown by placement, device, demographic

**Meta Experiments:**
- A/B testing built into Ads Manager
- Holdout tests for incrementality
- Conversion lift studies

### Privacy-Safe Measurement
- Aggregated Event Measurement (AEM) for iOS 14.5+ events
- Private Lift for measuring ad impact without sharing individual data
- Conversions API for reliable server-side tracking
- First-party data strategies increasingly important

## Common Tracking Issues & Fixes

| Issue | Cause | Fix |
|---|---|---|
| Events not showing | Pixel not installed correctly | Use Meta Pixel Helper browser extension to verify |
| Low EMQ score | Missing customer parameters | Send more hashed identifiers via CAPI |
| Duplicate events | No deduplication | Implement matching event_id in Pixel + CAPI |
| Attribution gaps | CAPI not configured | Set up server-side tracking |
| Events delayed >7 days | Outside acceptance window | Send events within 7 days of occurrence |
| "Learning Limited" | Insufficient conversion volume | Broaden targeting, increase budget, or use higher-funnel event |
| Health/wellness restrictions | Category classification | Check Events Manager, appeal if misclassified |

## Diagnostics Checklist

Before launching any campaign, verify:
1. ✅ Pixel fires correctly on all key pages (use Pixel Helper)
2. ✅ CAPI is configured and sending events
3. ✅ Event deduplication is working (check for duplicate events in Events Manager)
4. ✅ EMQ score is 6+ (ideally 8+)
5. ✅ Standard events mapped to your conversion funnel
6. ✅ Domain verification completed
7. ✅ Aggregated Event Measurement configured (for iOS)
8. ✅ UTM parameters set up for cross-channel attribution
