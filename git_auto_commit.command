#!/bin/zsh

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cd ~/PsyNote || {
    echo -e "${RED}Ошибка: Директория PsyNote не найдена!${NC}"
    exit 1
}

# Функция для уведомлений
notify() {
    osascript -e "display notification \"$2\" with title \"$1\""
}

# Проверяем Git
if ! git status &>/dev/null; then
    echo -e "${RED}Ошибка: Это не Git репозиторий${NC}"
    notify "Git Error" "Not a git repository"
    exit 1
fi

# Проверяем изменения
CHANGES=$(git status --porcelain)
if [ -z "$CHANGES" ]; then
    echo -e "${YELLOW}Нет изменений для коммита${NC}"
    notify "Git" "No changes to commit"
    exit 0
fi

echo -e "${YELLOW}Обнаружены изменения:${NC}"
git status -s

# Добавляем изменения
git add .
echo -e "${GREEN}Изменения добавлены${NC}"

# Коммит
COMMIT_MSG="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Коммит создан: $COMMIT_MSG${NC}"
    notify "Git Commit" "Commit created successfully"
else
    echo -e "${RED}Ошибка при коммите${NC}"
    notify "Git Error" "Commit failed"
    exit 1
fi

# Push
echo -e "${YELLOW}Отправляем на GitHub...${NC}"
git push origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Успешно отправлено на GitHub!${NC}"
    notify "Git Push" "Pushed to GitHub successfully"
else
    echo -e "${RED}Ошибка при отправке на GitHub${NC}"
    notify "Git Error" "Push to GitHub failed"
    exit 1
fi
