from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Пробуем такой импорт
try:
    from api import iching
except ImportError:
    # Если не работает, пробуем относительный импорт
    from .api import iching

app = FastAPI(title="PsyNote API", version="1.0.0")

# Настройка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Подключаем роутер
app.include_router(iching.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "project": "PsyNote"}