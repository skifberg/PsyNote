from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Импортируем модули API
from api import iching
from api import self_analysis  # Раскомментирован!

app = FastAPI(
    title="PsyNote API",
    version="1.0.0",
    description="Психологический помощник с модулем Книги Перемен"
)

# Настройка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Подключаем роутеры API
app.include_router(iching.router)
app.include_router(self_analysis.router)  # Раскомментирован!

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Главная страница с Decision Gate"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health_check():
    """Проверка статуса API"""
    return {
        "status": "ok", 
        "project": "PsyNote",
        "version": "1.0.0",
        "available_modules": ["iching", "self_analysis"],
        "modules_in_development": ["testing", "decision_gate"]
    }

@app.get("/about")
async def about():
    """Информация о проекте"""
    return {
        "name": "PsyNote",
        "description": "Психологический помощник с AI-интеграцией",
        "author": "Oleg",
        "tech_stack": ["Python", "FastAPI", "HTML/CSS/JS"]
    }

# Дополнительные эндпоинты можно добавлять здесь

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)