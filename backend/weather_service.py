import httpx
import os

# Ключ можно получить бесплатно на openweathermap.org
# Если ключа нет — используем демо-режим с фейковыми данными
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def determine_category(temp: float, description: str, wind_speed: float) -> str:
    """Определяет категорию мема по погодным условиям."""
    desc = description.lower()
    if "снег" in desc or "snow" in desc:
        return "snow"
    if "дождь" in desc or "rain" in desc or "гроза" in desc or "storm" in desc:
        return "rain"
    if temp >= 25:
        return "hot"
    if temp <= 0:
        return "cold"
    if wind_speed >= 10:
        return "wind"
    return "wind"  # fallback


async def fetch_weather(city: str) -> dict:
    """Запрашивает погоду у OpenWeatherMap. При отсутствии ключа — демо-данные."""
    if not API_KEY:
        # Демо-режим, чтобы приложение работало без регистрации
        return {
            "city": city,
            "temp": 28.5,
            "description": "ясно",
            "icon": "01d",
            "wind_speed": 3.0,
        }

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(BASE_URL, params=params)
        if resp.status_code == 404:
            raise ValueError("Город не найден")
        resp.raise_for_status()
        data = resp.json()

    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data["wind"]["speed"],
    }
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


async def fetch_forecast(city: str) -> list[dict]:
    """Возвращает список из ~5 дней с усреднённой погодой по каждому дню."""
    if not API_KEY:
        # Демо-режим: 5 выдуманных дней с разной погодой
        return [
            {"date": "2026-09-26", "temp": 27.0, "description": "ясно",       "icon": "01d", "wind_speed": 3.0},
            {"date": "2026-09-27", "temp": 18.0, "description": "облачно",     "icon": "03d", "wind_speed": 5.0},
            {"date": "2026-09-28", "temp": 12.0, "description": "дождь",       "icon": "10d", "wind_speed": 7.0},
            {"date": "2026-09-29", "temp": -3.0, "description": "снег",        "icon": "13d", "wind_speed": 4.0},
            {"date": "2026-09-30", "temp": 5.0,  "description": "ветрено",     "icon": "50d", "wind_speed": 12.0},
        ]

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(FORECAST_URL, params=params)
        if resp.status_code == 404:
            raise ValueError("Город не найден")
        resp.raise_for_status()
        data = resp.json()

    # Группируем по дате (YYYY-MM-DD)
    from collections import defaultdict
    days: dict[str, list] = defaultdict(list)
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        days[date].append(item)

    result = []
    for date, items in list(days.items())[:5]:
        temps = [it["main"]["temp"] for it in items]
        winds = [it["wind"]["speed"] for it in items]
        # Берём описание из середины дня (12:00), иначе — первое
        mid = next((it for it in items if "12:00:00" in it["dt_txt"]), items[0])
        result.append({
            "date": date,
            "temp": round(sum(temps) / len(temps), 1),
            "description": mid["weather"][0]["description"],
            "icon": mid["weather"][0]["icon"],
            "wind_speed": round(max(winds), 1),
        })
    return result