# Skill: /arch-check

MVVM boundary audit — Views не должны импортировать Supabase, Models не должны импортировать SwiftUI.

## Trigger

`/arch-check`  
`/arch-check --ci` — exit 1 если P0 violations

## Execution

<arch-check>

### Step 1 — Run checker

```bash
bash /Users/vitalik/Documents/Projects/MobileApp/.claude/scripts/check-architecture-boundaries.sh
```

### Step 2 — On P0 violations

Добавь в `inbox-qa-reviewer.md`:
```
🆕 [ARCH-BOUNDARY] P0 — View/Model layer violation (N files). 
Run: bash .claude/scripts/check-architecture-boundaries.sh
Fix: переместить Supabase-вызовы в Service/ViewModel слой.
```

### Output format

```
Boundary check: N violations (P0: X, P1: Y)

P0 files: [список]
Action: [что делать]
```

### Rules

- Язык: русский
- < 150 слов
- Чистый результат → "Границы слоёв чистые ✅"
- P1 violations (ViewModels→Supabase) — предупреждать, не блокировать (migration debt)

</arch-check>
