import anthropic
import json
from typing import Dict, List
from guardrails import get_disclaimer

EMAIL_DELAY_HOURS = [0, 24, 72, 168, 264]  # 0h, 1d, 3d, 7d, 11d

EMAIL_GOALS = [
    "deliver_lead_magnet",
    "story_and_empathy",
    "education_tip",
    "behind_the_scenes",
    "pre_launch_soft",
]

EMAIL_GOAL_DESCRIPTIONS = {
    "deliver_lead_magnet": "Deliver the lead magnet. Thank them. Set expectations for the series.",
    "story_and_empathy": "Share a relatable caregiver story. Build emotional connection. No pitch.",
    "education_tip": "One practical tip related to the blog topic. Demonstrate expertise. Soft DoseSync mention.",
    "behind_the_scenes": "Show behind-the-scenes of building DoseSync. Build trust and anticipation.",
    "pre_launch_soft": "Announce DoseSync launching soon. Share what's coming. Invite to waitlist/early access.",
}


def generate_email_funnel(
    question,
    lead_magnet: Dict,
    config,
) -> Dict:
    client = anthropic.Anthropic()

    lang_instruction = (
        "Write all content in Russian. Use 'Вы'-form. Subject lines in Russian."
        if question.language == "ru"
        else "Write in English."
    )
    disclaimer = get_disclaimer(question.language)

    emails_count = min(config.emails_count, len(EMAIL_DELAY_HOURS))
    sequence = []

    for i in range(emails_count):
        goal = EMAIL_GOALS[i]
        delay = EMAIL_DELAY_HOURS[i]
        goal_desc = EMAIL_GOAL_DESCRIPTIONS[goal]

        email = _generate_single_email(
            client=client,
            step=i,
            goal=goal,
            goal_desc=goal_desc,
            delay_hours=delay,
            question=question,
            lead_magnet=lead_magnet,
            config=config,
            lang_instruction=lang_instruction,
            disclaimer=disclaimer,
        )
        sequence.append(email)

    launch_broadcast = _generate_launch_broadcast(
        client=client,
        question=question,
        lead_magnet=lead_magnet,
        config=config,
        lang_instruction=lang_instruction,
        disclaimer=disclaimer,
    )

    return {
        "trigger": f"optin_{question.id}_{question.topic_cluster}",
        "persona_segment": question.persona_segment,
        "language": question.language,
        "sequence": sequence,
        "launch_broadcast_template": launch_broadcast,
    }


def _generate_single_email(
    client, step, goal, goal_desc, delay_hours,
    question, lead_magnet, config,
    lang_instruction, disclaimer,
) -> Dict:
    prompt = f"""{lang_instruction}

You are a conversion copywriter for DoseSync (family medication coordination iOS app).

CONTEXT:
- Subscriber opted in for: "{lead_magnet.get('title', '')}"
- Blog topic: {question.raw_question}
- Persona: {question.persona_segment}
- Email #{step} in nurture sequence, sent {delay_hours}h after opt-in
- Email goal: {goal_desc}

Write email #{step} as a JSON object:
{{
  "step": {step},
  "delay_hours": {delay_hours},
  "subject_lines": ["variant A subject", "variant B subject"],
  "preview_text": "45-char preview text",
  "goal": "{goal}",
  "content_summary": [
    "Opening hook (1-2 sentences)",
    "Body section 1",
    "Body section 2",
    "CTA description"
  ],
  "cta": "CTA button text (under 6 words)",
  "ps_line": "Optional P.S. line (soft, human, not pushy)"
}}

Rules:
- Emails 0-1: zero product pitch, focus on value delivery
- Emails 2-3: gentle DoseSync mentions (1-2 per email max)
- Email 4: soft pre-launch anticipation only
- Plain conversational tone, not corporate
- CTA must be specific to the email goal
- NEVER claim DoseSync is medical tool
- Disclaimer appended to email 4 only: {disclaimer.strip()}

Return ONLY valid JSON."""

    message = client.messages.create(
        model=config.model,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


def _generate_launch_broadcast(
    client, question, lead_magnet, config,
    lang_instruction, disclaimer,
) -> Dict:
    prompt = f"""{lang_instruction}

You are a conversion copywriter for DoseSync launching 2026-07-07.

CONTEXT:
- Subscriber originally opted in for: "{lead_magnet.get('title', '')}"
- Their persona: {question.persona_segment}
- Topic interest: {question.topic_cluster}

Write the LAUNCH DAY broadcast email as JSON:
{{
  "step": 999,
  "delay_hours": 0,
  "subject_lines": ["variant A — urgency/benefit", "variant B — curiosity/story"],
  "preview_text": "45-char preview text",
  "goal": "launch_announcement",
  "content_summary": [
    "Open by calling back their original pain (reference the lead magnet topic)",
    "Announce DoseSync is live today",
    "3 specific features that solve their pain",
    "7-day free trial offer (no free plan)",
    "Primary CTA to App Store"
  ],
  "cta": "Start my free 7-day trial",
  "ps_line": "P.S. line adding urgency or social proof",
  "disclaimer": "{disclaimer.strip()}"
}}

Return ONLY valid JSON."""

    message = client.messages.create(
        model=config.model,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)
