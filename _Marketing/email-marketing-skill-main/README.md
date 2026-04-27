# Email Marketing Skill for Claude

A skill that gives Claude deep, opinionated expertise in email marketing. Covers strategy, deliverability, list building, segmentation, automation, copywriting, analytics, and ESP selection.

This isn't a generic best-practice summary. It reflects the experience and opinions of a practitioner.

## What's covered

- **[Authentication](email-marketing/authentication.md)** — SPF, DKIM, DMARC setup and troubleshooting; transactional vs marketing email
- **[List building](email-marketing/list-building.md)** — Forms, lead magnets, single vs double opt-in, subscriber source tracking
- **[Segmentation and data](email-marketing/segmentation-and-data.md)** — Segmentation types, dynamic vs static segments, data hygiene, privacy compliance, personalisation and merge tags
- **[Copywriting](email-marketing/copywriting.md)** — Subject lines, email anatomy, CTAs, spam trigger avoidance
- **[Automation and sequences](email-marketing/automation-and-sequences.md)** — Automation triggers, welcome sequences, abandoned cart, re-engagement, campaign goal-setting
- **[Deliverability and metrics](email-marketing/deliverability.md)** — How inbox placement works, getting out of spam, IP warming, full metrics reference, Gmail Promotions tab, MIME structure
- **[ESP selection and reference](email-marketing/esp-and-reference.md)** — Five-factor ESP evaluation framework, legislation quick reference (CAN-SPAM, GDPR, CASL, CCPA), common mistakes, glossary

## Usage

### Claude Code

Clone the repo, then add the skill directory path to your project or user settings in `.claude/settings.json`:

```json
{
  "skills": [
    "/path/to/email-marketing-skill/email-marketing"
  ]
}
```

### Claude.ai

Add the contents of [`email-marketing/SKILL.md`](email-marketing/SKILL.md) as custom instructions in a [Claude.ai project](https://claude.ai).

### API / other integrations

Include the contents of [`email-marketing/SKILL.md`](email-marketing/SKILL.md) in your system prompt.

## Examples

Once Claude has access to the skill, ask about anything email marketing related:

- "Help me plan a welcome email sequence"
- "What's wrong with my deliverability?"
- "Write subject lines for a product launch campaign"
- "Should I use single or double opt-in?"
- "Compare Mailchimp and Klaviyo for my use case"
- "Set up SPF and DKIM for my domain"

## Contributing

Contributions are welcome. If you have practitioner-level insights to add, open a PR. Keep the tone opinionated and practical — this skill deliberately avoids wishy-washy "it depends" advice where a clear recommendation is warranted.

## License

MIT
