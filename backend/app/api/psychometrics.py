from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
from typing import List, Optional
import logging

router = APIRouter()

# Настройка логирования
logger = logging.getLogger(__name__)

# Путь к файлу с тестами
TESTS_FILE = Path("data/psychometric_tests.json")

def get_default_tests():
    """Возвращает тесты по умолчанию если файл не найден"""
    return {
        "tests": [
            {
                "id": "big5",
                "name": "Тест личности Big Five",
                "description": "Научная оценка 5 основных черт личности",
                "category": "personality",
                "estimated_time": 20,
                "questions_count": 100,
                "active": True,
                "version": "1.0",
                "image": "🧠"
            },
            {
                "id": "phq9",
                "name": "PHQ-9: Оценка депрессии",
                "description": "Шкала оценки депрессивных симптомов",
                "category": "mood",
                "estimated_time": 5,
                "questions_count": 9,
                "active": True,
                "version": "1.0",
                "image": "😔"
            },
            {
                "id": "gad7",
                "name": "GAD-7: Шкала тревожности",
                "description": "Шкала оценки генерализованной тревоги",
                "category": "anxiety",
                "estimated_time": 3,
                "questions_count": 7,
                "active": True,
                "version": "1.0",
                "image": "😰"
            }
        ]
    }

class TestConfig:
    @staticmethod
    def load_tests():
        """Загрузить конфигурацию тестов"""
        try:
            if not TESTS_FILE.exists():
                # Создаем файл с тестами по умолчанию
                default_tests = get_default_tests()
                with open(TESTS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(default_tests, f, ensure_ascii=False, indent=2)
                return default_tests
            
            with open(TESTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            logger.error(f"Ошибка загрузки тестов: {str(e)}")
            return get_default_tests()
    
    @staticmethod
    def save_tests(data):
        """Сохранить конфигурацию тестов"""
        try:
            with open(TESTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения тестов: {str(e)}")
            return False

@router.get("/tests")
async def get_available_tests(all: bool = False):
    """Получить список доступных тестов"""
    try:
        data = TestConfig.load_tests()
        
        # Для отладки
        logger.info(f"Загружены тесты: {data}")
        
        if all:
            return data['tests']
        else:
            # Возвращаем только активные тесты
            active_tests = [test for test in data['tests'] if test.get('active', True)]
            return active_tests
    
    except Exception as e:
        logger.error(f"Ошибка в get_available_tests: {str(e)}")
        return get_default_tests()['tests']

@router.get("/categories")
async def get_test_categories():
    """Получить список категорий тестов"""
    try:
        data = TestConfig.load_tests()
        categories = list(set(test['category'] for test in data['tests']))
        return {"categories": categories}
    except Exception as e:
        logger.error(f"Ошибка в get_test_categories: {str(e)}")
        return {"categories": ["personality", "mood", "anxiety"]}

# Простые эндпоинты для отладки
@router.get("/health")
async def health_check():
    """Проверка здоровья модуля"""
    return {"status": "healthy", "module": "psychometrics"}

@router.get("/debug")
async def debug_info():
    """Отладочная информация"""
    data = TestConfig.load_tests()
    return {
        "file_exists": TESTS_FILE.exists(),
        "tests_count": len(data['tests']),
        "tests": data['tests']
    }