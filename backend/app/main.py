from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

# Получаем абсолютный путь к директории приложения
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="PsyNote",
    description="Психологическое веб-приложение для самоанализа и работы с собой",
    version="1.0.0"
)

# Правильные пути к статическим файлам и шаблонам
static_dir = BASE_DIR / "static"
templates_dir = BASE_DIR / "templates"

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

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

# Подключаем модуль психометрических тестов
try:
    from api.psychometrics import router as psychometrics_router
    app.include_router(psychometrics_router, prefix="/api", tags=["Psychometrics"])  # Изменили префикс!
    print("✅ Модуль Psychometrics подключен")
except ImportError as e:
    print(f"❌ Ошибка импорта Psychometrics: {e}")

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

@app.get("/psychometrics")
async def psychometrics_page(request: Request):
    """Страница психометрических тестов"""
    return templates.TemplateResponse("psychometrics.html", {"request": request})

@app.get("/api/health")
async def health_check():
    """Проверка здоровья всего приложения"""
    return {
        "status": "healthy", 
        "service": "PsyNote",
        "version": "1.0.0",
        "modules": ["iching", "self_analysis", "psychometrics"]
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    """Обработчик 404 ошибок"""
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Обработчик 500 ошибок"""
    return templates.TemplateResponse("500.html", {"request": request}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)