# IO State Safe

Safe state.yaml management for pipeline orchestration. Defines the schema, validation rules, and update protocol.

## state.yaml Schema

```yaml
session_id: "leadgen-{project-slug}-{YYYYMMDD}-{HHMMSS}"
project: "easystaff-payroll"
pipeline: "leadgen"
mode: "fresh | new_campaign | append"     # launch mode (see manager-leadgen)
status: "running"
current_phase: "round_loop"
active_campaign_slug: "payments-us"       # which campaign is being worked on (null until created)
active_campaign_id: 3070919               # SmartLead campaign ID (null until created/assigned)
active_run_id: "run-001"                  # which run file is in progress
phase_states:
  offer_extraction: "pending | in_progress | completed | failed | skipped"
  filter_generation: "pending | in_progress | completed | failed | skipped"
  cost_gate: "pending | in_progress | completed | failed | skipped"
  round_loop: "pending | in_progress | completed | failed | skipped"
  people_extraction: "pending | in_progress | completed | failed | skipped"
  sequence_generation: "pending | in_progress | completed | failed | skipped"
  campaign_push: "pending | in_progress | completed | failed | skipped"
run_id: "run-001"
started_at: "2026-04-06T10:00:00Z"
last_updated: "2026-04-06T10:25:00Z"
error: null
completed_at: null
```

## Location

`~/.gtm-mcp/projects/{slug}/state.yaml` — accessed via MCP tools:
- Read: `load_data(project, "state.yaml")`
- Write: `save_data(project, "state.yaml", data, mode="write")`

Always use `mode="write"` for state.yaml (overwrite entire file, never merge — prevents partial state corruption).

## Validation Before Write

Before saving state.yaml, verify:
1. `session_id` is set and non-empty
2. `current_phase` is one of the 7 valid phase names
3. All 7 phase_states keys exist
4. Each phase_state value is one of: pending, in_progress, completed, failed, skipped
5. `status` is one of: awaiting_approval, approved, running, paused, completed, insufficient, failed
6. `last_updated` is set to current timestamp
7. `mode` is one of: fresh, new_campaign, append
8. `active_run_id` is set and matches `run_id`

If validation fails: do NOT write. Report the invalid field to the user.

## Update Protocol

**Before starting a phase**:
```yaml
current_phase: "{phase_name}"
phase_states.{phase_name}: "in_progress"
last_updated: "{now}"
```

**After completing a phase**:
```yaml
phase_states.{phase_name}: "completed"
last_updated: "{now}"
```

**On phase failure**:
```yaml
phase_states.{phase_name}: "failed"
error: "{error_message}"
status: "failed"
last_updated: "{now}"
```

**On pipeline completion**:
```yaml
status: "completed"
completed_at: "{now}"
last_updated: "{now}"
```

## YAML Best Practices

- 2-space indentation, never tabs
- Quote strings that could be interpreted as booleans: `"true"`, `"false"`, `"yes"`, `"no"`
- Use ISO-8601 timestamps: `"2026-04-06T10:00:00Z"`
- Block scalars for multi-line error messages: `error: |`
- No trailing whitespace
