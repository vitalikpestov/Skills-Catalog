---
name: ascii-wireframe
description: >
  Generate precise ASCII wireframes before writing any code, slides, SQL, or workflow config.
  Use this skill whenever the user asks to build a UI, dashboard, landing page, presentation deck,
  database schema, automation workflow, or any structured artifact where layout and structure matter.
  Also trigger when the user says "wireframe", "mockup", "sketch the layout", "plan the structure",
  "draw the interface", "ASCII diagram", or describes a multi-section interface. This skill prevents
  Claude from guessing layout decisions by making every structural choice visible and editable
  before any code is written. Even if the user jumps straight to "build me a dashboard" without
  mentioning wireframes, use this skill — the wireframe-first approach saves significant iteration time.
---

# ASCII Wireframe — Sketch First, Build Second

> Created by [Vitalik Pestov](https://www.linkedin.com/in/vitalik-bd-in-web3/) — based on the ASCII wireframing methodology for AI-assisted development.

When a user describes an interface, schema, workflow, or presentation in words, you fill in the gaps yourself — guessing proportions, element placement, hierarchy, and missing details. The result looks polished but doesn't match what the user actually had in mind.

ASCII wireframes eliminate that guesswork. You work from a visual blueprint, not a text interpretation. Every layout decision is explicit. The user gets accuracy on the first build instead of 30 minutes of corrections.

## Core Principle

**Draw first, build second.** Changes at the ASCII stage cost nothing. Changes at the code stage cost everything.

## The Three-Step Process

Every task follows the same three steps, regardless of what you're building:

### Step 1 — Sketch, Don't Describe

Generate a detailed ASCII wireframe of the requested artifact. Use box-drawing characters and arrows to show structure, relationships, and proportions. Output ONLY the ASCII diagram — no code, no implementation, no configuration.

The wireframe must make every layout decision explicit:
- Relative widths and proportions (e.g., "sidebar 15%, main content 85%")
- Element placement and hierarchy
- Relationships and flow between components
- Labels for every block, button, column, and section
- Specific data examples where relevant (sample values, column names, row content)

**Prompt pattern:**
```
Before writing any code, generate a DETAILED ASCII wireframe of [thing].

REQUIREMENTS:
- Use box-drawing characters for structure
- Include EVERY major element and component
- Show relative sizes and proportions (e.g., sidebar 20%, main 80%)
- Add LABELS under each element
- Use ARROWS to show relationships and flow
- Indicate spacing with whitespace or dashed lines (-----)

OUTPUT: ASCII wireframe ONLY — no code, no explanations
```

### Step 2 — Iterate on the Sketch, Not on Code

Present the wireframe to the user and invite feedback. Apply their corrections to the ASCII diagram. This is the cheap iteration phase — no code to rewrite, no broken components, no cascading changes.

Typical iteration requests:
- Adjusting proportions ("make the line chart wider than the pie chart")
- Adding missing elements ("add a pricing section between features and footer")
- Changing data formats ("use status dots instead of text labels")
- Restructuring flow ("both branches should end with Log to DB")

**Prompt pattern:**
```
Update the wireframe with these SPECIFIC changes only:

CHANGE 1: [description]
CHANGE 2: [description]

RULES:
- Apply ONLY these changes — everything else remains identical
- Redraw the ENTIRE wireframe
- Maintain all proportions for unchanged elements
- Keep all labels in place

OUTPUT: Full wireframe with changes applied
```

When redrawing, reproduce the FULL wireframe with the changes applied — don't show just the changed parts. The user needs to see the complete picture.

### Step 3 — Build from the Wireframe as Specification

Once the user approves the wireframe, treat it as the exact specification. Build the artifact matching every detail in the wireframe. Do not invent, add, remove, or rearrange anything that isn't in the approved wireframe.

**Prompt pattern:**
```
Build [the thing] using this wireframe as the EXACT specification.

WIREFRAME:
[paste the approved wireframe]

TECH STACK:
[your stack]

CRITICAL RULES:
1. MATCH LAYOUT EXACTLY — Every position, size, proportion
2. DO NOT INVENT — No colors, buttons, or features not in wireframe
3. PROPORTIONS MATTER — Sidebar 20%, main 80%, etc.
4. TEXT FROM WIREFRAME — Use exact labels and annotations
5. RESPONSIVE — Both desktop and mobile if shown
6. NO PLACEHOLDER LIBRARIES — Use [your framework] + CSS
7. ASK IF AMBIGUOUS — Don't guess

OUTPUT:
- Single-file [type] OR proper structure
- Ready to run immediately
- Include mock data exactly as shown
```

## Domain-Specific Guidance

The three-step process applies universally, but different artifact types have specific wireframing patterns:

### Web Interfaces (Dashboards, Apps, Landing Pages)

Use box-drawing characters to show layout grid. Indicate proportions with explicit percentages or ratios. Show every interactive element with brackets: `[Button]`, `[Search]`, `[+ New]`. Include sample data in tables and cards.

Key things to make explicit in the wireframe:
- Sidebar vs. content area width ratio
- Number of columns for cards/features (3 vs. 4 matters)
- Chart proportions when side by side (60/40, 50/50, etc.)
- Table column names and sample rows
- Which element is highlighted/primary (e.g., "Pro tier highlighted")
- Hero layout (full-width vs. split 50/50)
- Navigation items and their order

Example wireframe structure for a dashboard:
```
+----------------------------------------------------------------------+
| NAVBAR                    [Search]              [Bell] [Avatar]      |
+------+---------------------------------------------------------------+
|      | +----------------+ +----------------+ +----------------+      |
| SIDE | | Revenue        | | Users          | | Churn          |      |
| BAR  | | $48,200        | | 1,842          | | 2.1%           |      |
| 15%  | +----------------+ +----------------+ +----------------+      |
|      | +----------------------------------+ +--------------------+    |
| Dash | | Revenue Over Time                | | Traffic Sources    |    |
| Ana  | | line chart — 60% width           | | pie — 40%          |    |
| Memb | +----------------------------------+ +--------------------+    |
| Rev  | +----------------------------------------------[+ New]---+    |
| Set  | | Recent Members                                        |    |
|      | | Name    | Plan | Date       | Status                  |    |
|      | | Alice   | Pro  | 2026-02-28 | * Active                |    |
|      | +--------------------------------------------------------+    |
+------+---------------------------------------------------------------+
```

### Presentations (Slide Decks)

Show each slide as a labeled box with its layout type. The goal is to prevent the "all slides look the same" problem — every slide should have a visually distinct layout.

Key things to make explicit:
- Slide type label (Title, Stat, Quote, Columns, Table, CTA)
- Content placement within each slide
- Which slides use special layouts (full-bleed image, dark background, split layout)
- Number of columns/items per slide

Example wireframe for a single slide:
```
SLIDE 6 (Transition — Quote):
+------------------------------------------+
|  [dark background]                       |
|                                          |
|     "Your team deserves better than      |
|      a Friday afternoon spreadsheet."    |
|                                          |
+------------------------------------------+
```

### Database Schemas (ER Diagrams)

Show each table as a box with columns listed. Use arrows or lines to indicate foreign key relationships. Include column types and constraints (PK, FK, nullable).

Key things to make explicit:
- All tables, not just the obvious ones (audit logs, subscriptions, junction tables)
- Foreign key relationships with direction
- Column names and types
- Constraints (PK, FK, unique, not null)

Example:
```
+------------------+         +------------------+
| users            |         | products         |
| id (PK, UUID)    |         | id (PK, UUID)    |
| email            |         | name, price      |
| name             |         | stripe_price_id  |
| plan             |         | active           |
| stripe_id        |         +------------------+
| created_at       |
+------------------+
        |                            |
        v                            v
+------------------+         +------------------+
| purchases        |         | subscriptions    |
| id (PK)          |         | id (PK)          |
| user_id (FK)     |         | user_id (FK)     |
| product_id (FK)  |         | product_id (FK)  |
| amount, currency |         | status           |
| status           |         | started_at       |
+------------------+         | ends_at          |
        |                    +------------------+
        v
+------------------+
| audit_logs       |
| id (PK)          |
| purchase_id (FK) |
| event_type       |
| payload (jsonb)  |
+------------------+
```

### Automation Workflows (n8n, Zapier, etc.)

Use flowchart notation with arrows showing data flow. The critical thing here is making ALL branches visible — including error paths, "not found" cases, and edge cases that would otherwise be silently omitted.

Key things to make explicit:
- Every decision branch (valid/invalid, found/not found, score thresholds)
- Error handling paths
- Symmetric endings (both branches terminate properly)
- Node types and integrations (HTTP Request, Slack, Supabase)

Example:
```
[WEBHOOK] --> [Parse & Validate]
    INVALID --> [Send Error Email] --> END
    VALID   --> [Lookup Contact in CRM]
        NOT FOUND --> [Create New Contact (HubSpot POST)] --> merge
        FOUND     --> merge
    --> [Check Lead Score]
        < 50  --> [Add to Nurture Sequence] --> [Log to DB] --> END
        >= 50 --> [Notify Sales Slack] --> [Create CRM Task] --> [Log to DB] --> END
```

## Why This Works

Without a wireframe, you make assumptions:
- Charts get equal widths when the user wanted 60/40
- Sidebars take 25-30% instead of the intended 15%
- Table columns are whatever seems reasonable, not what the user needs
- Buttons the user didn't mention are absent
- Error branches in workflows are skipped entirely
- All presentation slides get the same title-plus-bullets layout
- Database schemas miss auxiliary tables (subscriptions, audit logs)

With a wireframe, every decision is visible and editable before any implementation begins. The user approves the structure, and you execute it exactly.

## When to Use This Approach

Apply this three-step process to:
- Any web interface or UI component
- Presentations and slide decks
- Database schemas and API designs
- Automation workflows and pipelines
- Landing pages and marketing pages
- Email templates with complex layouts
- Mobile app screens
- Form layouts and multi-step wizards

## Behavior Rules

1. **Never skip the wireframe step.** Even if the user says "just build it," generate the wireframe first and show it. A 30-second wireframe saves 30 minutes of revision.

2. **Never write code during Step 1 or Step 2.** The wireframe phase is purely structural. Code comes only in Step 3.

3. **Redraw the full wireframe on iteration.** When the user requests changes, show the complete updated wireframe — not just the changed section. Context matters.

4. **Treat the approved wireframe as sacred.** In Step 3, do not add elements the user didn't include, remove elements they placed, or change proportions they specified. The wireframe is the specification.

5. **Make proportions explicit.** Never leave width ratios, column counts, or spacing ambiguous. Write "60% / 40%" or "3 columns" directly in the wireframe.

6. **Include sample data.** Tables should show column headers and at least one example row. Cards should show realistic placeholder values. This prevents misunderstandings about data structure.

7. **Label everything.** Every box, section, button, and region in the wireframe gets a label. Unlabeled boxes create ambiguity.

8. **Show all branches in workflows.** Error paths, edge cases, and "not found" scenarios must be visible. If a branch isn't in the wireframe, it won't be in the code.
