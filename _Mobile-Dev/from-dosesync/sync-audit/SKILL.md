---
name: sync-audit
description: "SwiftData↔Supabase sync-correctness auditor for DoseSync's offline-first layer. Scans Services/, ViewModels/, Models/ for the highest-risk untested surface in a medical app: lost/duplicated mutations across the offline queue. Checks 12 rules — needsSync coverage on every local mutation, optimistic-update rollback on remote failure, server-wins conflict resolution, idempotent dose confirm (double-dose), no user_id in Supabase queries, @MainActor isolation of ModelContext, no @Model refs held in View structs, sync triggers on foreground + connectivity. Inspired by mwd1234/ios-agentic-skills data-modeling-and-sync. Use before TestFlight, after any Service/sync change, or when doses go missing / duplicate / stale across devices."
user-invocable: true
---

# Sync-Audit — SwiftData↔Supabase Correctness for DoseSync

Audits the offline-first sync layer — the single highest-risk untested surface in DoseSync. A bug here is not cosmetic: a lost mutation = a dose that looks given but isn't (or vice versa), a duplicated mutation = a double-dose record. Both break the core USP.

Does NOT replace unit tests (`swift-testing`) — this is a **code-reading + grep pass** that finds structural sync defects unit tests often miss (a mutation path that forgets `needsSync`, a `try?` that swallows a remote failure silently).

## When to invoke

- `/sync-audit` or "audit sync", "check offline sync", "sync correctness"
- **Mandatory** before TestFlight when any `Services/*Sync*`, `DoseService`, `MedicationService`, `FamilyService`, or `@Model` changed
- When a dose / medication goes **missing, duplicated, or stale** across devices
- After touching `SyncService`, `NetworkMonitor`, conflict resolution, or `needsSync`

## Scope

```
DoseSync/DoseSync/Services/     — *Service.swift, SyncService, NetworkMonitor, DoseRealTimeManager
DoseSync/DoseSync/ViewModels/   — mutation call-sites
DoseSync/DoseSync/Models/       — @Model classes, needsSync attribute
```

## Output

- Console report sorted by severity (P0 → P3)
- `DoseSync/sync-audit-report.md` — markdown table: rule / file:line / severity / fix
- Summary counts per category

Severity for this skill skews high — sync defects are data-integrity defects:
- **P0** — silent data loss / duplication / double-dose bypass. Merge-blocker.
- **P1** — sync can stall or desync under a realistic path (offline→reconnect, conflict).
- **P2** — fragile pattern, works now but easy to break.
- **P3** — style / consistency.

---

## 12 Audit Rules

### Category A — Mutation Integrity (P0–P1)

**A1 — Every local mutation sets `needsSync = true`**
```
Grep targets: assignments to @Model properties in Services/ + ViewModels/
Pattern: '\.status = |\.givenAt = |\.givenBy = |\.snooze|\.pillsRemaining = |context.insert\(|context.delete\('
```
For each mutation of a synced @Model, verify `needsSync = true` is set in the same path BEFORE the remote call. A mutation without `needsSync` → if the remote call fails, the change is never retried → **silent divergence (P0)**.
Exempt: read-only computed props, draft/local-only models with no Supabase table.

**A2 — Optimistic update is retained on remote failure, never silently dropped**
```
Grep: 'try? await supabase' , 'catch {' blocks in Services/ around .update/.insert/.delete
```
Pattern must be: local mutate (needsSync=true) → `do { remote; needsSync=false } catch { /* keep needsSync=true, log */ }`.
Flag P0 if:
- `try?` on a remote mutation with **no** fallback that preserves `needsSync` (swallows failure → lost write).
- `catch` that sets `needsSync = false` anyway.
- `catch` that reverts the local optimistic change to a *wrong* state instead of leaving it queued.
Per `supabase-layer.md` Offline-First Pattern.

**A3 — `needsSync = false` only after confirmed remote success**
```
Grep: 'needsSync = false'
```
Every clear of `needsSync` must be reachable ONLY inside the success path of a remote call (after `.execute()` returns without throw). Flag any `needsSync = false` set unconditionally, in a `defer`, or before the await.

**A4 — Idempotent dose confirm (double-dose protection survives retry)**
```
Grep: 'func confirmDose|canGiveDose|func.*Dose.*async'
```
Verify confirm path checks current status (`canGiveDose()` / status guard) BEFORE applying, so a queued+retried confirm can't create a second `given` record. A retry of an already-given dose must be a no-op, not a second write. Cross-check Critical Test Case #1 + #11a. Flag P0 if retry path can double-apply.

---

### Category B — Conflict Resolution (P0–P1)

**B1 — Server-wins for `dose_records`**
```
Grep: SyncService conflict handling, 'dose_record', merge/resolve logic
```
On conflict for dose_records, server version MUST prevail (per `supabase-layer.md` Sync Strategy). Flag if local overwrites server unconditionally, or if there is no conflict branch at all (last-write-wins by accident).

**B2 — Client-wins only for drafts (medication edits, profile)**
```
Grep: medication update / profile update sync paths
```
Verify the client-wins exception is scoped to drafts, not leaking onto dose_records. Mismatched strategy = silent overwrite of a caregiver's confirmation.

---

### Category C — Concurrency & Memory (P0)

**C1 — ModelContext touched only on `@MainActor`**
```
Grep: 'modelContext' , 'ModelContext' , 'context.save()' , 'context.fetch' in Services/
Cross-check: is the enclosing type/func @MainActor or called from one?
```
SwiftData `ModelContext` is not Sendable / not thread-safe. Any `async let` / `Task.detached` / non-MainActor service that touches a context = data-race crash (the DoseLoadHelper SIGSEGV class). Flag P0. See memory `feedback_swiftdata_model_in_swiftui_view` + the FamilyService/MedicationService @MainActor fix.

**C2 — No `@Model` reference held in a `View` struct**
```
Grep: 'let .*: <ModelTypeName>' / stored @Model props in Views/ struct bodies
```
Holding a SwiftData @Model in a View struct → SIGSEGV when the context invalidates it. Extract a value-type snapshot instead. Per `feedback_swiftdata_model_in_swiftui_view`. Flag P0.

---

### Category D — Security & Triggers (P1–P2)

**D1 — No `user_id` passed in Supabase queries**
```
Grep: '\.eq\("user_id"' , 'user_id:' in Services/ query builders
```
RLS uses `auth.uid()` automatically. Passing `user_id` = either redundant or an RLS-bypass smell. Flag per CLAUDE.md hard rule. P1.

**D2 — Realtime channel filter is NOT treated as the auth gate**
```
Grep: 'realtime.channel' , 'onPostgresChange' , 'filter:' in DoseRealTimeManager
```
The client-side `filter: family_id=eq.{UUID}` is a perf hint, not security. Confirm the code does not assume the filter authorizes — RLS `is_family_member()` is the gate (per `supabase-layer.md` Realtime Security). Flag P2 if a comment/code implies the filter is the protection.

**D3 — Sync queue processed on BOTH foreground AND connectivity-restore**
```
Grep: 'scenePhase' , 'NetworkMonitor' , 'needsSync == true' fetch, '.task' / observers in SyncService
```
`needsSync == true` records must drain on app foreground AND on connectivity change. Missing either trigger = queued mutations stall until the other event fires. Flag P1 if only one trigger exists.

**D4 — No PII in sync logs**
```
Grep: 'logger.*\(.*name|logger.*email|logger.*medication' in Services/
```
`os.Logger` must not log emails, names, medication names (Critical Test Case #68). P2.

---

## Run Procedure

1. **Preflight** — confirm `rg` (ripgrep) available; fall back to `grep -rn` if not.
2. Run each rule's grep against its scope. Collect hits with `file:line`.
3. For each hit, READ the surrounding 10–20 lines — most rules need context (A1/A2/A3 especially: a hit is only a defect if the success/failure handling is wrong).
4. Classify P0–P3. **Do not** report a grep hit as a finding without reading the code — false positives here erode trust (per honesty-constraints §1).
5. Cross-reference Critical Test Cases #1, #11a, #12, #13, #14 — if a P0 sync path has no covering Swift Testing suite, note it as a test gap, not just a code defect.
6. Write `DoseSync/sync-audit-report.md`. Summarize P0 count first.

## Verdict format

```
SYNC-AUDIT VERDICT: <CLEAN / DEFECTS FOUND>
P0: N  P1: N  P2: N  P3: N
Test gaps: <list of P0 paths with no covering suite>
```

P0 > 0 → merge-blocker per `dev-qa-loop.md` (BLOCKED verdict, data-integrity risk).

## What this skill does NOT do

- Does not run the app or simulator (that's `audit-ui` / physical QA).
- Does not write tests (that's `swift-testing` / `test-gaps`) — it flags missing coverage.
- Does not touch Supabase schema/RLS (that's backend-developer + `supabase-layer.md`).
- Does not fix — read-only audit. Findings route to `inbox-ios-developer.md`.
