# Skill: /sprint-status

Weekly Friday review — velocity агентов, корректировка приоритетов, learnings.

## Trigger

`/sprint-status` или `/sprint-status <week>` (e.g. `/sprint-status W22`)

## Execution

<sprint-status>

### Step 1 — Regenerate dashboard

```bash
bash $PROJECT_ROOT/.claude/scripts/ceo-dashboard.sh
```

### Step 2 — Collect sprint data

Read in parallel:
1. `.claude/docs/CEO-DASHBOARD.md` — свежий dashboard
2. `.claude/agents/pm/inbox-pm.md` — задачи недели (last 100 lines)
3. All inbox files — grep `✅ DONE` с датой текущей недели
4. `git log --oneline --since="7 days ago"` — commit velocity

### Step 3 — Sprint analysis

Compute for the week:

**Velocity (задачи):**
- Закрыто задач (✅ DONE с датой этой недели): N
- Открытых осталось: M
- Completion rate: N/(N+M) %

**Commit velocity:**
- Total commits 7d
- По агентам (ios-dev / be-dev / web-dev / i18n) по ветке/коммит-префиксу

**Escalations:**
- ⚠️ BLOCKED эпизодов за неделю
- [ARCH] вопросов (→ нужен новый ADR?)
- P0 эскалаций

**SLA нарушения:**
- Задачи в работе >8h без closure (🔴 в Block 3 dashboard)

**Автономность trend:**
- Dashboard autonomy% vs прошлая неделя (если есть предыдущий snapshot)

### Step 4 — Output format

```
## Sprint Status — [неделя] [даты]

### Velocity
- Закрыто задач: N
- Commits: M (ios-dev: X, be-dev: Y, web-dev: Z)
- Completion rate: P%

### Блокеры недели
- [список ⚠️ BLOCKED эпизодов с агентом и темой]

### Топ 3 достижения
1. [самый важный shipped результат]
2. ...
3. ...

### Рекомендации на следующую неделю
1. [приоритет #1 исходя из данных]
2. [агент с наибольшим backlog]
3. [если BLOCKED повторился — предложить ADR]

### Ритуал пятницы (5 мин)
- [ ] Обновить context files агентов с новыми constraints?
- [ ] Добавить learning в RULES.md?
- [ ] Нужен новый ADR для повторяющегося [ARCH]?
- [ ] Приоритизировать inbox-pm.md на следующую неделю?

**Автономность:** [bar] X% → цель 90%
**До лонча:** N дней
```

### Rules

- Ответ < 400 слов — CEO читает за 3 мин
- Язык: русский
- Не пересказывать что уже видно в dashboard — только insights и рекомендации
- Если completion rate < 50% → явно назвать root cause (too many P2, agent blocked, scope creep)
- Если один агент закрыл 0 задач за неделю → флаг: возможно нет задач в inbox

</sprint-status>
