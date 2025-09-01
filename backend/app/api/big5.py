from fastapi import APIRouter, HTTPException
from models.entities import UserResponse
from services.database_service import DatabaseService
import random

router = APIRouter()

@router.get("/next_question/{user_id}")
async def get_next_question(user_id: int):
    """
    Получить следующий вопрос для пользователя
    """
    try:
        question = await DatabaseService.get_next_question(user_id)
        
        if not question:
            return {"status": "completed", "message": "Все вопросы пройдены"}
        
        return {
            "item_id": question["item_id"],
            "text": question["text"],
            "domain": question["domain"],
            "options": [
                {"score": 1, "text": "Совершенно не обо мне"},
                {"score": 2, "text": "В основном не обо мне"},
                {"score": 3, "text": "Отчасти верно, отчасти нет"},
                {"score": 4, "text": "В основном верно"},
                {"score": 5, "text": "Полностью верно"}
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения вопроса: {str(e)}")

@router.post("/response")
async def save_response(response: UserResponse):
    """Сохранить ответ пользователя"""
    success = await DatabaseService.save_user_response(response)
    if not success:
        raise HTTPException(status_code=500, detail="Ошибка сохранения ответа")
    return {"status": "success", "message": "Ответ сохранен"}

@router.get("/results/{user_id}")
async def get_results(user_id: int):
    """Получить результаты теста для пользователя"""
    try:
        results = await DatabaseService.get_user_results(user_id)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения результатов: {str(e)}")

@router.get("/stats")
async def get_stats():
    """Получить статистику базы данных"""
    try:
        from models.database import db
        
        # Получаем базовую статистику
        items_count = await db.fetchone("SELECT COUNT(*) as count FROM items")
        responses_count = await db.fetchone("SELECT COUNT(*) as count FROM user_responses")
        users_count = await db.fetchone("SELECT COUNT(*) as count FROM users")
        
        return {
            "items_count": items_count["count"] if items_count else 0,
            "responses_count": responses_count["count"] if responses_count else 0,
            "users_count": users_count["count"] if users_count else 0,
            "database_type": "SQLite"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")