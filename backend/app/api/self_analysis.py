from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
from typing import Dict, Any
import random

router = APIRouter(prefix="/api/self-analysis", tags=["self_analysis"])

def load_self_analysis_data():
    """Загрузка данных модуля самоанализа"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "self_analysis.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки данных: {str(e)}")

@router.get("/modules")
async def get_all_modules():
    """Получить все модули самоанализа"""
    return load_self_analysis_data()

@router.get("/module/{module_id}")
async def get_module(module_id: str):
    """Получить конкретный модуль по ID"""
    data = load_self_analysis_data()
    for module in data['modules']:
        if module['id'] == module_id:
            return module
    raise HTTPException(status_code=404, detail="Модуль не найден")

@router.get("/technique/{module_id}/{technique_id}")
async def get_technique(module_id: str, technique_id: str):
    """Получить конкретную технику"""
    data = load_self_analysis_data()
    for module in data['modules']:
        if module['id'] == module_id:
            for technique in module['techniques']:
                if technique['id'] == technique_id:
                    return technique
    raise HTTPException(status_code=404, detail="Техника не найдена")

# ДОБАВЛЯЕМ НОВЫЕ ЭНДПОИНТЫ ДЛЯ РАБОТЫ С ВОПРОСАМИ
@router.get("/random-question/{module_id}/{technique_id}")
async def get_random_question(module_id: str, technique_id: str):
    """Получить случайный вопрос из техники"""
    try:
        technique = await get_technique(module_id, technique_id)
        
        if 'questions' not in technique or not technique['questions']:
            raise HTTPException(status_code=404, detail="Вопросы не найдены в технике")
        
        random_question = random.choice(technique['questions'])
        return {
            "question": random_question,
            "technique_name": technique['name'],
            "module_name": next((m['name'] for m in load_self_analysis_data()['modules'] if m['id'] == module_id), "")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")

@router.get("/all-techniques")
async def get_all_techniques():
    """Получить все техники всех модулей"""
    data = load_self_analysis_data()
    techniques = []
    
    for module in data['modules']:
        for technique in module['techniques']:
            techniques.append({
                "id": technique['id'],
                "name": technique['name'],
                "description": technique.get('description', ''),
                "module_id": module['id'],
                "module_name": module['name'],
                "has_questions": 'questions' in technique and bool(technique['questions'])
            })
    
    return {"techniques": techniques}

@router.post("/save-answer")
async def save_answer(answer_data: Dict[str, Any]):
    """Сохранить ответ пользователя"""
    try:
        # Здесь будет логика сохранения в базу данных
        # Пока просто возвращаем полученные данные
        return {
            "status": "success",
            "message": "Ответ сохранен",
            "data": answer_data,
            "saved_at": "2024-01-15T10:00:00Z"  # В реальности используйте datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения: {str(e)}")

@router.get("/health")
async def health_check():
    """Проверка работы модуля"""
    data = load_self_analysis_data()
    return {
        "status": "healthy",
        "modules_count": len(data['modules']),
        "techniques_count": sum(len(module['techniques']) for module in data['modules'])
    }