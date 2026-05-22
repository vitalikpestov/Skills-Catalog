# Targeting & Audiences Reference

## The 2025 Targeting Paradigm Shift

The biggest shift in Meta advertising: **manual audience selection is becoming obsolete for performance campaigns.** Meta's Andromeda architecture processes billions of candidate ads per second using deep learning, making AI-driven targeting superior to hand-picked audiences in most cases.

Key insight: Your ad creative now does what interests and demographics used to. The creative naturally attracts your ideal customer and filters out everyone else.

## Audience Types

### 1. Core Audiences (Manual/Demographic Targeting)
Build targeting from scratch using platform data:
- **Demographics:** Age, gender, relationship status, education, language
- **Location:** Country, state, city, postal code, radius
- **Interests:** Meta's predefined buckets (e.g., "B2B Software", "Wellness", "Luxury Travel")
- **Behaviors:** Purchase patterns, device usage, travel habits

**When to use:**
- Early-stage startups with no CRM data
- Testing positioning for different personas
- Highly niche products where broad targeting is too diffuse
- Top-of-funnel awareness seeding

**Important 2025 changes:**
- Meta has removed many detailed targeting categories (especially niche fandoms, local scenes, cultural affinities)
- Interests are now broader, less specific than before
- June 2025: Major changes merged/removed many specific interest tags
- Keywords like "Vegan Fitness" or "Vintage Sci-Fi Films" may no longer exist

### 2. Custom Audiences (Retargeting)
Target people who have already interacted with your brand:

- **Website visitors** (via Pixel): Page visitors, specific page visitors, time on site, events fired
- **App users:** Specific in-app actions (add to cart, level completed)
- **Customer list:** Upload emails/phone numbers, Meta matches to profiles
- **Engagement-based:** Video viewers, post engagers, page followers, Instagram profile visitors, lead form openers
- **Offline activity:** In-store purchases, phone calls (now via standard CAPI since Offline API discontinued May 2025)

**Retargeting windows:**
- Website visitors: Use 180 days (Meta auto-prioritizes recent interactions)
- Video viewers/engagers: Use 365 days
- Don't narrow windows manually — let Meta handle recency

**Best practices:**
- High conversion potential at much lower CPL than cold traffic
- Enables multi-touch nurturing through sequential ads
- Separate retargeting may be unnecessary in 2025 — combining warm+cold in one ad set often works better

### 3. Lookalike Audiences
Meta's ML identifies new people resembling your best customers:

- **Seed source:** Custom audience (buyers, subscribers, high-value customers)
- **Size:** 1% (most similar) to 10% (broadest)
- **Recommendation:** Start with 1%, test larger percentages
- **Best seed:** Top 5% customers by value (value-based lookalike)

**2025 status:**
- Still useful but less essential than before
- Meta now creates "lookalike-style" expansions automatically with Advantage+ Audience
- Use traditional LALs when you need precise control (lead gen, new markets, smaller countries with 5-10%)
- Don't spin up 10 ad sets with one interest each — overlap kills validity

### 4. Advantage+ Audience (AI-Driven)
Meta's most automated targeting option:

- You provide optional "suggestions" (interests, demographics) — these are starting points, not constraints
- Algorithm uses pixel data, past conversions, real-time engagement signals to find best audience
- Dynamically expands beyond suggestions if better opportunities detected
- Results: 13% lower cost per catalog sale, 7% lower cost per website conversion, 28% lower CPC

**When to use:**
- When you have strong conversion events set up
- When your pixel has accumulated sufficient data
- For broad prospecting at scale
- When you want to let Meta's AI do the work

**When NOT to use:**
- Brand new accounts with zero conversion history
- Hyper-niche B2B targeting
- When you need strict geographic or demographic controls

## Targeting Strategy Recommendations

### For New Accounts (Little/No Data)
1. Start with a few interest or lookalike layers to help the algorithm learn
2. Use modest budget, broad audience, focus on gathering initial conversion events
3. Once you have 50+ conversions, switch to Advantage+ Audience
4. Think of it as "seeding" the algorithm

### For Established Accounts
1. **Primary campaign:** Broad/Advantage+ targeting for conversions
2. **Secondary:** Interest-based testing for awareness and data collection
3. **Retargeting:** Either combined in main campaign or separate for specific offers
4. Use Custom Audiences from main campaign (video viewers, engagers) to seed retargeting

### The Combined Audience Approach (2025 Best Practice)
Combine warm and cold audiences in the same ad set:
- Include warm audiences (site visitors, engagers, email subscribers)
- Include cold audiences (broad or interest-based)
- Algorithm prioritizes high-intent users first, then expands
- Often outperforms separated funnel stages

### Exclusions
- **Generally don't exclude existing customers** — they bring repeat purchases and social proof
- **Exclude when:** Offer sensitivity (first-time buyer discount), specific customer experience requirements
- Use exclusion lists sparingly — they limit the algorithm's ability to optimize

## Audience Sizing Guidelines

- **Sweet spot for broad campaigns:** 1-5 million people
- **Minimum for algorithm learning:** ~100,000 (smaller audiences starve the algorithm)
- **For smaller countries (e.g., Italy):** Use broader targeting, larger LAL percentages (3-10%)
- **Don't micro-segment:** Overlap between ad sets wastes budget and confuses the algorithm

## Testing Framework

1. **Aim for 50-100 conversions per week per ad set**
2. **Let tests run 7-10 days** or until 3-4 conversions per ad
3. **Don't A/B test interests across multiple ad sets** — causes overlap and slows learning
4. **Test the right thing at the right time:** audience first, then creative, then copy
5. **Clean inputs drive clean results:** Wrong tracking invalidates all testing

## Special Ad Categories & Targeting Restrictions

Housing, Employment, Credit, Health/Wellness, and Political/Social Issue ads have restricted targeting:
- Cannot target by age, gender, or zip code in some categories
- Limited interest targeting
- Requires additional verification and documentation
- Health and wellness brands may lose access to Purchase/Add to Cart optimization events (since January 2025)

## Key Metrics for Targeting Health

| Metric | Healthy Range | Action if Outside |
|---|---|---|
| Frequency | 1.5 - 3.0 | >3.0 = refresh creatives or broaden audience |
| CPM | Varies by vertical | Rising = audience saturation, broaden |
| CTR | >1% for Feed | <1% = creative or targeting issue |
| Audience overlap | <20% between ad sets | Consolidate overlapping ad sets |
| Learning phase spend | <20% of total | Consolidate ad sets for faster learning |
