# 🌦️ Погода с настроением (мемы под прогноз)

Приложение показывает текущую погоду в любом городе и подбирает
забавный мем под погодные условия. Можно добавить свой мем и
поделиться открыткой с друзьями.

## Стек

- **Backend:** Python 3.10+, FastAPI, SQLAlchemy, SQLite, httpx
- **Frontend:** React 18, Vite
- **Внешний API:** OpenWeatherMap (опционально)

## Требования

- Python 3.10+
- Node.js 18+
- (опционально) API-ключ OpenWeatherMap

## Запуск бэкенда

```bash
cd backend
python -m venv venv

# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

pip install -r requirements.txt

# (опционально) ключ для реальной погоды:
# Linux/macOS:
export OPENWEATHER_API_KEY=ваш_ключ
# Windows (PowerShell):
# $env:OPENWEATHER_API_KEY="ваш_ключ"

uvicorn main:app --reload --port 8000