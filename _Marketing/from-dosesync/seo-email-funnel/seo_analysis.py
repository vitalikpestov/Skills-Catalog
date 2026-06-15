import anthropic
from typing import Dict

WORD_TARGETS = {"short": 800, "medium": 1500, "long": 2500}

PERSONA_LABELS = {
    "sandwich_caregiver": "sandwich generation caregiver (caring for both aging parents and children)",
    "young_parent": "young parent managing a child's medication",
    "grandparent": "grandparent helping with grandchildren's medications",
    "professional_caregiver": "professional caregiver or home nurse",
    "other": "family caregiver",
}

CLUSTER_CONTEXT = {
    "double_dosing": "double-dosing accidents, missed doses, coordination errors between family members",
    "grandparents": "grandparents joining family medication coordination, tech-friendly onboarding",
    "adhd_kids": "ADHD medication schedules, school-home handoffs, caregiver coordination for kids",
    "burnout": "caregiver burnout from manual tracking, anxiety about medication errors",
    "other": "family medication coordination and tracking",
}


def build_seo_outline(
    raw_question: str,
    topic_cluster: str,
    persona_segment: str,
    language: str,
    model: str = "claude-sonnet-4-6",
    article_length: str = "medium",
) -> Dict:
    client = anthropic.Anthropic()

    persona_desc = PERSONA_LABELS.get(persona_segment, "family caregiver")
    cluster_desc = CLUSTER_CONTEXT.get(topic_cluster, "medication coordination")
    word_target = WORD_TARGETS.get(article_length, 1500)
    lang_instruction = "Respond in Russian." if language == "ru" else "Respond in English."

    prompt = f"""{lang_instruction}

You are an SEO content strategist specializing in health technology and family caregiving.

TASK: Build a complete SEO outline for a blog article answering this question:
"{raw_question}"

Context:
- Target persona: {persona_desc}
- Topic cluster: {cluster_desc}
- Target length: ~{word_target} words
- Product: DoseSync (family medication coordination app, NOT a medical advice tool)
- NEVER claim DoseSync provides medical advice, diagnoses, or clinical outcomes

Return a JSON object with this exact structure:
{{
  "seo_title": "compelling H1 title with primary keyword, under 60 chars",
  "meta_description": "155-char meta description, includes primary keyword, has CTA",
  "primary_keyword": "main keyword phrase (2-4 words)",
  "secondary_keywords": ["keyword2", "keyword3", "keyword4", "keyword5"],
  "search_intent": "informational|navigational|commercial|transactional",
  "heading_outline": [
    {{"level": "h2", "title": "...", "summary": "what this section covers in 1 sentence"}},
    ...
  ],
  "internal_link_anchors": ["anchor text 1", "anchor text 2"],
  "faq_questions": ["FAQ Q1?", "FAQ Q2?", "FAQ Q3?"]
}}

Requirements:
- 5-7 H2 sections minimum
- Include an FAQ section at the end (at least 3 questions)
- Primary keyword must appear naturally in title, first H2, and meta description
- Headings should follow informational → practical → CTA progression
- Last section should naturally mention DoseSync as a solution (not a pitch)

Return ONLY the JSON object, no markdown fences, no extra text."""

    message = client.messages.create(
        model=model,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    raw = message.content[0].text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    outline = json.loads(raw)
    outline.setdefault("language", language)
    outline.setdefault("article_length", article_length)
    outline.setdefault("word_target", word_target)
    return outline
