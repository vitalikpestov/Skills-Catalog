import anthropic
import json
from typing import Dict


def parse_interview(transcript: str, language: str = "en", model: str = "claude-sonnet-4-6") -> Dict:
    """
    Parse a voice interview transcript into structured content blocks:
    - pain_story: vivid opening story of the core problem
    - mistakes: common mistakes caregivers make
    - solutions: practical tips/systems that work
    - case_stories: 1-3 anonymised real stories or composites
    - quotes: 3-5 memorable quotes from transcript
    - stats: any numbers, frequencies, durations mentioned
    - emotional_peaks: moments of high emotional intensity (anxiety, relief, fear)
    """
    client = anthropic.Anthropic()

    lang_instruction = "Respond in Russian." if language == "ru" else "Respond in English."

    prompt = f"""{lang_instruction}

You are a content editor extracting structured material from a caregiver interview transcript.

TRANSCRIPT:
---
{transcript}
---

Extract and structure the content into the following JSON format. If a field is not present in the transcript, return an empty list or empty string — do NOT hallucinate content.

{{
  "pain_story": "2-3 sentence vivid opening story capturing the core emotional problem. Use present tense. First person or third person composite OK.",
  "mistakes": [
    {{"mistake": "what caregivers typically do wrong", "consequence": "what happens as a result"}}
  ],
  "solutions": [
    {{"tip": "practical actionable advice", "detail": "1-2 sentences expanding the tip"}}
  ],
  "case_stories": [
    {{"persona": "brief persona description (anonymised)", "situation": "what happened", "outcome": "how it was resolved or what was learned"}}
  ],
  "quotes": [
    "direct or lightly paraphrased quote from the transcript"
  ],
  "stats": [
    {{"claim": "specific number or frequency mentioned", "context": "what it refers to"}}
  ],
  "emotional_peaks": [
    {{"moment": "brief description of emotional moment", "emotion": "anxiety|relief|guilt|fear|hope|frustration"}}
  ],
  "key_insight": "single most important takeaway from this interview in one sentence"
}}

Return ONLY valid JSON, no markdown fences, no preamble."""

    message = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    blocks = json.loads(raw)
    return blocks
