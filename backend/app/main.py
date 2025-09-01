from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys
from pathlib import Path

# Создаем экземпляр приложения FastAPI
app = FastAPI(
    title="PsyNote",
    description="Психологическое веб-приложение для самоанализа и работы с собой",
    version="1.0.0"
)

# ПРАВИЛЬНЫЕ пути - без префикса "app/"
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Импортируем и подключаем роутеры
try:
    from api.iching import router as iching_router
    app.include_router(iching_router, prefix="/api/iching", tags=["I Ching"])
    print("✅ Модуль I Ching подключен")
except ImportError as e:
    print(f"❌ Ошибка импорта I Ching: {e}")

try:
    from api.self_analysis import router as self_analysis_router
    app.include_router(self_analysis_router, prefix="/api/self-analysis", tags=["Self Analysis"])
    print("✅ Модуль Self Analysis подключен")
except ImportError as e:
    print(f"❌ Ошибка импорта Self Analysis: {e}")

# Basic routes
@app.get("/")
async def read_root(request: Request):
    """Главная страница с Decision Gate"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/iching")
async def iching_page(request: Request):
    """Страница Книги Перемен"""
    return templates.TemplateResponse("iching.html", {"request": request})

@app.get("/self-analysis")
async def self_analysis_page(request: Request):
    """Страница модуля самоанализа"""
    return templates.TemplateResponse("self_analysis.html", {"request": request})

@app.get("/api/health")
async def health_check():
    """Проверка здоровья всего приложения"""
    return {
        "status": "healthy", 
        "service": "PsyNote",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)