#!/bin/bash
# Скрипт автоматического запуска PsyNote сервера

echo "🎯 Запуск PsyNote сервера..."
echo "📂 Текущая директория: $(pwd)"

# Проверяем, что мы в правильной директории
if [[ ! $(pwd) == *"PsyNote"* ]]; then
    echo "❌ Не в директории PsyNote. Переходим..."
    cd /Users/oleg/PsyNote
fi

echo "🔍 Проверяем виртуальное окружение..."

# Активируем venv
if [ -d "venv" ]; then
    echo "✅ Виртуальное окружение найдено"
    source venv/bin/activate
    echo "🐍 Python: $(python --version)"
    echo "📦 PIP: $(pip --version)"
else
    echo "❌ Виртуальное окружение не найдено!"
    echo "Создайте его: python -m venv venv"
    exit 1
fi

echo "📁 Переходим в backend/app..."
cd backend/app

echo "🔍 Проверяем, запущен ли сервер..."
# Проверяем, не запущен ли уже сервер
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️ Сервер уже запущен на порту 8000"
    echo "Останавливаем предыдущий процесс..."
    pkill -f "uvicorn main:app"
    sleep 2
fi

echo "🚀 Запускаем сервер..."
echo "📡 Сервер будет доступен по: http://localhost:8000"
echo "📚 Документация API: http://localhost:8000/docs"
echo ""
echo "Для остановки сервера нажмите Ctrl+C"
echo "----------------------------------------"

# Запускаем сервер
uvicorn main:app --reload --port 8000 --host 0.0.0.0