import anthropic
import json
from typing import Dict

MAGNET_TYPES = {
    "double_dosing": ("checklist", "Double-Dose Prevention Checklist"),
    "grandparents":  ("guide",     "Grandparent Caregiver Quick-Start Guide"),
    "adhd_kids":     ("template",  "ADHD Medication Schedule Template"),
    "burnout":       ("framework", "Caregiver Burnout Prevention Framework"),
    "other":         ("checklist", "Family Medication Coordination Checklist"),
}


def generate_lead_magnet(
    question,
    seo_outline: Dict,
    interview_blocks: Dict,
    config,
) -> Dict:
    client = anthropic.Anthropic()

    magnet_type, magnet_title_hint = MAGNET_TYPES.get(
        question.topic_cluster, MAGNET_TYPES["other"]
    )

    lang_instruction = (
        "Write in Russian. Use 'Вы'-form." if question.language == "ru"
        else "Write in English."
    )

    key_insight = interview_blocks.get("key_insight", "")
    solutions = interview_blocks.get("solutions", [])
    solution_summary = "\n".join(
        f"- {s.get('tip', '')}" for s in solutions[:5]
    )

    prompt = f"""{lang_instruction}

You are a lead magnet strategist for a family caregiving app (DoseSync).

CONTEXT:
- Blog article topic: {seo_outline['seo_title']}
- Primary keyword: {seo_outline['primary_keyword']}
- Persona: {question.persona_segment}
- Topic cluster: {question.topic_cluster}
- Key insight from interviews: {key_insight}
- Solutions found in interviews:
{solution_summary}

TASK: Design a downloadable lead magnet of type "{magnet_type}".
Base title hint: "{magnet_title_hint}"

Return a JSON object:
{{
  "type": "{magnet_type}",
  "title": "compelling title (under 60 chars, includes primary keyword or pain point)",
  "promise": "1-sentence promise — what the reader gains immediately after using this",
  "format_outline": [
    "Section 1: ...",
    "Section 2: ...",
    "Section 3: ..."
  ],
  "optin_copy_short": "15-word max CTA copy for a banner/button (e.g. 'Get the free checklist →')",
  "optin_copy_long": "2-3 sentence copy for the email opt-in form. Include the promise, mention it's free, hint at what's inside.",
  "delivery_subject_line": "Email subject line for the delivery email",
  "thank_you_headline": "Headline for the thank-you page after opt-in"
}}

Rules:
- NEVER claim DoseSync provides medical advice
- NEVER include specific drug names
- The lead magnet must be genuinely useful standalone — not a product ad
- DoseSync can be mentioned once as the tool that helps implement the system

Return ONLY valid JSON, no markdown fences."""

    message = client.messages.create(
        model=config.model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)
