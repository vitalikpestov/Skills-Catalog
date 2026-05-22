# Notchy

A macOS menu bar app that puts Claude Code right in your MacBook's notch. Hover over the notch or click the menu bar icon to open a floating terminal panel with embedded sessions that automatically detect your open Xcode projects.

<!-- Add your screenshot here: ![Notchy](screenshot.png) -->

## Features

- **Notch integration** — hover over the MacBook notch to reveal the terminal panel
- **Xcode project detection** — automatically discovers open Xcode projects and `cd`s into them
- **Multi-session tabs** — run multiple Claude Code sessions side by side
- **Live status in the notch** — animated pill shows whether Claude is working, waiting, or done
- **Git checkpoints** — Cmd+S to snapshot your project before Claude makes changes

## Requirements

- macOS 26.0+
- MacBook with a notch (for notch features; menu bar still works without one)

## Building

Open `Notchy.xcodeproj` in Xcode and build (Cmd+B), or from the command line:

```bash
xcodebuild -project Notchy.xcodeproj -scheme Notchy -configuration Debug build
```

## Dependencies

- [SwiftTerm](https://github.com/migueldeicaza/SwiftTerm) — terminal emulator view (via Swift Package Manager)

## License

[MIT](LICENSE)
