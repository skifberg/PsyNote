from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Dict, List, Optional
from pathlib import Path

# Импортируем AI модуль
try:
    from ai_config.deepseek_client import deepseek_client
    AI_AVAILABLE = True
except ImportError as e:
    AI_AVAILABLE = False
    print(f"⚠️  AI модуль не доступен: {e}")

router = APIRouter(prefix="/psychometrics", tags=["psychometrics"])

class TestAnswer(BaseModel):
    question_id: int
    value: int

class TestSubmission(BaseModel):
    test_id: str
    answers: List[TestAnswer]

class AIAnalysisRequest(BaseModel):
    provider: Optional[str] = "deepseek"

# Путь к папке с тестами (относительно текущего файла)
TESTS_DIR = Path(__file__).parent.parent / "tests"

def load_test(test_id: str) -> Dict:
    """Загрузка теста из JSON файла"""
    test_path = TESTS_DIR / f"{test_id}.json"
    try:
        if not test_path.exists():
            raise HTTPException(status_code=404, detail="Тест не найден")
            
        with open(test_path, "r", encoding="utf-8") as f:
            test_data = json.load(f)
            
        # Добавляем подсчет вопросов для совместимости
        if "questions" in test_data:
            test_data["question_count"] = len(test_data["questions"])
            
        return test_data
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Ошибка формата теста")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки теста: {str(e)}")

def calculate_score(test_data: Dict, answers: List[TestAnswer]) -> int:
    """Подсчет баллов теста"""
    total_score = 0
    answer_dict = {answer.question_id: answer.value for answer in answers}
    
    for question in test_data["questions"]:
        if question["id"] in answer_dict:
            total_score += answer_dict[question["id"]]
    
    return total_score

def interpret_result(test_data: Dict, score: int) -> Dict:
    """Интерпретация результатов"""
    for range_data in test_data["scoring"]["ranges"]:
        if range_data["min"] <= score <= range_data["max"]:
            return {
                "result": range_data["result"],
                "description": range_data.get("description", ""),
                "recommendations": range_data.get("recommendations", [])
            }
    
    return {
        "result": "Результат не определен",
        "description": "Невозможно интерпретировать полученные баллы",
        "recommendations": ["Обратитесь к специалисту для консультации"]
    }

@router.get("/tests")
async def get_available_tests():
    """Получить список доступных тестов"""
    tests = []
    try:
        if TESTS_DIR.exists():
            for file in TESTS_DIR.glob("*.json"):
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        test_data = json.load(f)
                        tests.append({
                            "id": test_data["id"],
                            "name": test_data["name"],
                            "description": test_data["description"],
                            "question_count": len(test_data.get("questions", []))
                        })
                except Exception as e:
                    print(f"Ошибка загрузки теста {file}: {e}")
                    continue
                    
        return tests
        
    except Exception as e:
        print(f"Ошибка получения тестов: {e}")
        return []

@router.get("/tests/{test_id}")
async def get_test(test_id: str):
    """Получить тест по ID"""
    return load_test(test_id)

@router.post("/tests/{test_id}/submit")
async def submit_test(test_id: str, submission: TestSubmission):
    """Отправить ответы на тест"""
    if test_id != submission.test_id:
        raise HTTPException(status_code=400, detail="Несоответствие ID теста")
    
    test_data = load_test(test_id)
    
    # Валидация ответов
    if len(submission.answers) != len(test_data["questions"]):
        raise HTTPException(status_code=400, detail="Не все вопросы отвечены")
    
    # Подсчет баллов
    score = calculate_score(test_data, submission.answers)
    
    # Интерпретация
    interpretation = interpret_result(test_data, score)
    
    # Вычисляем максимальный возможный балл
    max_score = 0
    for question in test_data["questions"]:
        max_option = max(option["value"] for option in question["options"])
        max_score += max_option
    
    return {
        "test_id": test_id,
        "test_name": test_data["name"],
        "score": score,
        "max_score": max_score,
        "interpretation": interpretation
    }

@router.post("/tests/{test_id}/ai-analysis")
async def ai_test_analysis(test_id: str, submission: TestSubmission, request: AIAnalysisRequest):
    """AI-анализ результатов теста через DeepSeek"""
    
    if not AI_AVAILABLE:
        raise HTTPException(status_code=501, detail="AI модуль не настроен")
    
    # Загружаем тест и вычисляем результаты
    test_data = load_test(test_id)
    score = calculate_score(test_data, submission.answers)
    interpretation = interpret_result(test_data, score)
    
    try:
        # AI анализ
        ai_analysis = deepseek_client.analyze_test_results(
            test_name=test_data["name"],
            score=score,
            max_score=sum(max(opt["value"] for opt in q["options"]) for q in test_data["questions"]),
            interpretation=interpretation
        )
        
        return {
            "test_id": test_id,
            "test_name": test_data["name"],
            "score": score,
            "max_score": sum(max(opt["value"] for opt in q["options"]) for q in test_data["questions"]),
            "interpretation": interpretation,
            "ai_analysis": ai_analysis,
            "ai_model": "deepseek-chat"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка AI анализа: {str(e)}")