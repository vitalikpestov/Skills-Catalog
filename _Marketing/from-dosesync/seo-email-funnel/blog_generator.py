import anthropic
from typing import Dict
from guardrails import get_disclaimer, apply_guardrails


INTEGRATION_INSTRUCTIONS = {
    "light": "Mention DoseSync once naturally in the conclusion as one possible solution. No product pitch.",
    "medium": (
        "Reference DoseSync 2-3 times: once as a solution example in the body, "
        "once in a specific tip, once in the conclusion with a soft CTA."
    ),
    "strong": (
        "Weave DoseSync throughout: open with a relatable DoseSync scenario, "
        "use it as the primary example in 2-3 sections, and close with a clear "
        "'Try DoseSync free for 7 days' CTA."
    ),
}


def generate_blog_post(
    question,
    seo_outline: Dict,
    interview_blocks: Dict,
    config,
) -> Dict:
    client = anthropic.Anthropic()

    lang_instruction = "Write in Russian. Use 'Вы'-form (formal you). Keep all headings in Russian." if question.language == "ru" else "Write in English."
    integration_hint = INTEGRATION_INSTRUCTIONS.get(config.product_integration_level, INTEGRATION_INSTRUCTIONS["medium"])
    word_target = seo_outline.get("word_target", 1500)
    disclaimer = get_disclaimer(question.language)

    interview_summary = _format_interview_for_prompt(interview_blocks)

    heading_block = "\n".join(
        f"- {h['level'].upper()}: {h['title']} — {h['summary']}"
        for h in seo_outline.get("heading_outline", [])
    )

    faq_block = "\n".join(f"- {q}" for q in seo_outline.get("faq_questions", []))

    prompt = f"""{lang_instruction}

You are a senior health tech content writer. Write a complete, engaging SEO blog article.

ARTICLE SPECS:
- Title: {seo_outline['seo_title']}
- Meta description: {seo_outline['meta_description']}
- Primary keyword: {seo_outline['primary_keyword']}
- Secondary keywords: {', '.join(seo_outline.get('secondary_keywords', []))}
- Target length: ~{word_target} words
- Search intent: {seo_outline.get('search_intent', 'informational')}

REQUIRED SECTIONS (use these headings):
{heading_block}

FAQ QUESTIONS TO INCLUDE:
{faq_block}

CONTENT MATERIAL FROM INTERVIEW:
{interview_summary}

PRODUCT INTEGRATION RULE:
{integration_hint}
Product: DoseSync — family medication coordination app (iOS). Core features: shared dose log, real-time sync between caregivers, double-dose protection, push reminders, grandparent-friendly mode.

WRITING RULES:
1. Open with the pain story — make it vivid and specific (1-2 paragraphs)
2. Use the primary keyword in first 100 words
3. Each H2 section: 150-300 words
4. Include at least 2 quotes from interview material (or compose realistic composites)
5. Bullet lists for tips/mistakes — max 5 items per list
6. FAQ section at end in H2 + H3 structure
7. Conclusion with a single soft CTA (no hard sell)
8. NEVER claim DoseSync provides medical advice or clinical outcomes
9. NEVER include specific drug names
10. End with this exact disclaimer line: {disclaimer.strip()}

OUTPUT FORMAT: Pure markdown. Start directly with # title. No preamble or meta-commentary."""

    message = client.messages.create(
        model=config.model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )

    content_markdown = message.content[0].text.strip()
    content_markdown = apply_guardrails(content_markdown, question.language)

    return {
        "id": question.id,
        "seo_title": seo_outline["seo_title"],
        "meta_description": seo_outline["meta_description"],
        "primary_keyword": seo_outline["primary_keyword"],
        "secondary_keywords": seo_outline.get("secondary_keywords", []),
        "heading_outline": seo_outline.get("heading_outline", []),
        "content_markdown": content_markdown,
        "internal_links": seo_outline.get("internal_link_anchors", []),
        "language": question.language,
        "word_count": len(content_markdown.split()),
    }


def _format_interview_for_prompt(blocks: Dict) -> str:
    lines = []

    if blocks.get("pain_story"):
        lines.append(f"PAIN STORY:\n{blocks['pain_story']}")

    if blocks.get("key_insight"):
        lines.append(f"KEY INSIGHT:\n{blocks['key_insight']}")

    if blocks.get("mistakes"):
        lines.append("COMMON MISTAKES:")
        for m in blocks["mistakes"][:4]:
            lines.append(f"  - {m.get('mistake', '')} → {m.get('consequence', '')}")

    if blocks.get("solutions"):
        lines.append("PRACTICAL SOLUTIONS:")
        for s in blocks["solutions"][:5]:
            lines.append(f"  - {s.get('tip', '')}: {s.get('detail', '')}")

    if blocks.get("quotes"):
        lines.append("USABLE QUOTES:")
        for q in blocks["quotes"][:4]:
            lines.append(f'  "{q}"')

    if blocks.get("stats"):
        lines.append("STATS/NUMBERS:")
        for st in blocks["stats"][:3]:
            lines.append(f"  - {st.get('claim', '')} ({st.get('context', '')})")

    if blocks.get("emotional_peaks"):
        lines.append("EMOTIONAL MOMENTS:")
        for ep in blocks["emotional_peaks"][:3]:
            lines.append(f"  - [{ep.get('emotion', '')}] {ep.get('moment', '')}")

    return "\n".join(lines)
