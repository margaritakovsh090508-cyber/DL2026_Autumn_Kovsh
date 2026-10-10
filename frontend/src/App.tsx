import { useState, FormEvent } from 'react'
import { fetchWeather, fetchForecast } from './api'
import WeatherCard from './components/WeatherCard'
import MemeCard from './components/MemeCard'
import ForecastList from './components/ForecastList'
import AddMemeForm from './components/AddMemeForm'
import type { Weather, Forecast } from './types'

type Mode = 'now' | 'forecast'

export default function App() {
  const [city, setCity] = useState('')
  const [mode, setMode] = useState<Mode>('now')
  const [weather, setWeather] = useState<Weather | null>(null)
  const [forecast, setForecast] = useState<Forecast | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)

  async function handleSearch(e: FormEvent) {
    e.preventDefault()
    if (!city.trim()) return
    setLoading(true); setError(''); setWeather(null); setForecast(null)
    try {
      if (mode === 'now') setWeather(await fetchWeather(city.trim()))
      else setForecast(await fetchForecast(city.trim()))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Неизвестная ошибка')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header><h1>🌦️ Погода с настроением</h1><p>Погода + мем = хорошее настроение</p></header>
      <div className="mode-switch">
        <button className={mode === 'now' ? 'active' : ''} onClick={() => setMode('now')}>Сейчас</button>
        <button className={mode === 'forecast' ? 'active' : ''} onClick={() => setMode('forecast')}>5 дней</button>
      </div>
      <form className="search" onSubmit={handleSearch}>
        <input placeholder="Введите город (например, Moscow)" value={city} onChange={(e) => setCity(e.target.value)} />
        <button type="submit" disabled={loading}>{loading ? '...' : 'Узнать'}</button>
      </form>
      {error && <div className="error">⚠️ {error}</div>}
      {mode === 'now' && weather && (
        <div className="result">
          <WeatherCard weather={weather} />
          {weather.meme ? <MemeCard meme={weather.meme} /> : <p>Мемов пока нет 😢</p>}
        </div>
      )}
      {mode === 'forecast' && forecast && <ForecastList forecast={forecast} />}
      <div className="footer-actions">
        <button onClick={() => setShowForm(!showForm)}>{showForm ? 'Скрыть форму' : '➕ Добавить мем'}</button>
      </div>
      {showForm && <AddMemeForm onAdded={() => {}} />}
    </div>
  )
}