---
name: email-marketing/list-building
description: >
  List building strategy covering lead generation forms, form placement tactics,
  lead magnets, single vs double opt-in, and subscriber source tracking. Reference
  this when advising on growing an email list, form design, or attribution.
---

# List Building

## Lead Generation Forms: Best Practices

**Build forms in your ESP where possible.** This eliminates the data plumbing problem: when someone submits a form, the data needs to get to your ESP. Building natively removes this failure point.

**The six essentials of a good form:**

1. **Clear value proposition headline.** What specifically is the subscriber getting? "Shop the sale first" is excellent. "Sign up for our newsletter" is not.
2. **Right expectations.** How often will you email? What kind of content? Removes uncertainty and reduces future spam complaints.
3. **Clear, action-oriented CTA.** "Subscribe" works. Specific is better: "Get the guide", "Join 5,000 readers".
4. **Clear field labels.** Never rely on placeholder text alone as a label.
5. **Minimal fields.** An email address is all that's strictly necessary. Each additional field reduces conversion rate. Only add friction intentionally (e.g., qualifying leads).
6. **Privacy assurance.** A brief, honest, human line about how you'll use their data. Not legal boilerplate.

**Field count guidance:** Above 3 fields, conversion rate starts dropping noticeably. Above 5 fields, you're qualifying leads, not collecting subscribers. Be intentional about which mode you're in.

**Always test on mobile.** Mobile traffic is significant. ESP-built forms are usually responsive but verify.

## Form Placement and Tactics

In order of typical conversion rate (higher = more intrusive, higher conversion):

1. **Permission priming overlays** — Full-screen prompts. Most effective, most intrusive. Use carefully.
2. **Exit intent popups** — Triggered when cursor moves to close/address bar. Catches departing visitors.
3. **Timed/scroll-triggered popups** — Appear after X seconds, X pages visited, or X% scroll depth. Good balance of visibility and UX.
4. **Immediately-firing popups** — Show on landing. High visibility, potentially high annoyance. Test carefully.
5. **Full-width sticky banner (HelloBar-style)** — Persistent top-of-page bar. Good visibility, lower friction than popups.
6. **In-content embedded forms** — Inside blog posts, product pages. Lower visibility, lower friction.
7. **Footer/sidebar embedded forms** — Low visibility but always present.

**Off-site channels:**
- Link-in-bio tools (for Instagram/TikTok-first audiences)
- Meta lead generation ads
- Video callouts (YouTube, etc.)
- QR codes on print/events (link to a tracked landing page)

Always run multiple placements simultaneously. Don't rely on a single form in a single location.

## Lead Magnets

**Definition:** An incentive offered in exchange for an email address or contact details.

**Common types:** Ebooks, whitepapers, templates, tools/calculators, quizzes, exclusive data/research, discount codes, free trials, on-demand demos, free courses/lessons.

**Three criteria for a good lead magnet:**
- **Relevant** — Attracts your actual target customer profile, not just anyone with an email address
- **Useful** — Solves a real problem or delivers genuine value
- **Valuable** — Not easily available elsewhere for free; worth the "price" of an email address

**Trap to avoid:** Discount code lead magnets inflate signup numbers but attract deal-seekers who churn immediately or provide throwaway email addresses. Optimise for subscriber quality, not signup volume.

**Non-negotiable:** Deliver on the lead magnet promise in the first email. Failure here erodes trust before the relationship has started.

## Single vs Double Opt-In

**Single opt-in:** Added to list immediately on form submission.
- Pros: Higher signup rate, no confirmation friction
- Cons: Invalid addresses get through, bounce risk higher, consent record weaker

**Double opt-in (confirmed opt-in):** Must click a confirmation link in an automated follow-up email before being added to the active list.
- Pros: Verified real addresses, cleaner list, stronger consent evidence, lower bounce rate, fewer spam complaints
- Cons: Some signups lost to confirmation drop-off; requires proper confirmation email design

**Confirmation link expiration:** Set to 24–48 hours. Send a single reminder email before expiry.

**Decision guidance:**

| Priority | Recommendation |
|---|---|
| List quality and deliverability | Double opt-in |
| GDPR-regulated jurisdiction | Double opt-in (safest for consent records) |
| Volume growth, market where single opt-in is norm | Single opt-in (with strong bounce management) |
| Ecommerce with incentivised sign-ups | Single opt-in with careful bounce suppression |

## Tracking Subscriber Sources

Knowing where subscribers come from is as valuable as knowing how many you have. A subscriber from organic search who read three articles before signing up is very different from one who clicked a paid ad popup.

**Methods:**

| Method | How | Best For |
|---|---|---|
| UTM parameters | Append `?utm_source=X&utm_medium=Y&utm_campaign=Z` to sign-up URLs | Cross-channel campaign tracking |
| Dedicated landing pages | Unique URL per source (`/signup-podcast`) | Clean attribution without URL complexity |
| Hidden form fields | `<input type="hidden" name="source" value="blog-sidebar">` | Granular placement tracking within a site |
| Custom ESP fields | Store source data on subscriber profile | Segmentation, personalised welcome emails |
| QR codes | Link to tracked landing page | Offline-to-online attribution |

**Critical practice:** Use consistent naming conventions for UTM parameters from day one. Inconsistency makes the data useless within months.

**Combine methods.** Attribution in marketing is always incomplete. Incomplete is still better than blind.
