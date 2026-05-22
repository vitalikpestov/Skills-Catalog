#!/bin/bash
# Установщик плагина c-level-advisor для Cowork / Claude Code
# Запусти: bash ~/Documents/MASTER\ skills/install-c-level-advisor.sh

set -e

PLUGIN_FILE="$HOME/Library/Application Support/Claude/local-agent-mode-sessions"
SKILLS_DIR="$HOME/.claude/skills"

# Найдём последнюю загруженную версию плагина
UPLOADED=$(find "$HOME/Library/Application Support/Claude" -name "c-level-advisor.plugin" 2>/dev/null | head -1)

if [ -z "$UPLOADED" ]; then
    echo "❌ Файл c-level-advisor.plugin не найден."
    echo "   Убедись что файл загружен в Cowork."
    exit 1
fi

echo "✅ Найден плагин: $UPLOADED"

# Создаём директорию скиллов если нет
mkdir -p "$SKILLS_DIR"

# Распаковываем плагин
TMPDIR=$(mktemp -d)
unzip -o "$UPLOADED" -d "$TMPDIR" > /dev/null

# Копируем все скиллы
SKILLS_COPIED=0
for skill_dir in "$TMPDIR/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    dest="$SKILLS_DIR/$skill_name"
    cp -r "$skill_dir" "$dest"
    echo "   ✓ $skill_name"
    SKILLS_COPIED=$((SKILLS_COPIED + 1))
done

rm -rf "$TMPDIR"

echo ""
echo "🎉 Установлено $SKILLS_COPIED скиллов из c-level-advisor"
echo "   Перезапусти Cowork чтобы скиллы появились."
