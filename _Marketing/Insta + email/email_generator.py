"""
Uses Claude to generate a newsletter email from Instagram post content.
"""

import anthropic


SYSTEM_PROMPT = """You are an expert email copywriter specializing in newsletters for motivational coaches and wellness brands.

Your job is to turn Instagram content (captions and video transcripts) into a compelling, high-converting newsletter email.

Guidelines:
- Write in a warm, personal, and inspiring tone that matches the brand voice
- Structure the email with a strong subject line, engaging intro, main content sections, and a clear CTA
- Keep it scannable: use short paragraphs, subheadings where helpful
- Reference specific insights, stories, or tips from the Instagram content — don't be generic
- The email should feel cohesive, not like a list of posts
- Length: 400-600 words in the body (not including subject line)
- Format in clean HTML suitable for email clients
- IMPORTANT: When greeting the reader use exactly {{contact.first_name}} as the merge tag (e.g. "Hey {{contact.first_name}},") — this is the Go High Level personalisation tag and must not be changed"""


def generate_newsletter_email(
    posts_content: list[dict],
    client_name: str,
    from_name: str,
    subject_prefix: str,
    anthropic_api_key: str,
    cta_text: str = "",
    cta_url: str = "",
) -> dict:
    """
    Generate a newsletter email from post content using Claude.

    posts_content: list of dicts with keys: url, type, caption, transcript (optional)
    Returns dict with: subject, html_body, plain_text_preview
    """
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    # Build the content block for Claude
    content_sections = []
    for i, post in enumerate(posts_content, 1):
        section = f"## Post {i} ({post['type']})\n"
        if post.get("caption"):
            section += f"**Caption:**\n{post['caption']}\n\n"
        if post.get("transcript"):
            section += f"**Video Transcript:**\n{post['transcript']}\n\n"
        content_sections.append(section)

    content_block = "\n".join(content_sections)

    cta_instruction = ""
    if cta_text and cta_url:
        cta_instruction = f"\n\nInclude a prominent CTA button with the text \"{cta_text}\" linking to: {cta_url}"
    elif cta_text:
        cta_instruction = f"\n\nInclude a prominent CTA button with the text \"{cta_text}\""

    user_prompt = f"""Here is the Instagram content from {from_name}'s recent posts.
Please write a newsletter email that turns this content into an engaging email for their audience of ~8,000 subscribers.{cta_instruction}

{content_block}

Output format (return exactly this structure):
SUBJECT LINE: [subject line here]
---
HTML BODY:
[full HTML email body here]
---
PREVIEW TEXT: [40-60 char preview/preheader text]"""

    print("Generating newsletter email with Claude...")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text
    return _parse_claude_output(raw)


def _parse_claude_output(raw: str) -> dict:
    """Parse Claude's structured output into components."""
    import re
    result = {"subject": "", "html_body": "", "preview_text": ""}

    # Extract subject line
    subject_match = re.search(r"SUBJECT LINE:\s*(.+)", raw)
    if subject_match:
        result["subject"] = subject_match.group(1).strip()

    # Extract preview text
    preview_match = re.search(r"PREVIEW TEXT:\s*(.+)", raw)
    if preview_match:
        result["preview_text"] = preview_match.group(1).strip()

    # Extract HTML body — everything between HTML BODY: and the next --- or PREVIEW TEXT:
    body_match = re.search(
        r"HTML BODY:\s*\n(.*?)(?:\n---|\nPREVIEW TEXT:)",
        raw,
        re.DOTALL
    )
    if body_match:
        result["html_body"] = body_match.group(1).strip()
    else:
        # Fallback: grab everything after HTML BODY: if no clear end marker
        body_fallback = re.search(r"HTML BODY:\s*\n(.*)", raw, re.DOTALL)
        if body_fallback:
            body = body_fallback.group(1).strip()
            # Remove trailing PREVIEW TEXT line if present
            body = re.sub(r"\nPREVIEW TEXT:.*$", "", body, flags=re.DOTALL).strip()
            result["html_body"] = body

    return result
