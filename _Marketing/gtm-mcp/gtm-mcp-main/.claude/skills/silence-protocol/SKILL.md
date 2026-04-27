# Silence Protocol

When active, agent produces zero conversational output. All results go through MCP tool calls (`save_data`) only. Enables clean parallel execution without interleaved chat.

## When to Use

- Background workers spawned by manager-leadgen (via Task tool)
- Batch operations during round loop (scrape, classify, people)
- Any agent invoked with `run_in_background: true`

## When NOT to Use

- Interactive commands (/leadgen, /qualify, /outreach, /replies) — user needs feedback
- Approval gates — must ask user and wait for response
- Error reporting that prevents file writing

## Rules

1. **No conversational output**: Do not explain, summarize, or narrate. No status updates in chat.
2. **Tool-call-only output**: Write all results via `save_data` tool. Never use chat to communicate results.
3. **Completion = file existence**: Success/failure is determined by whether the output file exists and its content.

## Execution Metadata

Include in every output written by a silent worker:

```json
{
  "_execution": {
    "agent": "company-qualifier",
    "started_at": "2026-04-06T10:00:00Z",
    "completed_at": "2026-04-06T10:05:00Z",
    "status": "success",
    "error": null,
    "items_processed": 100,
    "items_succeeded": 89,
    "items_failed": 11
  },
  "results": { ... }
}
```

## Exceptions

Silence protocol does NOT suppress:
- Fatal errors that prevent any file writing (report to chat as last resort)
- Permission requests (MCP tool access needs user approval)
- These should be rare — design workers to handle errors in output files
