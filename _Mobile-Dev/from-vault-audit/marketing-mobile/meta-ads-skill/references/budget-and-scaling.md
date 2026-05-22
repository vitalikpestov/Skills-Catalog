# Budget & Scaling Reference

## CBO vs ABO

### CBO (Campaign Budget Optimization) = "Advantage Campaign Budget"
- Set ONE budget at the campaign level
- Meta's AI distributes across ad sets based on predicted performance
- Real-time algorithmic optimization hour-by-hour
- The 80/20 rule applies: ~20% of ad sets get ~80% of spend

**Strengths:**
- Consistent results through holistic data approach
- Efficient scaling with automated budget allocation
- Faster learning phase (pools data across ad sets)
- Frees time for creative and strategy work
- Meta internal data (April 2025): 17% ROAS increase within 6 weeks

**Weaknesses:**
- Loss of granular control
- Algorithm bias toward high-volume audiences (may neglect niche segments)
- Budget "starvation" for new/smaller ad sets
- Unpredictable allocation
- Makes fair A/B testing difficult

**Use CBO when:**
- Scaling proven campaigns
- Running evergreen/ongoing campaigns
- Full-funnel strategies with similar audience sizes
- Broad targeting paired with Advantage+
- You have 50+ conversions/week

### ABO (Ad Set Budget Optimization)
- Set FIXED budget for each ad set individually
- Each ad set spends its allocation regardless of performance
- Manual control over distribution

**Strengths:**
- 100% control over budget allocation
- Fair, scientific A/B testing (equal spend per variant)
- Better for small budgets (focus entire budget on one ad set)
- Isolated learning per ad set
- Can turn ad sets on/off without disrupting others

**Weaknesses:**
- Requires constant manual monitoring
- Winning ad sets can't automatically get more budget
- Slower optimization at campaign level
- More time-intensive management

**Use ABO when:**
- Testing new creatives, audiences, or copy angles
- Niche B2B campaigns with lower conversion volumes
- Small budgets needing precise allocation
- Newer accounts with little historical data
- You need isolated, reliable test data

### The Hybrid Approach (Recommended)

Most top media buyers use both:

1. **ABO for testing:** Equal budget per ad set, isolate variables, gather clean data
2. **CBO for scaling:** Move proven winners into CBO campaign, let algorithm optimize
3. **Post ID duplication:** When moving ads from ABO to CBO, use the same post ID to carry social proof (likes, comments, shares)

**Structure:**
- Testing Campaign (ABO or CBO): 30% of budget
- Scale Campaign (CBO): 70% of budget
- Optional: Cost Cap campaign for efficiency at scale

## Budget Allocation Guidelines

### Minimum Budgets
- To exit learning phase: Need ~50 optimization events per ad set per week
- Rule of thumb: Daily budget ≥ 2-3x your target CPA
- For a €20 CPA target: minimum ~€40-60/day per ad set

### Budget Distribution by Stage
- **Testing:** 20-30% of total ad budget
- **Scaling winners:** 60-70%
- **Retargeting:** 10-20% (less if using combined audiences)

### Budget by Business Size
| Monthly Budget | Recommended Structure |
|---|---|
| €500-1,500 | 1 CBO campaign, 2-3 ad sets, focus on one objective |
| €1,500-5,000 | Testing (ABO) + Scale (CBO), 2 campaigns |
| €5,000-20,000 | Testing + Scale + Retargeting, 3-4 campaigns |
| €20,000+ | Full funnel, multiple objective campaigns, cost cap testing |

## Scaling Strategies

### Vertical Scaling (Budget Increases)
- Increase budget by **10-20% every 2-3 days**
- Larger jumps (>20%) can reset the learning phase
- Monitor CPA and ROAS after each increase
- If CPA rises >20%, pause and let it stabilize
- Works best with CBO

### Horizontal Scaling (Adding New Elements)
- Duplicate winning campaigns with one variable changed:
  - New audience segment
  - New creative angle
  - New placement emphasis
- Avoids disrupting performing campaign
- Test in isolation, then consolidate

### Scaling Framework for Different Sizes

**Small brands (starting out):**
1. Find 1-2 winning creatives via CBO testing
2. Scale budget slowly (10-20% every few days)
3. Once stable, add new creative variations
4. Focus on one objective (usually Sales or Leads)

**Medium brands (€50-500/day):**
1. ABO testing with 3-5 creative concepts weekly
2. Move winners to CBO scale campaign
3. Test 3-5 new creatives per week
4. Horizontal scale: new lookalikes, new interest stacks
5. Refresh creatives every 2-4 weeks

**Large brands (€500+/day):**
1. High-volume creative testing (5-10 concepts/week)
2. Cost cap campaigns for efficient scaling
3. Multiple CBO campaigns for different objectives/funnels
4. Clone and reset when campaigns peak
5. Track campaign-level CPA, ROAS, and frequency

## The Learning Phase

### What It Is
- Period when Meta's algorithm gathers enough data to optimize delivery
- Needs ~50 optimization events per ad set per week
- Typically lasts 3-7 days
- Performance may be volatile during this phase

### What Triggers a Learning Phase Reset
- Budget changes >20%
- Audience targeting changes
- Creative changes (adding/removing ads)
- Optimization event changes
- Bid strategy changes
- 7+ day pause

### "Learning Limited" Status
Means the ad set isn't getting enough optimization events. Solutions:
1. Broaden targeting (wider audience)
2. Increase budget
3. Combine ad sets (consolidate)
4. Use a higher-funnel optimization event (e.g., Add to Cart instead of Purchase)
5. Improve creative to increase conversion rate

### Best Practice
- Keep <20% of total spend in the learning phase
- Advertisers who achieve this lower cost per purchase by up to 68%
- Make changes in batches rather than incrementally
- Wait for learning phase to complete before evaluating

## Bid Strategies

### Lowest Cost (Default)
- Meta gets you the most results for your budget
- No bid control
- Best for: Most campaigns, especially when starting out

### Cost Cap
- Set a target cost per result
- Meta aims to stay at or below your cap
- May under-deliver if cap is too low
- Best for: Mature accounts with clear CPA targets
- Good for scaling efficiently at large budgets

### Bid Cap
- Hard ceiling on per-auction bid
- Most restrictive — can severely limit delivery
- Best for: Advanced buyers with specific ROI requirements

### Minimum ROAS
- Set minimum return on ad spend target
- Meta only serves ads expected to meet or exceed target
- Best for: E-commerce with clear margin requirements

### Value Optimization
- Maximize total purchase value (not just volume)
- Requires sending purchase values via Pixel/CAPI
- Best for: Businesses with variable order values

## Key Metrics to Monitor

### Primary KPIs (Check Daily)
| Metric | What It Tells You |
|---|---|
| ROAS | Revenue generated per ad dollar spent |
| CPA / CPL | Cost per acquisition or lead |
| Conversion Rate | % of clickers who convert |
| Total Conversions | Volume of desired actions |

### Health Metrics (Check 2-3x/week)
| Metric | Healthy Range | Action |
|---|---|---|
| Frequency | 1.5-3.0 | >3.0 = creative fatigue, refresh |
| CPM | Varies by vertical | Rising = audience saturation |
| CTR | >1% Feed | <1% = creative or targeting issue |
| Hook Rate | >25% | <25% = weak opening |
| Learning phase spend | <20% of total | >20% = consolidate |

### Target Benchmarks (Approximate)
- **E-commerce ROAS:** 2.5x-4.0x is healthy
- **Lead gen CPL:** Varies hugely by industry (€5-50+)
- **Average Facebook CPM (2025):** €8-15 (varies by vertical and season)
- **Click-through rate:** 1-2% is average; >2% is strong

## Automation Rules

Set up automated rules to save 10-20 hours/week:

1. **Kill underperformers:** Pause ad sets exceeding target CPA by 20%+ after minimum spend threshold
2. **Scale winners:** Increase budget by 15% when ROAS exceeds target for 3 consecutive days
3. **Fatigue detection:** Alert when frequency exceeds 3.0 (rotate in fresh creative)
4. **Weekend reduction:** Lower budgets by 20-30% on weekends for B2B campaigns
5. **Budget protection:** Daily spending limit notifications

**Important:** Automation rules only work well with accurate tracking. Fix tracking first, then automate.
