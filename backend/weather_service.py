import httpx
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


class WeatherNotConfiguredError(Exception):
    """API-ключ OpenWeatherMap не задан."""
    pass


def determine_category(temp: float, description: str, wind_speed: float) -> str:
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
    return "wind"


def _ensure_configured() -> None:
    if not API_KEY:
        raise WeatherNotConfiguredError(
            "Сервис погоды не настроен: не задан OPENWEATHER_API_KEY. "
            "Получите бесплатный ключ на https://openweathermap.org/api "
            "и добавьте его в файл backend/.env"
        )


async def fetch_weather(city: str) -> dict:
    _ensure_configured()
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "ru"}
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


async def fetch_forecast(city: str) -> list[dict]:
    _ensure_configured()
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "ru"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(FORECAST_URL, params=params)
        if resp.status_code == 404:
            raise ValueError("Город не найден")
        resp.raise_for_status()
        data = resp.json()

    from collections import defaultdict
    days: dict[str, list] = defaultdict(list)
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        days[date].append(item)

    result = []
    for date, items in list(days.items())[:5]:
        temps = [it["main"]["temp"] for it in items]
        winds = [it["wind"]["speed"] for it in items]
        mid = next((it for it in items if "12:00:00" in it["dt_txt"]), items[0])
        result.append({
            "date": date,
            "temp": round(sum(temps) / len(temps), 1),
            "description": mid["weather"][0]["description"],
            "icon": mid["weather"][0]["icon"],
            "wind_speed": round(max(winds), 1),
        })
    return result
