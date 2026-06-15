---
name: inbox
description: Write a task directly to a specific agent's inbox. Usage: /inbox <agent-name> — followed by task description. Maps short alias to canonical inbox path, appends 🆕 entry in standard format, commits the change.
---

# /inbox — Agent Inbox Writer

Writes a new task directly to the specified agent's inbox file.

## Trigger

`/inbox <agent-name> [optional: task description inline]`

If task description is not inline — use the current conversation context (what the user described just before or after the command).

## Agent Alias → Inbox Path Map

| Alias | Inbox path |
|-------|-----------|
| `ios`, `ios-dev`, `ios-developer` | `.claude/agents/dev/inbox-ios-developer.md` |
| `be`, `backend`, `backend-dev`, `backend-developer` | `.claude/agents/dev/inbox-backend-developer.md` |
| `web`, `web-dev`, `web-developer` | `.claude/agents/dev/inbox-web-developer.md` |
| `android`, `android-dev`, `android-developer` | `.claude/agents/dev/inbox-android-developer.md` |
| `qa`, `qa-reviewer` | `.claude/agents/dev/inbox-qa-reviewer.md` |
| `i18n`, `translator`, `i18n-translator` | `.claude/agents/marketing/inbox-i18n-translator.md` |
| `designer`, `ux`, `ui-ux`, `ui-ux-designer` | `.claude/agents/design/inbox-ui-ux-designer.md` |
| `pm`, `pm-orchestrator` | `.claude/agents/pm/inbox-pm.md` |
| `ceo`, `vitalik`, `physical` | `.claude/agents/pm/inbox-ceo-physical.md` |
| `cpo` | `.claude/agents/product/inbox-cpo.md` |
| `bizanal`, `analyst` | `.claude/agents/product/inbox-bizanal.md` |
| `marketing`, `director`, `marketing-director` | `.claude/agents/marketing/inbox-director.md` |
| `aso`, `app-store-optimizer` | `.claude/agents/marketing/inbox-app-store-optimizer.md` |
| `analytics`, `analytics-lead` | `.claude/agents/marketing/analytics/inbox-analytics-lead.md` |
| `growth`, `growth-hacker` | `.claude/agents/marketing/inbox-growth-hacker.md` |
| `monetization`, `monetization-lead` | `.claude/agents/marketing/monetization-retention/inbox-monetization-lead.md` |
| `ua`, `paid-ua`, `paid-ua-lead` | `.claude/agents/marketing/paid-ua/inbox-paid-ua-lead.md` |
| `asa`, `asa-specialist` | `.claude/agents/marketing/paid-ua/inbox-asa-specialist.md` |
| `pr`, `pr-growth`, `pr-growth-lead` | `.claude/agents/marketing/pr-growth/inbox-pr-growth-lead.md` |
| `seo`, `seo-geo`, `seo-geo-expert` | `.claude/agents/marketing/inbox-seo-geo-expert.md` |
| `content`, `content-creator` | `.claude/agents/marketing/inbox-content-creator.md` |
| `reddit` | `.claude/agents/marketing/inbox-reddit-community-builder.md` |
| `tiktok` | `.claude/agents/marketing/inbox-tiktok-strategist.md` |
| `instagram` | `.claude/agents/marketing/inbox-instagram-curator.md` |
| `linkedin` | `.claude/agents/marketing/inbox-linkedin-content-creator.md` |
| `twitter` | `.claude/agents/marketing/inbox-twitter-engager.md` |
| `lawyer`, `legal` | `.claude/agents/legal/inbox-lawyer.md` |
| `compliance` | `.claude/agents/legal/inbox-compliance.md` |
| `findir`, `finance` | `.claude/agents/finance/inbox-findir.md` |
| `vcr`, `investor` | `.claude/agents/finance/inbox-vcr.md` |
| `support` | `.claude/agents/support/inbox-support.md` |

## Execution Steps

1. **Parse args** — identify agent alias from `/inbox <alias>`. If alias unknown, list available aliases.

2. **Resolve inbox path** — map alias → full absolute path under `$PROJECT_ROOT/`.

3. **Read inbox** — scan the top 30 lines to understand current format and last task ID convention.

4. **Generate task ID** — follow pattern visible in file (e.g. `IOS-XXX-1`, `BE-XXX-1`, `CC-XXX-1`). If no pattern, use `TASK-<AGENT-SLUG>-<YYYY-MM-DD>`.

5. **Compose the task entry** using standard format:
```markdown
## 🆕 <TASK-ID> [<Priority>] — <Title> (делегировал: user, <YYYY-MM-DD>)

**Контекст:** <что нужно сделать — из conversation context>

**Acceptance criteria:**
- [ ] <критерий 1>

**Effort:** <оценка если очевидна>
**Owner:** <agent-name>
```

6. **Prepend after the first `---` separator** in the inbox file (top of active queue, before archived tasks).

7. **Save** via Edit tool.

8. **Commit**:
```
git add <inbox-path>
git commit -m "chore(inbox): add task to <agent> inbox — <task-title>"
git push origin main
```

9. **Report**: "Задача добавлена в `<inbox-path>` как `<TASK-ID>`."

## Rules

- If priority not specified by user — infer from urgency/blocking status. Default: P2.
- If task title not given inline — derive from conversation context (last user message).
- Never overwrite existing tasks. Always prepend.
- Always commit immediately after write.
- One task per invocation. For multiple tasks — run `/inbox` multiple times.
