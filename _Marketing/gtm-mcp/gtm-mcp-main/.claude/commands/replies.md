# /replies — Sync, Classify & Triage Campaign Replies

Sync replies from SmartLead campaigns, classify them, and present a triage report.

**Read before starting:** **reply-classification** skill (3-tier funnel, classification rules, draft response generation).

## Arguments
- `--campaign <name>`: Specific campaign (default: all active campaigns)
- `--project <name>`: All campaigns for a project
- `--warm-only`: Show only warm replies (interested + meeting_request)

## Phase 1: Sync + Classify

### 1. Discover Campaigns
- Call `smartlead_list_campaigns`
- Filter by project if specified
- Get campaigns with status ACTIVE or COMPLETED

### 2. Fetch Replied Leads
For each campaign:
- Call `smartlead_sync_replies`
- Get all leads with reply status

### 3. Classify (3-Tier Funnel)
**Skill**: reply-classification

For each reply:

**Tier 1 (FREE)**: Check regex patterns
- OOO → classify as out_of_office (0.95 confidence)
- Unsubscribe → classify as unsubscribe (0.90 confidence)
- Bounce → skip entirely
- If matched → DONE for this reply

**Tier 2 (FREE)**: Fetch full thread
- Call SmartLead API for full message history
- Extract latest REPLY (not our sent messages)
- Re-check Tier 1 on full text
- Strip HTML

**Tier 3 (LLM)**: Classify ambiguous replies
- Use classification rules from reply-classification skill
- Max 10 concurrent LLM calls
- Return: category, confidence, reasoning

### 4. Dedup
- Hash: MD5 of first 500 chars (lowercased, stripped)
- Skip already-classified replies

## Phase 2: Triage Report

Present results sorted by priority:

### WARM REPLIES (interested + meeting_request)
```
1. John Smith, VP Sales at Acme Corp
   "Sounds good, send me pricing info"
   → Suggested action: Send pricing sheet, offer 15-min call

2. Jane Doe, CTO at TechCo
   "Can we schedule a demo next week?"
   → Suggested action: Share calendar link
```

### QUESTIONS (need response)
```
3. Mike Johnson, Head of Growth at StartupX
   "How does your integration with Salesforce work?"
   → Suggested answer: [based on project offer context]
```

### WRONG PERSON (with referrals)
```
4. Sarah Lee at BigCorp
   "I left BigCorp last month. Try reaching Tom Wilson, he's the new VP."
   → Action: Add Tom Wilson to pipeline
```

### NOT INTERESTED
- 12 explicit declines — no action needed

### AUTO-FILTERED
- 8 out-of-office (will return by various dates)
- 3 unsubscribes (removed from campaigns)
- 2 bounces (invalid emails)

## Summary Stats

```
Campaign: Fintech PAYMENTS Q1
Total replies: 45
Warm: 8 (18%)
Needs response: 12
Auto-filtered: 13
Classification: Tier 1 FREE: 13 | Tier 2 FREE: 12 | Tier 3 LLM: 20
```

## Phase 3: Draft Response Generation

After triage, automatically offer to draft responses for warm replies.

### Flow
1. "I found {N} warm replies. Want me to draft responses?"
2. If yes → generate drafts using rules from reply-classification skill (Draft Response Generation section):
   - Reference their specific reply content
   - Include project context (offer, case studies, metrics)
   - 3-5 sentences max, matching sequence tone
   - Specific CTA per reply type (meeting → calendar, question → answer + call offer)
   - No re-pitching — acknowledge interest and move forward
3. Present ALL drafts at once for batch review:
   ```
   Draft 1/8: John Smith (Acme Corp) — interested
   "Hi John, Great to hear from you! [draft]..."
   → [approve] [edit] [skip]
   
   Draft 2/8: Jane Doe (TechCo) — meeting_request
   "Hi Jane, Thursday at 2pm works for me! [draft]..."
   → [approve] [edit] [skip]
   ```
4. On batch approve → call `smartlead_send_reply` for each approved draft
5. Track approved/dismissed ratio for operator learning

## Ongoing Monitoring

After initial sync:
- "Reply monitoring is active. Run /replies again anytime for updates."
- For Telegram notifications: configure via project settings
