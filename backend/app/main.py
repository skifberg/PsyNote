from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys
from pathlib import Path
import asyncio

# Добавляем текущую директорию в путь для импортов
sys.path.append(str(Path(__file__).parent))

# Создаем экземпляр приложения FastAPI
app = FastAPI(
    title="PsyNote",
    description="Психологическое веб-приложение для самоанализа и работы с собой",
    version="1.0.0"
)

# Правильные пути к статическим файлам и шаблонам
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Флаг для отслеживания доступности сервисов БД
HAS_DB_SERVICE = False
HAS_BIG5_MODULE = False

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

# Пытаемся подключить Big Five модуль
try:
    from api.big5 import router as big5_router
    app.include_router(big5_router, prefix="/api/big5", tags=["Big Five Personality Test"])
    HAS_BIG5_MODULE = True
    print("✅ Модуль Big Five подключен")
except ImportError as e:
    print(f"❌ Ошибка импорта Big Five: {e}")
    print("⚠️  Big Five тест будет недоступен")

# Пытаемся подключить сервис базы данных
try:
    from services.database_service import DatabaseService
    HAS_DB_SERVICE = True
    print("✅ Сервис базы данных подключен")
except ImportError as e:
    print(f"❌ Ошибка импорта сервиса БД: {e}")
    print("⚠️  Функциональность БД будет недоступна")

# Инициализация при запуске
@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске приложения"""
    print("🚀 Запуск PsyNote...")
    
    if HAS_DB_SERVICE:
        print("🔄 Инициализация базы данных...")
        try:
            success = await DatabaseService.initialize_database()
            if success:
                print("✅ База данных инициализирована")
                
                # Пробуем импортировать вопросы, но не падаем при ошибке
                try:
                    print("🔄 Импорт вопросов Big Five...")
                    import_result = await DatabaseService.import_ipip_items()
                    if import_result:
                        print("✅ Вопросы Big Five импортированы")
                    else:
                        print("⚠️  Ошибка импорта вопросов (продолжаем работу)")
                except Exception as e:
                    print(f"⚠️  Ошибка при импорте вопросов: {e}")
            else:
                print("⚠️  Ошибка инициализации базы данных (продолжаем без БД)")
        except Exception as e:
            print(f"⚠️  Критическая ошибка при инициализации БД: {e}")
            print("⚠️  Продолжаем работу без функциональности БД")
    else:
        print("⚠️  Пропущена инициализация БД (модуль не найден)")

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

@app.get("/big5-test")
async def big5_test_page(request: Request):
    """Страница теста Big Five"""
    if not HAS_BIG5_MODULE:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Модуль Big Five временно недоступен"
        }, status_code=503)
    
    return templates.TemplateResponse("big5_test.html", {"request": request})

@app.get("/api/health")
async def health_check():
    """Проверка здоровья всего приложения"""
    modules = ["iching", "self_analysis", "psychometrics"]
    if HAS_BIG5_MODULE:
        modules.append("big5")
    
    return {
        "status": "healthy", 
        "service": "PsyNote",
        "version": "1.0.0",
        "modules": modules,
        "database": "available" if HAS_DB_SERVICE else "not_configured",
        "big5": "available" if HAS_BIG5_MODULE else "not_configured"
    }

# Новые API endpoints для Big Five
@app.get("/api/big5/status")
async def big5_status():
    """Проверка статуса Big Five модуля"""
    return {
        "available": HAS_BIG5_MODULE,
        "database_available": HAS_DB_SERVICE,
        "message": "Big Five тест готов к работе" if HAS_BIG5_MODULE and HAS_DB_SERVICE 
                  else "Big Five тест временно недоступен"
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

@app.exception_handler(503)
async def service_unavailable_handler(request: Request, exc: Exception):
    """Обработчик 503 ошибок (сервис недоступен)"""
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error_message": "Сервис временно недоступен"
    }, status_code=503)

if __name__ == "__main__":
    import uvicorn
    print("🌐 Запуск сервера на http://localhost:8000")
    print("📊 Проверь статус: http://localhost:8000/api/health")
    print("🧪 Big Five тест: http://localhost:8000/big5-test")
    print("📚 Документация API: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)