# Skill: /test-gaps

Детектирует тест-пробелы: diff между существующими `func test_` и 69-item mandatory list из `.claude/rules/tests-and-quality.md`.

## Trigger

`/test-gaps` — полный отчёт  
`/test-gaps --ci` — exit 1 если P0/P1 gaps есть

## Execution

<test-gaps>

### Step 1 — Run detector

```bash
python3 /Users/vitalik/Documents/Projects/MobileApp/.claude/scripts/check-test-coverage.py --full
```

### Step 2 — Action on gaps

Для каждого P0 gap:
- Проверь, нет ли теста с другим именем (ложный miss)
- Если реальный gap → добавь в `inbox-qa-reviewer.md`:
  ```
  🆕 [TEST-GAP] T07 — subscription gating test missing. Добавить в Unit/FreePlanTests.swift
  ```

Для P1 gaps — добавить в backlog (P1 в inbox-qa-reviewer.md).

### Output format

```
Coverage: N/68 (X%)

P0 missing: [список или "none"]
P1 missing: [список]
Action: [что добавить в inbox]
```

### Rules

- Язык: русский
- < 150 слов
- Хороший результат ≥ 90% + 0 P0 gaps

</test-gaps>
