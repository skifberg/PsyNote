from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
import random

router = APIRouter()

# Загрузка данных I Ching
def load_iching_data():
    try:
        data_path = Path(__file__).parent.parent / "data" / "iching_data.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки данных: {str(e)}")

@router.get("/hexagrams")
async def get_all_hexagrams():
    """Получить все гексаграммы"""
    return load_iching_data()

@router.get("/hexagram/{number}")
async def get_hexagram(number: int):
    """Получить конкретную гексаграмму по номеру"""
    data = load_iching_data()
    for hexagram in data['hexagrams']:
        if hexagram['number'] == number:
            return hexagram
    raise HTTPException(status_code=404, detail="Гексаграмма не найдена")

@router.get("/random")
async def get_random_hexagram():
    """Получить случайную гексаграмму"""
    data = load_iching_data()
    random_hexagram = random.choice(data['hexagrams'])
    return random_hexagram

@router.get("/divination")
async def perform_divination():
    """Выполнить гадание"""
    data = load_iching_data()
    result = random.choice(data['hexagrams'])
    return {
        "result": result,
        "message": "Гадание выполнено успешно"
    }