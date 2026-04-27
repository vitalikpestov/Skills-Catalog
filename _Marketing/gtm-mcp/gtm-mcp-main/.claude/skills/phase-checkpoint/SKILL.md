# Phase Checkpoint

Create a git checkpoint after a pipeline phase completes. Enables time-travel debugging and rollback.

**This skill is OPTIONAL.** The primary resume mechanism is state.yaml (see io-state-safe). Git checkpoints provide additional debugging and rollback capability.

## When to Use

- After each major phase completes in the leadgen pipeline
- After user approves a critical decision (offer, filters, sequence)
- Before starting an expensive phase (round loop, people extraction)

## Procedure

### 1. Check for Changes
```bash
git status --porcelain
```
If no changes since last commit → skip (idempotent). Return `status: "skipped"`.

### 2. Stage Project Files
```bash
git add -A
```

### 3. Create Commit
```bash
git commit -m "checkpoint: {project} phase {phase_id} ({phase_name}) completed"
```

### 4. Create Tag
```bash
git tag "leadgen-{project-slug}-phase-{phase_id}-{phase_name}"
```

Tag format: `leadgen-easystaff-payroll-phase-3-cost_gate`

### 5. Update state.yaml

Add checkpoint record to state:
```yaml
checkpoints:
  - phase: 3
    name: "cost_gate"
    tag: "leadgen-easystaff-payroll-phase-3-cost_gate"
    commit: "abc123def"
    created_at: "2026-04-06T10:15:00Z"
```

## Phase Mapping

| Phase ID | Name | Checkpoint Value |
|----------|------|------------------|
| 1 | offer_extraction | Offer approved by user |
| 2 | filter_generation | Filters approved by user |
| 3 | cost_gate | User confirmed spend |
| 4 | round_loop | Round(s) completed with classifications |
| 5 | people_extraction | Contacts extracted, KPI checked |
| 6 | sequence_generation | Sequence approved by user |
| 7 | campaign_push | Campaign pushed to SmartLead |

## Viewing Checkpoints
```bash
git tag -l "leadgen-{project}*"
git log --oneline --decorate leadgen-{project}-phase-1-offer_extraction..leadgen-{project}-phase-4-round_loop
```

## Idempotency

Running checkpoint twice for the same phase with no changes → second run skips gracefully. Safe to call after every phase without checking if already checkpointed.
