# Claude Code Source Snapshot (For Security Research)

This repository mirrors a publicly exposed snapshot of Claude Code’s source that became accessible on **March 31, 2026**, due to a source map exposure in the npm package.

It is preserved strictly for:
* **Educational purposes**
* **Defensive security research**
* **Software supply-chain analysis**

> [!CAUTION]
> This repository does not claim ownership of the original code and is not an official Anthropic repository.

---

## Research Background
This repository is maintained by a university student researching:
* Software supply-chain leaks and build artifact exposure
* Secure software engineering practices
* Architecture of agent-based developer tools
* Defensive analysis of real-world CLI systems

The archive supports:
* Academic study
* Hands-on security research
* Architectural review
* Discussion of packaging and release-process failures

---

## How the Source Became Public
On March 31, 2026, **Chaofan Shou (@Fried_rice)** reported that Claude Code source files were accessible through a `.map` file included in the npm distribution.

> “Claude code source code has been leaked via a map file in their npm registry!”
> — **@Fried_rice**, March 31, 2026

The source map pointed to unobfuscated TypeScript source files hosted in Anthropic’s R2 storage bucket, making the entire `src/` directory publicly downloadable.

---

## What This Repository Contains
Claude Code is Anthropic’s command-line interface for interacting with Claude to perform software engineering tasks such as:
* Editing files
* Running shell commands
* Searching codebases
* Managing workflows
* Coordinating multiple agents

### Snapshot details:
* **Public exposure date:** 2026-03-31
* **Language:** TypeScript
* **Runtime:** Bun
* **Terminal UI:** React + Ink
* **Size:** ~1,900 files, 512,000+ lines of code

---

## Directory Structure Overview
```text
src/
├── main.tsx                 # CLI entrypoint and orchestration
├── commands.ts              # Slash command registry
├── tools.ts                 # Tool registry
├── Tool.ts                  # Tool type definitions
├── QueryEngine.ts           # Core LLM query engine
├── context.ts               # Context collection logic
├── cost-tracker.ts          # Token cost tracking
│
├── commands/                # Slash command implementations (~50)
├── tools/                   # Tool implementations (~40)
├── components/              # Ink UI components (~140)
├── hooks/                   # React hooks
├── services/                # External service integrations
├── screens/                 # Full-screen UIs (Doctor, REPL, Resume)
├── types/                   # Type definitions
├── utils/                   # Utilities
│
├── bridge/                  # IDE and remote control bridge
├── coordinator/             # Multi-agent coordination
├── plugins/                 # Plugin system
├── skills/                  # Skill workflows
├── keybindings/             # Keybinding configs
├── vim/                     # Vim mode
├── voice/                   # Voice input support
├── remote/                  # Remote sessions
├── server/                  # Server mode
├── memdir/                  # Persistent memory
├── tasks/                   # Task management
├── state/                   # State management
├── migrations/              # Config migrations
├── schemas/                 # Zod schemas
├── entrypoints/             # Initialization logic
├── ink/                     # Ink renderer wrapper
├── buddy/                   # Companion sprite
├── native-ts/               # Native TS utilities
├── outputStyles/            # Output styling
├── query/                   # Query pipeline
└── upstreamproxy/           # Proxy configuration
```
## Architecture Overview

### 1. Tool System (`src/tools/`)
Each tool Claude Code can use is implemented as a self-contained module. Every tool defines its input schema, permission requirements, and execution logic.

| Tool | Purpose |
| :--- | :--- |
| **BashTool** | Run shell commands |
| **FileReadTool** | Read files (text, images, PDFs, notebooks) |
| **FileWriteTool** | Create or overwrite files |
| **FileEditTool** | Partial file edits |
| **GlobTool** | File pattern search |
| **GrepTool** | Content search (ripgrep) |
| **WebFetchTool** | Fetch URL content |
| **WebSearchTool** | Web search |
| **AgentTool** | Spawn sub-agents |
| **SkillTool** | Execute skills |
| **MCPTool** | MCP server calls |
| **LSPTool** | Language Server Protocol |
| **NotebookEditTool** | Jupyter notebook edits |
| **TaskCreate / Update** | Task management |
| **SendMessageTool** | Inter-agent messaging |
| **TeamCreate / Delete** | Team management |
| **PlanMode tools** | Planning mode toggle |
| **Worktree tools** | Git worktree isolation |
| **CronCreateTool** | Scheduled triggers |
| **RemoteTriggerTool** | Remote triggers |
| **SleepTool** | Wait / proactive mode |
| **SyntheticOutputTool** | Structured output |

### 2. Command System (`src/commands/`)
Slash commands (prefixed with `/`) provide user-facing functionality.
* `/commit` – create git commits
* `/review` – code review
* `/compact` – context compression
* `/config` – settings
* `/doctor` – diagnostics
* `/login / /logout` – authentication
* `/memory` – persistent memory
* `/skills` – skill management
* `/tasks` – task tracking
* `/vim` – Vim mode
* `/diff` – view changes
* `/cost` – usage cost
* `/resume` – restore session
* `/share` – share session
* `/desktop / /mobile` – app handoff

### 3. Service Layer (`src/services/`)
Handles integrations and system-level features:
* Anthropic API client
* MCP server connections
* OAuth 2.0 authentication
* LSP management
* Analytics and feature flags
* Plugin loading
* Context compression
* Policy enforcement
* Token estimation
* Team memory syncing

### 4. Bridge System (`src/bridge/`)
Provides two-way communication between the CLI and IDEs (VS Code, JetBrains).
* Message protocol
* Permission callbacks
* REPL bridge
* JWT authentication
* Session execution control

### 5. Permission System
Every tool invocation is checked through the permission system. Permissions may be prompted to the user, auto-approved, denied, or bypassed. 
**Modes:** Default, Plan Mode, Auto, and BypassPermissions.

### 6. Feature Flags
Uses Bun’s `bun:bundle` feature flags to completely remove inactive code at build time.
**Notable flags:** `PROACTIVE`, `KAIROS`, `BRIDGE_MODE`, `DAEMON`, `VOICE_MODE`, `AGENT_TRIGGERS`, `MONITOR_TOOL`.

---

## Important Files
* **`QueryEngine.ts` (~46K lines):** Core LLM engine handling streaming responses, tool-call loops, retries, token tracking, and thinking mode.
* **`Tool.ts` (~29K lines):** Defines base tool interfaces, schemas, permissions, and progress states.
* **`commands.ts` (~25K lines):** Registers and executes all slash commands with environment-specific loading.
* **`main.tsx`:** CLI startup logic including command parsing (Commander.js), Ink UI initialization, and parallel prefetching.

---

## Technology Stack

| Area | Technology |
| :--- | :--- |
| **Runtime** | Bun |
| **Language** | TypeScript (strict) |
| **UI** | React + Ink |
| **CLI** | Commander.js |
| **Validation** | Zod v4 |
| **Search** | ripgrep |
| **Protocols** | MCP, LSP |
| **API** | Anthropic SDK |
| **Telemetry** | OpenTelemetry + gRPC |
| **Feature Flags** | GrowthBook |
| **Auth** | OAuth 2.0, JWT, macOS Keychain |

---

## Design Highlights
* **Parallel Prefetching:** Startup performance is improved by loading MDM settings, keychain data, and API connections in parallel before heavy imports.
* **Lazy Loading:** Large dependencies (telemetry, analytics, gRPC) are dynamically imported only when needed.
* **Agent Swarms:** Multiple agents can run in parallel using `AgentTool` and the coordinator system.
* **Skill System:** Reusable workflows live in `skills/` and can be extended by users.
* **Plugin Architecture:** Supports both built-in and third-party plugins.

---

## Disclaimer
This repository is an educational and defensive security research archive maintained by a university student. Its purpose is to study source exposure incidents, packaging and release failures, and modern agent-based CLI architectures.

All original Claude Code source remains the property of Anthropic. This repository is not affiliated with, endorsed by, or maintained by Anthropic.
