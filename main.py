from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import date
from database import init_db, mark_day_as_success, get_streak, get_month_data
from pathlib import Path

app = FastAPI()
init_db()

# Подключаем папку static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    today = date.today()
    streak = get_streak()
    month_data = get_month_data(today.year, today.month)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "streak": streak,
            "month_data": month_data,
            "today": str(today),
            "year": today.year,
            "month": today.month,
        }
    )

@app.post("/mark")
def mark_day():
    mark_day_as_success()
    return RedirectResponse(url="/", status_code=303)

# Подключаем шаблоны
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")