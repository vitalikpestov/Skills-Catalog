# Resume Checkpoint

Restore pipeline state and resume from the last incomplete phase. Two modes: state.yaml-based (primary) or git tag-based (debugging).

## When to Use

- Pipeline was interrupted (crash, terminal close, user pause)
- User says "resume", "continue", or re-runs `/leadgen` on a project with existing state
- Debugging: want to re-run a specific phase with different parameters

## Primary Resume: state.yaml

### Algorithm

1. Load state.yaml: `load_data(project, "state.yaml")`
2. If no state.yaml → start fresh (new pipeline)
3. If status == "completed" → pipeline already done. Ask: "Start a new run?"
4. If status == "failed" → show error. Ask: "Retry failed phase or start fresh?"
5. If status == "running" or "paused":
   a. Find `current_phase` from state.yaml
   b. Find first phase where status is NOT "completed" or "skipped":
      - If "in_progress" → retry this phase from the beginning
      - If "pending" → start this phase
      - If "failed" → ask user: retry or skip
   c. Skip all "completed" and "skipped" phases (do NOT re-execute)
      - "skipped" phases are from Mode 2/3 (e.g., offer_extraction skipped when project exists)
   d. Load run file (`runs/{run_id}.json`) for execution context

### Present to User
```
Found existing pipeline for {project}.
Status: {status}
Completed: offer_extraction ✓, filter_generation ✓, cost_gate ✓
Current: round_loop (in progress — 287 companies gathered, 89 targets)
Pending: people_extraction, sequence_generation, campaign_push

Resume from round_loop? Or start fresh?
```

### On Resume
1. Set status: "running"
2. Set current_phase to the first non-completed phase
3. Update last_updated timestamp
4. Save state.yaml
5. Skip to that phase in the manager-leadgen flow

### On Start Fresh
1. Archive old state: `save_data(project, "state-archive/{old_session_id}.yaml", old_state)`
2. Create new state.yaml with all phases "pending"
3. Begin Phase 1

## Secondary Resume: Git Tags (Debugging)

If git checkpoints exist (from phase-checkpoint skill):

### List Available Checkpoints
```bash
git tag -l "leadgen-{project}*"
```

### Restore to Specific Phase
```bash
git checkout leadgen-{project}-phase-{N}-{name} -- .
```
This restores all files to the state they were in after phase N completed.

### Then Resume
Update state.yaml: reset all phases after N to "pending". Continue from phase N+1.

## Phase Mapping

| Phase ID | Name | What's Preserved on Resume |
|----------|------|---------------------------|
| 1 | offer_extraction | project.yaml with offer_summary |
| 2 | filter_generation | filters in run file (FilterSnapshots) |
| 3 | cost_gate | cost approval recorded |
| 4 | round_loop | All companies, scrapes, classifications in run file |
| 5 | people_extraction | Extracted contacts in run file |
| 6 | sequence_generation | sequences.json |
| 7 | campaign_push | campaigns.json with SmartLead IDs |

## Safety Rules

- NEVER delete old state.yaml — archive it
- NEVER modify completed run files — create new runs for new data
- If state.yaml and run file disagree → trust state.yaml (it's the pipeline-level authority)
- If unsure → ask user before resuming
