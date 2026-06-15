# Workflow Audit Report: Stuffolio

> [!NOTE]
> This is a **sample workflow-audit report** demonstrating the 5-layer audit output. It uses real Stuffolio findings from a session circa build 28 (April 2026). The findings shown are illustrative — most have been resolved in subsequent builds. Read this file end-to-end to see the report shape; live runs land at `.workflow-audit/` in your project root.

**Date:** 2026-04-15
**Project:** Stuffolio (Universal app: iOS 17+, iPadOS 17+, macOS 14+)
**Build:** 28
**Layers run:** All 5 (Discovery → Trace → Issues → Evaluate → Data Wiring)
**Files scanned:** 312 SwiftUI views, 47 view models, 22 managers
**Audit duration:** ~22 minutes

## Summary

| Layer | What was found |
|---|---|
| **1. Discovery** | 4 tab-bar entries (iOS), 11 sidebar entries (iPad/macOS), 22 sheet triggers, 47 navigation links, 13 notification-driven nav contexts, 6 deep-link handlers, 18 quick-find entries |
| **2. Flow Tracing** | 8 critical paths traced end-to-end. 6 complete, 2 with breaks |
| **3. Issue Detection** | 14 findings: 2 critical, 7 high, 4 medium, 1 low |
| **4. Semantic Evaluation** | 3 broken promises, 2 buried primary actions, 1 dismiss trap |
| **5. Data Wiring** | 1 mock-data instance, 2 unwired-model fields, 0 platform parity gaps |

## Issue Rating Table

All findings sorted by Urgency then ROI:

| # | Finding | Category | Urgency | Risk: Fix | Risk: No Fix | ROI | Blast Radius | Fix Effort |
|---|---------|----------|---------|-----------|-------------|-----|-------------|------------|
| 1 | DashboardView "Add Item" card opens generic ItemPicker instead of new-item form | Promise-Scope Mismatch | 🔴 Critical | ⚪ Low | 🟡 High | 🟠 Excellent | ⚪ 1 file | Trivial |
| 2 | RMARecordsListView empty state is a blank screen on iPad | Empty State Missing | 🔴 Critical | ⚪ Low | 🟡 High | 🟠 Excellent | ⚪ 1 file | Small |
| 3 | iPad sidebar "Settings" → Privacy → tap nothing → user stuck | Dead End | 🟡 High | ⚪ Low | 🟡 High | 🟠 Excellent | ⚪ 1 file | Small |
| 4 | Notification deep link "open insurance profile X" loses item context on macOS | Context Dropping | 🟡 High | 🟢 Med | 🟡 High | 🟠 Excellent | 🟢 2 files | Small |
| 5 | EditItemView Save button hidden below scroll fold on iPhone SE | Buried Primary Action | 🟡 High | ⚪ Low | 🟢 Medium | 🟠 Excellent | ⚪ 1 file | Small |
| 6 | Backup restore sheet shows only "Cancel" — no path forward without selection | Dismiss Trap | 🟡 High | ⚪ Low | 🟢 Medium | 🟢 Good | ⚪ 1 file | Small |
| 7 | "Check for Recalls" CTA on item detail opens generic recall search | Promise-Scope Mismatch | 🟡 High | 🟢 Med | 🟢 Medium | 🟢 Good | 🟢 2 files | Small |
| 8 | iPad sheet routing on macOS uses `.sheet`; iOS uses `.fullScreenCover` | Sheet Presentation Asymmetry | 🟡 High | 🟢 Med | 🟢 Medium | 🟡 Marginal | 🟢 4 files | Medium |
| 9 | DonationView "Estimated tax value" shows hardcoded $0.00 instead of computed FMV | Mock Data | 🟢 Medium | 🟢 Med | 🟢 Medium | 🟢 Good | ⚪ 1 file | Small |
| 10 | InsuranceProfile.policyNumber stored but not surfaced anywhere in UI | Unwired Data | 🟢 Medium | ⚪ Low | 🟢 Medium | 🟢 Good | ⚪ 1 file | Small |
| 11 | "Manage Coverage" entry point on item detail leads to general settings | Wrong Destination | 🟢 Medium | 🟢 Med | 🟢 Medium | 🟢 Good | 🟢 2 files | Small |
| 12 | Photo capture sheet on iPad has no "Done" button; only swipe-down to dismiss | Gesture-Only Action | 🟢 Medium | ⚪ Low | 🟢 Medium | 🟢 Good | ⚪ 1 file | Trivial |
| 13 | Loading spinner during AI Stuff Scout has no cancel button (max 30s) | Loading State Trap | 🟢 Medium | 🟢 Med | 🟡 Marginal | 🟡 Marginal | ⚪ 1 file | Small |
| 14 | Two paths to "Export Backup": Settings > Backup AND Backup tab on iPad | Inconsistent Pattern | ⚪ Low | 🟢 Med | ⚪ Low | 🟡 Marginal | 🟢 3 files | Medium |

---

## Layer 1 — Pattern Discovery

Inventoried every UI entry point in the project. Below is the abbreviated catalog (full inventory in `.workflow-audit/layer1-entry-points.yaml`).

### Tab Bar (iOS)
- Dashboard
- My Products
- Tools
- Settings

### Sidebar (iPad/macOS)
- Dashboard, My Products, Insights, Stuff Scout, Tools, Backup, Reports, Activity, Settings, Search, Help

### Sheet Triggers (22)
- Add Item (4 entry points: Dashboard quick-add, MyProducts toolbar, Tools "Quick Add", deep link)
- Edit Item (1 entry point: detail toolbar)
- AI Product Assistant (3 entry points: Tools, item detail, Stuff Scout result)
- Stuff Scout sheet, photo picker, RMA edit, Insurance edit, Donation record, Legacy wishes, etc.

### Notification-Driven Nav (13)
- Warranty expiry (`.warrantyExpiringSoon`, `.warrantyExpired`)
- Maintenance due (`.maintenanceTaskDue`)
- Recall found (`.recallFound`)
- Stuff Scout result ready (`.stuffScoutResultReady`)
- Backup completion (`.backupCompleted`, `.backupFailed`)
- Family sharing events (4 notification types)
- Widget interactions (3)

### Deep-Link Handlers (6)
- `stuffolio://item/<id>` → ItemDetailView
- `stuffolio://insurance/<policyId>` → InsuranceDetailView (broken on macOS — see finding #4)
- `stuffolio://donation/<recordId>` → DonationDetailView
- `stuffolio://stuff-scout` → StuffScoutView
- `stuffolio://settings/<section>` → SettingsView
- `stuffolio://backup/restore` → BackupRestoreView

---

## Layer 2 — Flow Tracing

Traced 8 critical user paths. Each is annotated with completeness.

### Path 1 — "Add Item from Dashboard" ✅ Complete

```
Dashboard (.dashboardEntry) → DashboardView "+ Add Item" card →
  AddItemSheet (.fullScreenCover on iOS, .sheet on iPad/macOS) →
  user fills form → save → ItemDetailView for new item
```

Works end-to-end on all 3 platforms.

### Path 2 — "Restore Backup" ❌ Break (finding #6)

```
Settings → Backup → "Restore from File" →
  fileImporter sheet → user cancels →
  ⚠️ stuck: no "back" or "manual restore" path; only "Cancel" closes the sheet
```

The fileImporter has only Cancel and no clear "I changed my mind" UX. Users tapping Cancel get returned to the Backup screen with no indication of next steps.

### Path 3 — "Open Item from Recall Notification" ❌ Break (finding #4)

```
iOS: Notification tap → notification.userInfo["itemID"] →
  AppNavigationView routes to ItemDetailView for that item ✅
macOS: Notification tap → notification.userInfo["itemID"] as Any →
  cast fails silently → routes to generic "My Products" list
```

The macOS NotificationCenter strips the `PersistentIdentifier` type when forwarding through the dictionary. Identical to RS-013 in the radar-suite codebase but for a different notification.

### Paths 4-8 (abbreviated)
- "Edit Insurance Profile" ✅ Complete
- "Add Maintenance Task" ✅ Complete
- "Stuff Scout from Existing Item" ✅ Complete
- "Family Share Item" ✅ Complete
- "Export to PDF" ✅ Complete

---

## Layer 3 — Issue Detection (14 findings)

### Finding 1 — Promise-Scope Mismatch — `DashboardView.swift:142`

🔴 **Critical** — The "+ Add Item" card visually promises a direct path to creating a new item. Tapping it on iPad opens `ItemPicker` (which is for selecting an *existing* item to view), not `AddItemSheet`. Users who tap "Add Item" and see a list of items they already own are confused.

**Current code:**
```swift
DashboardCard(title: "Add Item", icon: "plus.circle.fill") {
    showingItemPicker = true  // <-- wrong sheet
}
```

**Suggested fix:**
```swift
DashboardCard(title: "Add Item", icon: "plus.circle.fill") {
    showingAddItemSheet = true
}
```

### Finding 2 — Empty State Missing — `RMARecordsListView.swift:88` (iPad only)

🔴 **Critical** — On iPad with no RMA records, the view renders a `List { ForEach(records) { ... } }`. Empty array → blank list with no copy, no graphic, no "+ New RMA" button.

**Current code:**
```swift
List(records) { record in RMARow(record: record) }
```

**Suggested fix:**
```swift
if records.isEmpty {
    EmptyStateView(
        icon: "shippingbox",
        title: "No RMAs Yet",
        message: "Track returns and replacements here.",
        action: ("New RMA", { showingNewRMA = true })
    )
} else {
    List(records) { record in RMARow(record: record) }
}
```

### Finding 4 — Context Dropping — `AppNavigationView.swift:51` (macOS)

🟡 **High** — Same root cause as Path 3 above. The notification's `userInfo["itemID"]` is sent as `as Any` from the poster (line 273 of AIProductAssistantView.swift) and cast as `as? PersistentIdentifier` on the receiver. The `as Any` wrapper combined with `[String: Any]` causes the cast to silently fail on macOS but not iOS.

This is the documented `RS-013` pattern from the radar-suite ledger, surfaced again here for a different notification (the recall notification, not Stuff Scout).

**Current code (poster, AIProductAssistantView.swift:273):**
```swift
NotificationCenter.default.post(
    name: .recallFound,
    object: nil,
    userInfo: [
        "itemID": item.persistentModelID as Any,  // <-- type stripped
        ...
    ]
)
```

**Suggested fix:**
```swift
NotificationCenter.default.post(
    name: .recallFound,
    object: nil,
    userInfo: [
        "itemID": item.persistentModelID,  // <-- preserves type
        ...
    ]
)
```

### Finding 5 — Buried Primary Action — `EditItemView.swift:312`

🟡 **High** — On iPhone SE (568pt height), the `Save` button at the bottom of `EditItemView`'s scrolling form is below the keyboard fold AND below the visible content fold. Users who finish editing fields can't see the Save button without scrolling past the keyboard.

**Suggested fix:** Add a primary save button to the toolbar:
```swift
.toolbar {
    ToolbarItem(placement: .confirmationAction) {
        Button("Save") { save() }.fontWeight(.semibold)
    }
}
```

(Findings 6-14 abbreviated for sample purposes; full report file at the path above contains all 14 with current-code + suggested-fix per finding.)

---

## Layer 4 — Semantic Evaluation

Reviewing the project from the user's perspective — the layer that asks "did the user get what the UI promised?"

### Discoverability

| Feature | Tap depth | Visible from | Verdict |
|---|---|---|---|
| Add Item | 1 | Dashboard, MyProducts, Tools | ✅ Excellent |
| Stuff Scout | 1-3 | Tools, Insights, item detail | 🟡 Inconsistent (different paths from different surfaces) |
| Recalls | 2 | Tools | 🟢 Adequate |
| RMA tracking | 4 | Tools → RMAs (then user has no idea what RMA means) | 🟡 Acronym is jargon |
| Family Sharing | 3 | Settings → Family → Share | 🟢 Adequate |
| Insurance Profiles | 5 | Settings → Insurance → Add → fields → save → linked | 🔴 Buried |

**Insurance is significantly buried.** Users with insurance documentation rarely find this feature without explicit pointer. Recommend exposing it from item detail directly when the item value crosses an insurance threshold.

### Recovery from Errors

| Error path | Has recovery action | Verdict |
|---|---|---|
| Backup restore failure | "Try again" button + log | ✅ Good |
| Stuff Scout API failure | Cancel + retry | ✅ Good |
| Network unavailable on Recall search | Generic error toast, no retry | 🟡 Add retry |
| Photo permission denied | "Open Settings" button | ✅ Good |
| iCloud not signed in | No path forward (just toast) | 🔴 Add Settings deep link |

---

## Layer 5 — Data Wiring

Verifying that displayed data is real (not mock/hardcoded) and that model fields are surfaced where expected.

### Mock Data (1 finding)

**Finding 9 — `DonationView.swift:142`** displays `"Estimated tax value: $0.00"` regardless of input. The `donation.fairMarketValueInCents` field is set when the donation is recorded but never read by this view.

```swift
Text("Estimated tax value: $0.00")  // <-- hardcoded
// should be: donation.fairMarketValueInCents.formattedAsCurrency
```

### Unwired Data (2 findings)

**Finding 10 — `InsuranceProfile.policyNumber`** is stored on the model and editable in the form, but never displayed in any read-only context. The user has nowhere to see their own policy number after entering it.

**Finding 11 — Companion warranty info on items.** When an item has both an `Item.warranty` (manufacturer) and an `ExtendedWarranty`, only the manufacturer's is shown on the detail view. Extended warranty information is in the model but not in the visible UI.

### Platform Parity (0 findings)

All audited surfaces have feature parity between iOS, iPadOS, and macOS, except where intentional (e.g., context menus where right-click on macOS replaces long-press on iOS).

---

## Recommended Fix Phases

If addressing all 14 findings sequentially, suggested order:

**Phase 1 — Critical UX failures (1, 2)** [~30 min]
The wrong-sheet bug and the blank empty state are the most user-visible. Fix first.

**Phase 2 — Notification context drops + dead ends (3, 4, 6)** [~1 hour]
These break workflows. Findings 3 and 4 share architectural shape (untyped notification payloads); fix together.

**Phase 3 — Promises, buried actions, sheet asymmetry (5, 7, 8, 11)** [~2 hours]
Promise-scope and buried-action findings are individually small but collectively reduce daily friction.

**Phase 4 — Mock data + unwired (9, 10, 12, 13)** [~1.5 hours]
Less critical but worth knocking out before next user testing round.

**Phase 5 — Inconsistent patterns (14)** [defer]
Two paths to "Export Backup" is a classic redundancy that's worth fixing during a broader navigation refactor, not as a standalone change.

---

*Report generated 2026-04-15 by workflow-audit v3.0.0. Full per-layer YAML output in `.workflow-audit/`. Run `/workflow-audit fix` to enter the guided fix flow.*
