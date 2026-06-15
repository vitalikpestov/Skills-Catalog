# Skill: /horizon-check

Статус до лонча: дни, milestone drift, блокеры.

## Trigger

`/horizon-check`

## Execution

<horizon-check>

### Step 1 — Run script

```bash
python3 $PROJECT_ROOT/.claude/scripts/horizon-check.py
```

### Step 2 — Add context

- Если drift (milestone просрочен и не done) → добавить в inbox-pm.md: `🆕 [DRIFT] M? — название просрочен, обновить статус`
- Если submit_days_remaining < 21 → флаг: "⚠️ Submit в X дней — приоритет QA"
- Если blockers > 0 → список с owner и next action

### Output format

```
🎯 До лонча: 56d (2026-08-04)
📤 До submit: 39d (2026-07-18)

Milestones: 🟢🟢🟢🟢 (0 drift)
Blockers: 0

[drift items if any]
```

### Rules

- Язык: русский
- < 100 слов
- Если всё зелёное → "Трек в норме"

</horizon-check>
