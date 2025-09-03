from fastapi import APIRouter, HTTPException
from typing import Dict
import asyncio

from core.ai_psychologist import ai_psychologist

router = APIRouter(prefix="/ai-psychology", tags=["AI Psychology"])

@router.post("/analyze-test")
async def analyze_test_results(test_data: Dict):
    """AI-анализ результатов психологического теста"""
    try:
        analysis = await ai_psychologist.analyze_test_results(test_data)
        return {
            "success": True,
            "analysis": analysis,
            "test_name": test_data.get("name"),
            "score": test_data.get("score")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis error: {str(e)}")

@router.post("/suggest-methods")
async def suggest_psychological_methods(user_problem: str):
    """Подбор психологических методик based на проблеме пользователя"""
    try:
        methods = await ai_psychologist.suggest_methods(user_problem)
        return {
            "success": True,
            "user_problem": user_problem,
            "suggested_methods": methods
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Methods suggestion error: {str(e)}")

@router.post("/daily-reflection")
async def analyze_daily_reflection(entry_text: str):
    """AI-анализ дневниковой записи"""
    try:
        reflection = await ai_psychologist.daily_reflection(entry_text)
        return {
            "success": True,
            "user_entry": entry_text,
            "ai_reflection": reflection
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reflection analysis error: {str(e)}")

@router.get("/health")
async def ai_health_check():
    """Проверка работоспособности AI-психолога"""
    try:
        test_response = await ai_psychologist.daily_reflection("Тестовое сообщение для проверки")
        return {
            "status": "healthy",
            "ai_ready": True,
            "message": "AI психолог работает корректно"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")