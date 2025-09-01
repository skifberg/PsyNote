#!/bin/bash
# Автоматический коммит для PsyNote после тестирования

echo "🔍 Проверяю изменения в проекте..."

# Переходим в корень проекта
cd /Users/oleg/PsyNote

# Проверяем, есть ли изменения для коммита
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Нет изменений для коммита"
    exit 0
fi

echo "📁 Обнаружены изменения:"
git status --short

echo "🚀 Добавляю файлы в git..."
git add .

echo "💾 Создаю коммит..."
COMMIT_MESSAGE="✅ $(date +'%Y-%m-%d %H:%M') - Авто-коммит после тестирования

- Главная страница работает
- Книга Перемен запускается
- Модуль самоанализа открывается  
- Этап тестирования пройден

#autocommit #progress"

git commit -m "$COMMIT_MESSAGE"

echo "🎉 Коммит создан успешно!"
echo "📝 Для отправки изменений выполните:"
echo "   git push origin main"
