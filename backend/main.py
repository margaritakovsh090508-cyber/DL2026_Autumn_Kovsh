from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database import Base, engine, get_db
from models import Meme
from schemas import MemeCreate, MemeOut, WeatherResponse, ForecastResponse, ForecastDay
from weather_service import (
    fetch_weather, fetch_forecast, determine_category,
    WeatherNotConfiguredError,
)
import seed_data

# Создаём таблицы и заполняем БД при старте
Base.metadata.create_all(bind=engine)

from fastapi.responses import JSONResponse

class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(
    title="Weather Memes API",
    version="1.0.0",
    default_response_class=UTF8JSONResponse,
)
# CORS — чтобы фронтенд с другого порта мог обращаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    db = next(get_db())
    seed_data.seed(db)


@app.get("/api/weather", response_model=WeatherResponse)
async def get_weather(city: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Возвращает погоду и случайный мем под неё."""
    try:
        weather = await fetch_weather(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Сервис погоды недоступен")

    category = determine_category(
        weather["temp"], weather["description"], weather["wind_speed"]
    )

    # Случайный мем из нужной категории
    meme = (
        db.query(Meme)
        .filter(Meme.category == category)
        .order_by(func.random())
        .first()
    )

    return WeatherResponse(
        city=weather["city"],
        temp=weather["temp"],
        description=weather["description"],
        icon=weather["icon"],
        category=category,
        meme=meme,
    )

@app.get("/api/forecast", response_model=ForecastResponse)
async def get_forecast(city: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    """Возвращает прогноз на 5 дней, для каждого дня — свой мем."""
    try:
        days = await fetch_forecast(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502, detail="Сервис погоды недоступен")

    result_days = []
    for day in days:
        category = determine_category(day["temp"], day["description"], day["wind_speed"])
        meme = (
            db.query(Meme)
            .filter(Meme.category == category)
            .order_by(func.random())
            .first()
        )
        result_days.append(ForecastDay(
            date=day["date"],
            temp=day["temp"],
            description=day["description"],
            icon=day["icon"],
            category=category,
            meme=meme,
        ))

    # Возвращаем название города так, как его вернул weather_service
    # (в демо-режиме — как ввёл пользователь; в реальном API — официальное)
    return ForecastResponse(city=city, days=result_days)

@app.get("/api/memes", response_model=List[MemeOut])
def list_memes(category: str | None = None, db: Session = Depends(get_db)):
    """Список мемов, опционально фильтр по категории."""
    q = db.query(Meme)
    if category:
        q = q.filter(Meme.category == category)
    return q.order_by(Meme.likes.desc()).all()


@app.get("/api/memes/random", response_model=MemeOut)
def random_meme(category: str, db: Session = Depends(get_db)):
    meme = (
        db.query(Meme)
        .filter(Meme.category == category)
        .order_by(func.random())
        .first()
    )
    if not meme:
        raise HTTPException(status_code=404, detail="Мемов в этой категории нет")
    return meme


@app.post("/api/memes", response_model=MemeOut, status_code=201)
def create_meme(payload: MemeCreate, db: Session = Depends(get_db)):
    """Добавление нового мема."""
    if payload.category not in {"hot", "cold", "rain", "snow", "wind"}:
        raise HTTPException(status_code=400, detail="Неверная категория")
    meme = Meme(**payload.model_dump())
    db.add(meme)
    db.commit()
    db.refresh(meme)
    return meme


@app.post("/api/memes/{meme_id}/like", response_model=MemeOut)
def like_meme(meme_id: int, db: Session = Depends(get_db)):
    meme = db.query(Meme).filter(Meme.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Мем не найден")
    meme.likes += 1
    db.commit()
    db.refresh(meme)
    return meme


@app.get("/api/categories")
def get_categories():
    return ["hot", "cold", "rain", "snow", "wind"]