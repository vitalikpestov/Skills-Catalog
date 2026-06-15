# Skill: /ceo-review

CEO intelligent analysis of the current state. Reads CEO-DASHBOARD.md + key inboxes, gives prioritized action list in 15 minutes of reading.

## Trigger

User types `/ceo-review` or `/ceo-review <focus>` where focus = `blocks` | `prs` | `agents` | `health`

## Execution

<ceo-review>

### Step 1 — Regenerate dashboard

Run the dashboard script to ensure fresh data:

```bash
bash $PROJECT_ROOT/.claude/scripts/ceo-dashboard.sh
```

### Step 2 — Read key files

Read in parallel:
1. `.claude/docs/CEO-DASHBOARD.md` — main dashboard
2. `.claude/agents/pm/inbox-pm.md` — last 50 lines (recent PM state)
3. `.claude/docs/ceo-escalations.md` — all active escalations

### Step 3 — Analyze and prioritize

Apply this decision framework to produce the CEO action list:

**Priority triage rules:**
- 🔴 P0 in escalations or BLOCKED > 8h → surface first, requires CEO decision NOW
- PRs without needs-qa AND older than 7 days → potential merge backlog problem
- Agent active > 8h with no closure marker → 🟠 тихий блокер, check inbox
- Autonomy% < 60% → agency not autonomous enough, identify root cause
- Escalation count trending up → systemic problem, needs ADR or playbook

**Output format:**

```
## CEO Action List — [date]

### 🔴 Requires decision NOW (P0)
[one line each, max 3]

### ✅ Merge ready (30 sec each)
[PR# + title, action = gh pr merge or close]

### 🟠 Check these agents (potential silent blockers)
[agent name + last task + hours since update]

### 📋 Today's 3 priorities
1. [most impactful action]
2. [second]
3. [third]

### 💡 Pattern alert
[if same topic escalated 3+ times → suggest ADR/playbook]

**Time to read: ~5 min | Time to act on #1 priority: estimated Xh**
```

### Step 4 — If focus argument provided

- `blocks` → expand only Block 1 analysis, list each blocker with suggested resolution
- `prs` → expand Block 2, sort PRs by age, flag stale >14 days for closure
- `agents` → expand Block 3, show each active agent's full task list
- `health` → expand Block 7, trend analysis vs previous run (if available)

### Rules

- Do NOT recommend merging PRs with `needs-qa` label without QA closure marker
- Do NOT recommend closing stale PRs without first checking if they're in active sprint
- If autonomy% < 40% for 3+ consecutive days → escalate to CEO as systemic issue
- Keep entire response under 300 words — CEO reads in 5 min max
- Language: Russian (mirrors agency communication style)

</ceo-review>
