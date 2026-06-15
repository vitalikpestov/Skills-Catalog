---
name: create-migration
description: Создание Supabase SQL миграции с RLS, индексами и constraints
---

# Create Migration

Создание новой SQL миграции для Supabase.

## Workflow

### Шаг 1 — Имя файла
```
Supabase/Migrations/YYYYMMDDHHMMSS_описание.sql
```
Пример: `20260325120000_create_dose_records.sql`

### Шаг 2 — Структура миграции
```sql
-- ============================================================
-- Migration: описание
-- Date: YYYY-MM-DD
-- Module: название модуля из SPECIFICATION.md
-- ============================================================

-- 1. Create tables
CREATE TABLE IF NOT EXISTS public.table_name (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    -- поля из спецификации
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz  -- soft delete
);

-- 2. Indexes
CREATE INDEX idx_table_field ON public.table_name(field);

-- 3. RLS
ALTER TABLE public.table_name ENABLE ROW LEVEL SECURITY;

-- SELECT policy
CREATE POLICY "Users can view own family data"
    ON public.table_name FOR SELECT
    USING (
        family_id IN (
            SELECT family_id FROM public.family_members
            WHERE user_id = auth.uid() AND deleted_at IS NULL
        )
    );

-- INSERT policy
CREATE POLICY "Users can insert in own family"
    ON public.table_name FOR INSERT
    WITH CHECK (/* условие */);

-- UPDATE policy
CREATE POLICY "Users can update own family data"
    ON public.table_name FOR UPDATE
    USING (/* условие */);

-- 4. Triggers (updated_at)
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON public.table_name
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Шаг 3 — Проверка
```bash
supabase db push
supabase db lint
```

## Правила
- UUID v4 для всех PK
- timestamptz для всех дат (UTC)
- RLS на КАЖДУЮ таблицу — без исключений
- Soft delete через deleted_at (не DELETE)
- ON DELETE CASCADE для children, SET NULL для optional references
- Unique constraints для бизнес-правил (medication_id + scheduled_at)
