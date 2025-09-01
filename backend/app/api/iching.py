from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random
import json
from pathlib import Path

router = APIRouter(prefix="/api/iching", tags=["iching"])
templates = Jinja2Templates(directory="templates")

def load_iching_data():
    """Загрузка данных Книги Перемен"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "iching_data.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Если файла нет - вернем демо-данные
        return {
            "hexagrams": [
                {
                    "number": 1,
                    "name": "Цянь / Творчество",
                    "symbol": "䷀",
                    "meaning": "Сила творчества, инициатива, активная мужская энергия.",
                    "advice": "Сейчас время действовать смело и уверенно."
                },
                {
                    "number": 2,
                    "name": "Кунь / Исполнение",
                    "symbol": "䷁",
                    "meaning": "Восприимчивость, терпение, пассивная женская энергия.",
                    "advice": "Наберитесь терпения. Иногда бездействие — лучшее действие."
                }
            ],
            "general_advices": [
                "Сегодняшнее беспокойство — завтрашняя мудрость.",
                "Иногда нужно заблудиться, чтобы найти верный путь.",
                "Доверьтесь течению жизни — оно знает куда нести."
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки данных: {str(e)}")

@router.get("/", response_class=HTMLResponse)
async def iching_page(request: Request):
    """Главная страница Книги Перемен"""
    return templates.TemplateResponse("iching.html", {"request": request})

@router.get("/random")
async def get_random_hexagram():
    """Получить случайную гексаграмму (JSON API)"""
    data = load_iching_data()
    hexagram = random.choice(data['hexagrams'])
    return hexagram

@router.get("/random-advice")
async def get_random_advice():
    """Получить случайный совет (JSON API)"""
    data = load_iching_data()
    advice = random.choice(data['general_advices'])
    return {"advice": advice}

@router.get("/all-hexagrams")
async def get_all_hexagrams():
    """Получить все гексаграммы"""
    data = load_iching_data()
    return {"hexagrams": data['hexagrams']}

@router.get("/hexagram/{number}")
async def get_hexagram_by_number(number: int):
    """Получить гексаграмму по номеру"""
    data = load_iching_data()
    for hexagram in data['hexagrams']:
        if hexagram['number'] == number:
            return hexagram
    raise HTTPException(status_code=404, detail=f"Гексаграмма с номером {number} не найдена")

@router.get("/demo")
async def demo_data():
    """Демонстрационные данные для тестирования"""
    return {
        "message": "Это демо-данные Книги Перемен",
        "data": load_iching_data()
    }

# Эндпоинт для проверки здоровья модуля
@router.get("/health")
async def iching_health():
    """Проверка здоровья модуля Книги Перемен"""
    try:
        data = load_iching_data()
        return {
            "status": "healthy",
            "hexagrams_count": len(data['hexagrams']),
            "advices_count": len(data['general_advices'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Модуль не здоров: {str(e)}")