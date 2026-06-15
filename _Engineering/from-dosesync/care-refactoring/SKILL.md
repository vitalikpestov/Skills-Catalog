---
name: care-refactoring
description: Pragmatic maintenance refactoring for DoseSync (iOS Swift primary + Supabase BE + Android Kotlin). Use when asked to make the codebase easier to understand, safer to change, or more consistent with existing architecture WITHOUT changing user-visible behavior. A valid result is "No code changes needed". NOT for feature work, NOT for audit findings (IOS-AUDIT-*), NOT for launch blockers. Trigger phrases — "refactor X", "clean up X", "extract Y from Z", "split this file", "consolidate duplication", "improve readability", "/care-refactor".
---

# Care Refactoring — DoseSync

Adapted from upstream care-refactoring skill. DoseSync overrides: mandatory `qa-reviewer` challenge, explicit public-contracts catalog, layer-discipline anchored to existing rule files, composition with `dev-qa-loop.md` + `volume-gate.md`.

Cover: iOS (primary), Supabase BE (canonical `Supabase/EdgeFunctions/`), Android (secondary). Stack: Swift 5.9+/SwiftUI/MVVM/@Observable/SwiftData • Supabase (auth, realtime, postgres, edge functions) • Kotlin/Compose/Hilt/Room/Supabase-kt/Coroutines+Flow.

Valid outcome: `No code changes needed`.

---

## §0. When NOT to use

Auto-skip skill, switch to other workflow:

| Request | Route to |
|---|---|
| Audit finding (Wave 1-4 tickets, `IOS-AUDIT-*`, `AND-AUDIT-*`) | Execute against master plan in inbox. NOT refactor — feature fix. |
| Launch blocker (Phase 0/1 master plan) | Straight implementation, no challenge loop. |
| Bug fix | `investigate` skill (Iron Law) or `gsd-debug`. |
| New feature spec | `spec-review-gate.md` PM gate first. |
| ≥ 4h estimated effort | `volume-gate.md` Volume Evidence block mandatory FIRST. |
| Rename + cosmetics only, 1-2 files | `caveman:cavecrew-builder` 1-2 file surgical edit. |
| WelcomeView layout change | **HARD REJECT** — `welcome-screen-locked.md`. |
| Free vs Pro tier framing | **HARD REJECT** — CPO-DEC D-PAYWALL-004. |
| Add Combine / ObservableObject / @Published | **HARD REJECT** — `swift-conventions.md`. |
| Touch RU strings without «Вы»-form check | **HARD REJECT** — `tone-of-voice.md`. |

If trigger phrase matches but task fits another lane → say so, delegate via `delegate` skill, stop.

---

## §1. Operating Rules

- DoseSync rules override generic care-refactoring rules everywhere they conflict.
- Read these first: `.claude/rules/swift-conventions.md`, `supabase-layer.md`, `swiftui-views.md`, `dev-qa-loop.md`, `tests-and-quality.md`, `volume-gate.md`, `tone-of-voice.md`, `github-workflow.md`.
- For Android: `Android/DESIGN.md` + `android-dev` skill + `android-skills:*` family.
- Check `git status --short --branch` before editing. Preserve uncommitted founder work.
- Push immediately after commit (per `github-workflow.md` — PM-automation does `git reset --hard origin/main` periodically).
- Never modify these without explicit founder sign-off (auto-rejected by lint/CI):
  - `Views/Onboarding/WelcomeView.swift` floating-MedCards composition
  - `Localizable.xcstrings` RU strings without «Вы»-form check
  - Supabase RLS policies (must use `auth.uid()`, never accept `user_id` param)
  - MLAR vs MAR copy claims
  - Double-dose protection guards
  - `Android/app/src/main/java/com/dosesync/android/notification/` (BroadcastReceiver + goAsync pattern)
  - `Supabase/EdgeFunctions/` canonical paths (deployed) — NOT inner mirror `DoseSync/DoseSync/Supabase/EdgeFunctions/`

---

## §2. DoseSync public contracts (preserve unconditionally)

| Contract | Why locked |
|---|---|
| Supabase RLS policies + `auth.uid()` flow | Medical PHI — RLS = real security layer; `swift-conventions.md` |
| Edge Function HTTP signatures (path, body, headers, CORS allowlist) | iOS + Android both depend; canonical = `Supabase/EdgeFunctions/`, mirror NOT deployed |
| Push payload fields (`interruption-level`, `apns-priority: 10`, `apns-expiration`, `content-available: 1`) | APNs delivery + N1-N11 + Critical Alerts entitlement |
| StoreKit product IDs (`dosesync.solo.weekly`, `dosesync.family.yearly`, etc.) | ASC-registered, refund risk if renamed |
| SwiftData `@Model` schema + `@Attribute(.unique)` + `@Relationship` rules | Migration risk; v2 schema bump = separate spec |
| `needsSync: Bool` offline-first contract | SyncService depends; server-wins for `dose_records` |
| Notification escalation chain T+0 → T+15 → T+45 → T+120 | GrandparentMode deal-breaker per VoC v3 §16.5 + N5 |
| MLAR (logging-adherence) wording, NOT MAR | HIPAA red line; Cochrane 2020 unsupported |
| Guest access zero-signup flow | Pebbi differentiation (CLAUDE.md + Q22) |
| Free tier = NONE (hard paywall only) | CPO-DEC D-PAYWALL-004; no Free vs Pro framing |
| Trial = 7 days, Annual ONLY (Weekly = direct buy) | CPO-DEC PAYWALL-TRIAL-ANNUAL-ONLY-1 |
| Brand teal AccentColor (no system blue leak) | DS v1.0 + Wave 2 fixes |
| «Вы»-form RU copy (no «ты») | `tone-of-voice.md` + CI lint `check_ru_tone.py` |
| Room schema + DAO contracts (Android) | Migration risk; mirrors SwiftData schema |
| `ALLOWED_PARAMS` in `AnalyticsService` (Android) | Prevents PII leak to analytics |

If refactor risks ANY of above → `NARROW_SCOPE` or `NO_CHANGES_NEEDED`. No exceptions.

---

## §3. Discovery (before scope proposal)

Read in this order:

1. `git status --short --branch` + `git log -10 --oneline` — uncommitted work + recent context
2. `CLAUDE.md` root + nearest module CLAUDE.md
3. Touched layer's rule file (`swift-conventions.md` / `supabase-layer.md` / `swiftui-views.md` / `Android/DESIGN.md`)
4. Relevant tests (`DoseSyncTests/Unit/<Domain>/` or `Android/app/src/test/`)
5. Target file + 1-hop callers via grep

For broad discovery (> 3 files) → delegate to `Explore` or `caveman:cavecrew-investigator` agent. Compact `path:line → why it matters` map only.

Avoid:
- Touching files modified in `git status` unless they're the refactor target
- Reading `Zoom/`, `_resources/`, `Personal/` — out of scope per Documents CLAUDE.md
- Reading inner mirror `DoseSync/DoseSync/Supabase/EdgeFunctions/` — NOT deployed; canonical = `Supabase/EdgeFunctions/`

---

## §4. Layer responsibilities (anchor)

Map every refactor candidate to layer owner. Wrong-layer code = main refactor opportunity.

### 4.1 iOS

| Layer | Owns | Smell to fix |
|---|---|---|
| `Views/` (SwiftUI) | Render state, accept input, dispatch to ViewModel | Supabase call in `body` or `.task {}`; business decision; date math inline; locale-specific copy in code; force unwrap `!` w/o `// JUSTIFIED:` |
| `ViewModels/` (`@Observable final class`) | Flow orchestration, state transitions, calls Services | Direct Supabase/StoreKit/Push call; ObservableObject/@Published leak; Combine usage |
| `Services/` (DI singletons) | Supabase/StoreKit/Push/Sync, ONE domain per service | Multi-domain god service; missing `throws` or `Result`; print() instead of `Logger` |
| `Models/` (`@Model`) | SwiftData schema + value DTOs | Business logic in @Model; missing `@Attribute(.unique)` on id |
| `Utilities/` | Pure helpers, formatters, extensions | Hidden state; framework imports; non-deterministic helpers |
| `AppIntents/` | Siri/Shortcuts thin wrappers | Business logic; bypass ViewModel |

### 4.2 BE (Supabase)

| Layer | Owns | Smell to fix |
|---|---|---|
| `EdgeFunctions/` (canonical, NOT inner mirror) | HTTP handler, auth, validation, calls SQL/external API | CORS `*` wildcard (must be allowlist); inline business rule that belongs in SQL; missing `apns-priority`/`interruption-level`; absent rate limit; PHI in payload |
| `Migrations/` | Schema changes, mirror to all 3 paths if applies | Missing `SET search_path = pg_catalog, public` on SECURITY DEFINER; CHECK constraint on RLS path; non-idempotent; missing rollback |
| Postgres functions | Business rules in SQL when reused across triggers + EF | Duplicated logic in EF + function; missing search_path; recursive RLS via function (use SECURITY DEFINER helper) |
| RLS policies | Use `auth.uid()`, never accept `user_id` param | `auth.uid() = user_id` AND param check (param redundant); circular dependency between two tables |

### 4.3 Android

| Layer | Owns | Smell to fix |
|---|---|---|
| Composable / UI | Render `UiState`, emit `Event`/`Action` to ViewModel | Business logic in Composable; `collectAsState()` instead of `collectAsStateWithLifecycle()`; missing `key` in LazyColumn; lambda captures causing recomposition; logic in `LaunchedEffect`/`SideEffect` |
| ViewModel | UI state (`StateFlow<UiState>`), one-shot effects (`SharedFlow<Effect>`), coordinate use cases/repos | Direct Room/Supabase call; `MutableStateFlow` exposed publicly; multiple `_uiState.update {}` for atomic change; `GlobalScope.launch`; missing `viewModelScope` cancellation |
| Repository | Data access coord, offline-first (`needsSync`), Supabase SDK + Room | Returns Room entity instead of domain model; conflict resolution in ViewModel; optimistic update without rollback |
| Room DAO | SQL only | Business logic; Supabase call; Flow without `distinctUntilChanged()` when N+1 |
| Domain / UseCase | Pure business rules, framework-independent | Android `Context` import; framework type leak |
| Hilt Modules | Wiring only | Logic; `@Singleton` with mutable UI state that should be `@ViewModelScoped` |
| Analytics | Event tracking | PII in params (must match `ALLOWED_PARAMS`); event fired before op success; duplicate tracking |

### 4.4 Cross-cutting smells (any layer)

- Duplicated business rule across iOS + BE + Android (single source: Postgres function OR domain class)
- `print()` (iOS) / `Log.d` w/o tag (Android) — use `Logger(subsystem:category:)` / `Timber`
- Force unwrap `!` (Swift) or `!!` (Kotlin) without `// JUSTIFIED:` comment
- Hardcoded strings — use `Localizable.xcstrings` / `strings.xml`
- Missing `reduceMotion` guard on animation (iOS `swiftui-views.md`)
- Notification payload built in two places — single builder in `NotificationService`
- RLS check duplicated in EF code + RLS policy — keep in RLS only

---

## §5. Scope Proposal (mandatory output before any edit)

Propose 1-3 scopes MAX. NEVER more. For each:

```markdown
### Scope N: <one-line name>

- **Layer:** iOS / BE / Android (per §4)
- **File(s):** `path:line-range` (verified via Read, not guessed)
- **Smell:** <concrete; reference §4 layer violation>
- **Preserved contract:** <which §2 invariant stays untouched>
- **Smallest useful change:** <one sentence; should fit single commit>
- **Risk:** <what breaks if wrong>
- **Validation signal:** <which test / which manual QA from tests-and-quality.md Q#/N#/Critical-#>
- **Characterization test:** [exists | new test needed: <test name>] | disproportionate: <reason>]
- **Effort estimate:** < 4h (if ≥ 4h → reroute to volume-gate.md first)
```

Stop. Wait for §6.

---

## §6. Challenge Checkpoint (MANDATORY, not optional)

DoseSync override: challenge is mandatory, not "if subagents available".

Spawn `qa-reviewer` agent (read-only) with prompt:

> Read proposed care-refactoring scope below. Do NOT suggest fixes. Answer 7 questions:
> 1. Is this refactor worth doing vs. backlog deferral?
> 2. Is scope small enough (single commit, < 4h)?
> 3. Which §2 DoseSync public contract could accidentally break?
> 4. Is there a simpler change that gets 80% of the value?
> 5. Is this overengineering? (Adding interface/factory/protocol without current caller diversity = yes.)
> 6. What characterization test from `tests-and-quality.md` Q#/N#/Critical-# protects the behavior? If none → propose new test or declare disproportionate.
> 7. Final verdict: `PROCEED_WITH_SCOPE` / `NARROW_SCOPE` / `NO_CHANGES_NEEDED` / `SEPARATE_PRODUCT_TASK`

Max 2 disagreement rounds main ↔ qa-reviewer. After round 2 → take qa-reviewer's verdict.

End checkpoint with exactly one of:

- `PROCEED_WITH_SCOPE` → §7
- `NARROW_SCOPE` → revise scope, re-run §6
- `NO_CHANGES_NEEDED` → final report `No useful maintenance refactor found`. Skill ends.
- `SEPARATE_PRODUCT_TASK` → file ticket via `delegate` skill. Skill ends.

NO code edits before checkpoint ends with `PROCEED_WITH_SCOPE` or `NARROW_SCOPE`.

---

## §7. Characterization Tests

Lock behavior before production edit. Test must fail on accidental behavior change.

### 7.1 iOS

| Target layer | Test type | Location |
|---|---|---|
| `Services/` (Supabase / StoreKit / Push) | Unit test w/ mock client | `DoseSyncTests/Unit/Services/` |
| `ViewModels/` | State-transition unit test | `DoseSyncTests/Unit/ViewModels/` |
| `Models/` (`@Model`) | SwiftData persistence + relationship test | `DoseSyncTests/Unit/Models/` |
| `Views/` (only if extracting) | Snapshot test OR manual Q-row | `DoseSyncTests/UI/Snapshots/` or `Q#` |

### 7.2 BE

| Target | Test type | Location |
|---|---|---|
| EF | curl integration test | `Supabase/tests/` |
| RLS | SQL test via service_role bypass + `auth.uid()` override | `Supabase/tests/rls/` |
| Migration | Round-trip on Supabase branch via `mcp__claude_ai_Supabase__create_branch` | Branch test |
| Postgres function | `EXECUTE` test in SQL | `Supabase/tests/functions/` |

### 7.3 Android

| Target | Test type | Tooling |
|---|---|---|
| ViewModel | StateFlow / SharedFlow assertion | JUnit5 + Mockk + `app.cash.turbine.test {}` |
| Repository | Mock Supabase + in-memory Room | `Room.inMemoryDatabaseBuilder` |
| DAO | Query correctness | `Room.inMemoryDatabaseBuilder` |
| Domain / UseCase | Pure unit test | JUnit5 |
| Composable (only if extracting) | Compose UI test | `@get:Rule createComposeRule()` |

### 7.4 Run order

1. Write/identify characterization test
2. Run against current code → confirm GREEN
3. THEN edit production code
4. Re-run → confirm still GREEN (behavior preserved) OR RED with intentional change documented

### 7.5 Disproportionate cases (declare explicitly, don't fake it)

- Pure-cosmetic rename (no behavior surface)
- Layer move with zero call-site change
- Comment / docstring cleanup
- Dead-code removal (per Wave 1 DC-* findings — characterization = `grep` proves zero callers)

Do NOT encode known bugs as desired behavior. If characterization test surfaces real bug → stop refactor, file `IOS-BUG-*` / `AND-BUG-*` ticket, escalate via `delegate`.

---

## §8. Implementation Loop

For each accepted scope:

1. Branch off `main` only if multi-file > 3 files. Else commit directly to working branch.
2. Make minimal connected diff. ONE commit per scope.
3. Move decisions UP to owner layer (per §4). Don't patch symptoms in leaf adapters.
4. Update tests that already covered the path; don't add aspirational tests.
5. Run validation:

   **iOS:**
   ```bash
   cd $PROJECT_ROOT/DoseSync
   xcodebuild -project DoseSync/DoseSync.xcodeproj -scheme DoseSync \
     -destination 'platform=iOS Simulator,id=397BB07F-A869-4E70-8396-D64474119B4F' build
   # OR via MCP: mcp__XcodeBuildMCP__build_sim
   swiftlint
   xcodebuild test ... # focused: changed module only
   python3 scripts/check_ru_tone.py        # if RU strings touched
   python3 scripts/check_xcstrings_coverage.py  # if xcstrings touched
   ```

   **BE:**
   ```bash
   # If migration: test on Supabase branch first
   # mcp__claude_ai_Supabase__create_branch → apply_migration → execute_sql → reset_branch
   # If EF: deploy + curl integration
   supabase functions deploy <name> --project-ref <ref>
   curl -X POST https://<project>.supabase.co/functions/v1/<name> \
     -H "Authorization: Bearer $SERVICE_ROLE" -d '...'
   ```

   **Android:**
   ```bash
   cd $PROJECT_ROOT/Android
   ./gradlew assembleDebug
   ./gradlew :app:testDebugUnitTest
   ./gradlew detekt
   ```

6. Commit with conventional format. **Push immediately** (`github-workflow.md`).

### Commit message template

```
refactor(<layer>): <scope name> — preserve <contract>

Origin: care-refactoring skill §6 challenge passed.
Tests: <characterization test name> ran GREEN before + after.
Contracts preserved: <list from §2>
```

---

## §9. Avoid (DoseSync-specific)

### Universal
- Rewriting from scratch
- Adding interface / Protocol / Factory / Mediator without 2+ concrete impls (premature abstraction)
- Splitting simple code into many files just to look clean
- Leaving TODO / FIXME instead of completing the refactor
- Cross-file refactor in same commit as feature work
- Doc churn unrelated to refactor

### iOS-specific
- Introducing Combine (only async/await per `swift-conventions.md`)
- Introducing UIKit beyond `ASAuthorizationAppleIDButton` exception
- Adding `ObservableObject` / `@Published` (only `@Observable`)
- Adding `print()` (only `os.Logger(subsystem:category:)`)
- Adding force unwrap `!` without `// JUSTIFIED:` comment
- Splitting `Service` into 2 services without 2+ distinct call-site clusters
- Adding new feature flag without `growthbook-swift`
- Touching `WelcomeView.swift` floating MedCards (HARD REJECT — `welcome-screen-locked.md`)
- Editing inner mirror `DoseSync/DoseSync/Supabase/EdgeFunctions/` (NOT deployed)
- Removing `needsSync` flag or optimistic local-write pattern
- Replacing SwiftData with Core Data or third-party ORM
- Adding new RU string without «Вы»-form
- Touching MLAR copy and changing to MAR (tone-of-voice red line)

### BE-specific
- CORS `*` wildcard (must be allowlist)
- Skipping `SET search_path = pg_catalog, public` on SECURITY DEFINER
- Recursive RLS via subquery (use SECURITY DEFINER helper function)
- EF without `apns-priority` / `interruption-level` on dose push
- EF without rate limit on user-scoped push fan-out
- PHI in APNs payload (use deep-link + in-app fetch instead)
- Schema change without migration mirror across all 3 paths

### Android-specific
- `GlobalScope.launch` / unscoped coroutine
- Exposing `MutableStateFlow` / `MutableSharedFlow` from ViewModel
- Moving domain logic into Room DAOs or Supabase calls
- Touching `Android/.../notification/` BroadcastReceiver + goAsync without explicit permission (critical path)
- `collectAsState()` instead of `collectAsStateWithLifecycle()`
- `runBlocking` on main thread
- `Timber.d` / `Timber.e` with PII (email, medication name, user ID) — violates `ALLOWED_PARAMS`
- Analytics event fired before op success confirmation
- Hilt `@Singleton` with mutable UI state (should be `@ViewModelScoped`)

---

## §10. Pre-Final Review (self-audit before report)

Walk diff as fresh reviewer + apply `dev-qa-loop.md` VERDICT logic:

- [ ] Behavior preserved per §7 characterization test (PASS / FAIL)
- [ ] Scope stayed ≤ original proposal (no scope creep)
- [ ] §2 public contracts unchanged
- [ ] §4 layer responsibilities respected
- [ ] §9 avoid-list clean
- [ ] iOS: `swift build` green 0 warnings, `swiftlint` 0 violations
- [ ] iOS: `check_ru_tone.py` exit 0 (if RU touched), `check_xcstrings_coverage.py` exit 0 (if xcstrings touched)
- [ ] BE: migration tested on Supabase branch; EF curl integration green; RLS test green
- [ ] Android: `assembleDebug` green, `testDebugUnitTest` green, `detekt` 0 violations
- [ ] `ALLOWED_PARAMS` in Android `AnalyticsService` still covers all logged params
- [ ] No new TODO / FIXME left behind
- [ ] No doc churn unrelated to refactor

VERDICT logic:
- All checks PASS → commit + report
- Any FAIL → revert your own changes only, report `No useful maintenance refactor found — <reason>`

If diff shrunk during loop = good sign. If diff grew = red flag → consider revert.

---

## §11. Final Report

Output single markdown block:

```markdown
## Care-Refactor Report — <date>

**Overall result:** [no changes | changes made | partial validation]
**Layer:** iOS | BE | Android
**Scopes inspected:** N
**Challenge verdict:** PROCEED_WITH_SCOPE | NARROW_SCOPE | NO_CHANGES_NEEDED | SEPARATE_PRODUCT_TASK
**Scopes shipped:** N

### What improved
- <scope 1>: <why future work easier>

### §2 Contracts preserved
- <invariants verified untouched>

### Characterization coverage
- <test name>: added | reused | disproportionate: <reason>

### Validation
- Primary: <build / lint / xcstrings / detekt> — <status>
- Secondary: <tests run> — <pass/fail counts>
- Manual QA from tests-and-quality.md: <Q# / N# / Critical-# if relevant>

### Docs
- [ ] No doc changes (default)
- [ ] Updated <file> because <durable architecture/contract changed>

### Remaining risks
- <risk + suggested follow-up>

### Commit message (suggested)
refactor(<layer>): <scope> — preserve <contract>

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

---

## §12. Composition with other DoseSync rules

| Other rule | Relation |
|---|---|
| `volume-gate.md` | This skill REPLACES gate for refactor-only work < 4h. ≥ 4h → exit skill, gate first. |
| `dev-qa-loop.md` | Challenge checkpoint §6 = pre-VERDICT gate. Final review §10 = qa-reviewer's actual VERDICT. |
| `spec-review-gate.md` | Does NOT apply (no role/auth/access change in refactor scope by definition). If scope touches those → exit skill. |
| `oss-first-policy.md` | If refactor swaps custom code → OSS lib, run OSS-first §1-3 procedure inside §6 challenge. |
| `tests-and-quality.md` | Q-checklist + N-checklist + Critical-# = characterization test catalog. |
| `tone-of-voice.md` | CI `check_ru_tone.py` runs in §8 validation, blocks merge. |
| `welcome-screen-locked.md` | HARD REJECT WelcomeView floating MedCards refactor. |
| `competition-verification.md` | Does NOT apply (no new feature / new ICP). |
| `physical-device-testing.md` | If validation requires physical iPhone (APNs/Critical Alerts/Live Activity/haptics) → file in `inbox-ceo-physical.md`, not auto-run. |
| `inbox-archive-policy.md` | Skill report goes to inbox only if SEPARATE_PRODUCT_TASK verdict; closed refactors do NOT bloat inbox. |

---

## §13. Versioning

- v1.0 — 2026-06-04 — initial Android-only version (Kotlin/Compose/Hilt/Room focus).
- v2.0 — 2026-06-04 — full DoseSync adaptation. Owner: PM. Added: iOS primary layer §4.1, BE Supabase layer §4.2, universal §0 when NOT to use, §2 public contracts catalog (14 invariants), mandatory `qa-reviewer` challenge §6 (was "if subagents available"), composition table §12 with all DoseSync rules, BE-specific §9 avoid-list (CORS, search_path, RLS recursion, APNs headers, rate limit, PHI), iOS-specific §9 avoid-list (Combine, UIKit, ObservableObject, print, force unwrap, welcome-screen-locked, MLAR vs MAR, «Вы»-form), characterization test layers §7.1-§7.3.
- Review cadence: quarterly OR after any care-refactor that broke a §2 contract (retro trigger).
