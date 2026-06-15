---
name: add-screen
description: Добавление нового SwiftUI экрана по шаблону с ViewModel
---

# Add Screen

Создание нового SwiftUI экрана с ViewModel, навигацией и accessibility.

## Workflow

### Шаг 1 — Создай ViewModel
Файл: `ViewModels/{ScreenName}VM.swift`

```swift
import Foundation
import SwiftData
import os

@Observable
final class {ScreenName}VM {
    enum State {
        case loading
        case empty
        case error(String)
        case loaded
    }

    private let service: {Service}
    private let logger = Logger(subsystem: "com.dosesync", category: "{ScreenName}")

    var state: State = .loading
    // ... properties

    init(service: {Service} = .init()) {
        self.service = service
    }

    func load() async {
        state = .loading
        do {
            // fetch data
            state = /* .loaded or .empty */
        } catch {
            logger.error("Failed to load: \(error)")
            state = .error(error.localizedDescription)
        }
    }

    func retry() async {
        await load()
    }
}
```

### Шаг 2 — Создай View
Файл: `Views/{Module}/{ScreenName}View.swift`

```swift
import SwiftUI

struct {ScreenName}View: View {
    @State private var viewModel = {ScreenName}VM()

    var body: some View {
        Group {
            switch viewModel.state {
            case .loading:
                ProgressView()
            case .empty:
                EmptyStateView(
                    icon: "icon.name",
                    message: String(localized: "screen_empty_message")
                )
            case .error(let message):
                ErrorView(message: message) {
                    await viewModel.retry()
                }
            case .loaded:
                contentView
            }
        }
        .task { await viewModel.load() }
        .navigationTitle(String(localized: "screen_title"))
    }

    private var contentView: some View {
        // Main content
    }
}

#Preview {
    NavigationStack {
        {ScreenName}View()
    }
}
```

### Шаг 3 — Добавь в навигацию
Добавь экран в соответствующий NavigationStack/TabView по графу из SPECIFICATION.md.

### Шаг 4 — Localization
Добавь строки в `Localizable.xcstrings`:
- `screen_title` — заголовок
- `screen_empty_message` — текст пустого состояния
- Все user-facing строки

## Checklist
- [ ] ViewModel с 4 состояниями
- [ ] View с .task для async loading
- [ ] Preview работает
- [ ] accessibilityLabel на интерактивных элементах
- [ ] Dynamic Type поддержан
- [ ] Строки в String Catalog
- [ ] Добавлен в навигационный граф
