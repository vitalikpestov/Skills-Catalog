"""MCP prompts — reusable workflow templates discoverable by any MCP client."""


def lead_generation(website: str, segment: str = "") -> list[dict]:
    """Full lead-generation pipeline: scrape site, extract ICP, search Apollo, qualify, launch outreach."""
    seg = f" targeting the '{segment}' segment" if segment else ""
    return [{"role": "user", "content": (
        f"Run the full lead-generation pipeline for {website}{seg}.\n\n"
        "Steps:\n"
        "1. Scrape the website with scrape_website to understand their offer.\n"
        "2. Extract the ICP and value proposition from the scraped text.\n"
        "3. Use apollo_get_taxonomy to find matching industries and employee ranges.\n"
        "4. Run apollo_search_companies with the derived filters.\n"
        "5. Qualify the resulting companies against the ICP (target / maybe / skip).\n"
        "6. For target companies, run apollo_search_people to find decision-makers.\n"
        "7. Save all results to the project workspace.\n\n"
        "Present a summary with counts and next steps (email sequence or LinkedIn flow)."
    )}]


def classify_companies(icp: str) -> list[dict]:
    """Classify a list of companies as target or skip based on an ICP description."""
    return [{"role": "user", "content": (
        f"Classify companies against this ICP: {icp}\n\n"
        "For each company, assign: target or skip.\n"
        "Use via negativa rules — focus on excluding non-matches.\n\n"
        "Load the company list from the project workspace (companies.json), "
        "run blacklist_check on their domains, scrape each website, then classify. "
        "Save the classified results back to the project (versioned)."
    )}]


def classify_replies() -> list[dict]:
    """Categorize email campaign replies into actionable buckets."""
    return [{"role": "user", "content": (
        "Classify the latest campaign replies using the 3-tier funnel:\n"
        "- Tier 1 (FREE): regex patterns for OOO, unsubscribe, bounce\n"
        "- Tier 2 (FREE): fetch full thread, extract real reply text\n"
        "- Tier 3 (LLM): classify ambiguous replies\n\n"
        "Categories: interested, meeting_request, question, not_now, "
        "not_interested, wrong_person, out_of_office, unsubscribe, bounce.\n\n"
        "Load replies from SmartLead, classify each one, save results. "
        "For 'interested' and 'meeting_request' replies, draft follow-up messages."
    )}]


def generate_email_sequence(offer: str, icp: str) -> list[dict]:
    """Generate a cold-email sequence tailored to an offer and ICP."""
    return [{"role": "user", "content": (
        f"Write a cold-email sequence for this offer: {offer}\n"
        f"Target ICP: {icp}\n\n"
        "Follow the 12-rule GOD_SEQUENCE checklist:\n"
        "- 4-5 emails, spaced Day 0/3/7/14\n"
        "- ≤120 words per email\n"
        "- A/B subjects on Email 1\n"
        "- SmartLead variables: {{first_name}}, {{company_name}}, {{city}}, {{signature}}\n"
        "- <br> for line breaks, no em dashes\n\n"
        "Return the sequence as a list of steps with subject, subject_b, body, and day."
    )}]


def analyze_offer(website_text: str) -> list[dict]:
    """Extract the core offer, ICP, and differentiators from website copy."""
    return [{"role": "user", "content": (
        "Analyze this website text and extract:\n\n"
        "1. **Core offer**: What product or service is being sold?\n"
        "2. **Target ICP**: Who is the ideal customer? (industry, size, role)\n"
        "3. **Key differentiators**: What makes this offer unique?\n"
        "4. **Pain points addressed**: What problems does it solve?\n"
        "5. **Suggested Apollo filters**: industry tags, employee ranges, keywords.\n"
        "6. **Exclusion rules**: What companies are NOT targets?\n\n"
        f"Website text:\n---\n{website_text}\n---\n\n"
        "Return a structured summary that can feed directly into /launch."
    )}]
