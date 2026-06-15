---
name: implement-feature
description: Реализация нового модуля/фичи по спецификации — от модели данных до UI
---

# Implement Feature

Пошаговая реализация модуля из SPECIFICATION.md.

## Workflow

### Шаг 1 — Прочитай спецификацию
```
Read SPECIFICATION.md → найди раздел модуля → прочитай все 7 блоков
```

### Шаг 2 — Database (делегируй database-architect)
1. Создай SQL миграцию: `Supabase/Migrations/YYYYMMDDHHMMSS_module_name.sql`
2. Таблицы + RLS-политики + индексы + FK constraints
3. Edge Functions если нужны
4. Проверь: `supabase db push`

### Шаг 3 — SwiftData Models (ios-engineer)
1. Создай `@Model` класс в `Models/`
2. `@Attribute(.unique)` для id
3. `@Relationship` для связей
4. `needsSync: Bool` для offline

### Шаг 4 — Service Layer (ios-engineer)
1. Создай Service в `Services/`
2. CRUD операции через Supabase SDK
3. Offline-first: SwiftData → Supabase sync
4. Error handling

### Шаг 5 — ViewModel (ios-engineer)
1. `@Observable final class` в `ViewModels/`
2. State management (loading/empty/error/loaded)
3. Методы для user actions
4. Dependency injection

### Шаг 6 — Views (делегируй swiftui-developer)
1. Создай View файлы в `Views/ModuleName/`
2. 4 состояния экрана
3. NavigationStack/Sheet по графу
4. Accessibility: labels, Dynamic Type
5. Localization: String Catalog

### Шаг 7 — Tests
1. Unit tests для Service и ViewModel
2. Critical paths: happy path + edge cases из спецификации

### Шаг 8 — Review (делегируй qa-reviewer)
1. Code review по чеклисту
2. SwiftLint
3. Compilation check

## Чеклист завершения
- [ ] SQL миграция создана и применена
- [ ] SwiftData модель зеркалит Supabase схему
- [ ] Service с offline-first и error handling
- [ ] ViewModel с 4 состояниями
- [ ] Views с accessibility и localization
- [ ] Unit tests для critical paths
- [ ] QA review пройден
