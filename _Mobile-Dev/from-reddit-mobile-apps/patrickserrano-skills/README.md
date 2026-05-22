# iOS & Swift Skills for Claude Code

A collection of Claude Code skills for iOS, Swift, SwiftUI development, and release workflows.

## Installation

```bash
claude plugin install patrickserrano/skills
```

Or add as a marketplace and install:
```bash
claude plugin marketplace add https://github.com/patrickserrano/skills
claude plugin install ios-swift-skills
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `ios-debugger-agent` | Build, run, and debug iOS apps on simulator |
| `swift-concurrency-expert` | Swift 6.2+ concurrency review and remediation |
| `swiftui-liquid-glass` | iOS 26+ Liquid Glass API implementation |
| `swiftui-ui-patterns` | SwiftUI view patterns and best practices |
| `swiftui-view-refactor` | Refactor views for consistent structure |
| `swiftui-performance-audit` | Diagnose and fix SwiftUI performance issues |
| `release-app-store-changelog` | Generate App Store release notes from git |
| `release-macos-spm-packaging` | Package SwiftPM macOS apps without Xcode |
| `github-issue-fix-flow` | End-to-end GitHub issue fix workflow |
| `native-app-profiling` | CLI-based Time Profiler with xctrace |

## Usage

Once installed, skills are automatically available. Invoke them with `/skill-name`:

```
/swiftui-ui-patterns
/release-app-store-changelog
/ios-debugger-agent
```

Claude will also automatically suggest relevant skills based on your requests.

## Structure

```
.claude-plugin/
└── plugin.json          # Plugin manifest
skills/
├── ios-debugger-agent/
│   └── SKILL.md
├── swift-concurrency-expert/
│   └── SKILL.md
├── swiftui-liquid-glass/
│   └── SKILL.md
├── swiftui-ui-patterns/
│   └── SKILL.md
├── swiftui-view-refactor/
│   └── SKILL.md
├── swiftui-performance-audit/
│   └── SKILL.md
├── release-app-store-changelog/
│   └── SKILL.md
├── release-macos-spm-packaging/
│   └── SKILL.md
├── github-issue-fix-flow/
│   └── SKILL.md
└── native-app-profiling/
    └── SKILL.md
```

## Adding Skills

1. Create a new directory under `skills/` with your skill name
2. Add a `SKILL.md` file with frontmatter:

```markdown
---
name: my-skill-name
description: Brief description of when to use this skill
---

# Skill content here
```

## Credits

Skills adapted from:
- [Dimillian/Skills](https://github.com/Dimillian/Skills) by [@Dimillian](https://github.com/Dimillian) (Thomas Ricouard)
- [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [@steipete](https://github.com/steipete) (Peter Steinberger)

## License

MIT
