# Sample Stuffolio Scan

These files are a snapshot of workflow-audit output from a real run against
the Stuffolio iOS/macOS codebase (build 25, scan date 2026-02-23). They are
shipped as reference material so a new user can see what each layer's output
actually looks like before running their own audit.

**They are NOT methodology.** The methodology lives one directory up in
`agents/`. These files are illustrative output.

Files:

- `sample-layer1-inventory.yaml` — entry-point catalog from Layer 1
- `sample-layer1-summary.md` — narrative summary of Layer 1 findings
- `sample-layer2-summary.md` — narrative summary of Layer 2 flow traces
- `sample-layer2-traces/flow-NNN-*.yaml` — three traced Stuffolio user flows
- `sample-layer3-results.yaml` — categorized issues from Layer 3

When workflow-audit runs against your project, it writes equivalently-named
files (without the `sample-` prefix) to `.workflow-audit/` in your project
root.

## What the sample scan found (Stuffolio v1.0, Build 25)

| Severity | Count | Key Issues |
|----------|-------|------------|
| 🔴 Critical | 1 | MenuBarView PersistentIdentifier vs String type mismatch |
| 🟡 High | 3 | macOS Stuff Scout one-shot bug, 2 buried primary actions |
| 🟢 Medium | 7 | Mock data (2), unwired data (3), orphaned code (2) |
| ⚪ Low | 3 | Platform parity gap, superseded sheet cases, unwired rating |

The totals here are illustrative — they show the shape of a real audit's
output, not a target your project should match.
