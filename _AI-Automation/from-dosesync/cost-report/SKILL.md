# Skill: /cost-report

Отчёт по расходам на Claude API за период. Парсит `.jsonl` сессии, считает USD по моделям.

## Trigger

`/cost-report` — last 24h  
`/cost-report 7` — last 7 days  
`/cost-report 30` — last 30 days

## Execution

<cost-report>

### Step 1 — Run tracker

```bash
python3 $PROJECT_ROOT/.claude/scripts/track-cost.py --days {N} --report
```

Где `{N}` = число из аргумента (default 1 если не указано).

### Step 2 — Contextualise

После вывода скрипта добавить:

- **Trend:** сравни с предыдущим периодом из `.claude/docs/cost-tracking.jsonl` (если есть записи)
- **Top model:** какая модель съела больше всего $
- **Recommendation:** если Opus > 70% расходов — флаг: "Consider Sonnet for non-complex tasks"

### Step 3 — Append snapshot

```bash
python3 $PROJECT_ROOT/.claude/scripts/track-cost.py --days {N}
```

(без `--report` → записывает в `.claude/docs/cost-tracking.jsonl`)

### Output format

```
💰 Cost Report — [period]

| Model | Calls | Tokens | Cost |
|-------|-------|--------|------|
| ...   |       |        |      |
| TOTAL |       |        | $X.XX |

**Trend:** +X% vs previous period (или "First record")
**Alert:** [если daily avg > $50 — предупредить]
**Tip:** [рекомендация по оптимизации]
```

### Rules

- Язык: русский
- Ответ < 200 слов
- Если нет данных за период → "No sessions found"
- Daily avg = total / days

</cost-report>
