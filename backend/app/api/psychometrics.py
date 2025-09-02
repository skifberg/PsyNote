from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
from typing import List, Optional

router = APIRouter()

# Путь к файлу с тестами
TESTS_FILE = Path("data/psychometric_tests.json")

class TestConfig:
    @staticmethod
    def load_tests():
        """Загрузить конфигурацию тестов"""
        try:
            with open(TESTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(500, f"Ошибка загрузки тестов: {str(e)}")
    
    @staticmethod
    def save_tests(data):
        """Сохранить конфигурацию тестов"""
        try:
            with open(TESTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise HTTPException(500, f"Ошибка сохранения тестов: {str(e)}")

@router.get("/tests")
async def get_available_tests(all: bool = False):
    """Получить список доступных тестов"""
    try:
        data = TestConfig.load_tests()
        
        if all:
            return data['tests']
        else:
            # Возвращаем только активные тесты
            active_tests = [test for test in data['tests'] if test['active']]
            return {"tests": active_tests}
    
    except Exception as e:
        raise HTTPException(500, f"Ошибка загрузки тестов: {str(e)}")

@router.post("/admin/tests/{test_id}/toggle")
async def toggle_test(test_id: str, active: bool):
    """Активировать/деактивировать тест"""
    try:
        data = TestConfig.load_tests()
        
        # Находим и обновляем тест
        for test in data['tests']:
            if test['id'] == test_id:
                test['active'] = active
                break
        else:
            raise HTTPException(404, f"Тест {test_id} не найден")
        
        TestConfig.save_tests(data)
        return {"status": "success", "active": active, "test_id": test_id}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Ошибка обновления теста: {str(e)}")

@router.put("/admin/tests/{test_id}")
async def update_test(test_id: str, updated_test: dict):
    """Обновить параметры теста"""
    try:
        data = TestConfig.load_tests()
        
        for i, test in enumerate(data['tests']):
            if test['id'] == test_id:
                data['tests'][i] = {**test, **updated_test}
                break
        else:
            raise HTTPException(404, f"Тест {test_id} не найден")
        
        TestConfig.save_tests(data)
        return {"status": "success", "test": data['tests'][i]}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Ошибка обновления теста: {str(e)}")

@router.get("/categories")
async def get_test_categories():
    """Получить список категорий тестов"""
    try:
        data = TestConfig.load_tests()
        categories = list(set(test['category'] for test in data['tests']))
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(500, f"Ошибка загрузки категорий: {str(e)}")