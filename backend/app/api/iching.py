# backend/app/api/iching.py
from fastapi import APIRouter, HTTPException
import random
import json
from pathlib import Path

router = APIRouter(prefix="/api/iching", tags=["iching"])

def load_iching_data():
    """Загрузка данных Книги Перемен"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "iching_data.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка загрузки данных")

@router.get("/random")
async def get_random_hexagram():
    """Получить случайную гексаграмму"""
    data = load_iching_data()
    return random.choice(data['hexagrams'])