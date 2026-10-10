import type { Weather, Forecast, Meme } from './types'
const BASE = '/api'

export async function fetchWeather(city: string): Promise<Weather> {
  const res = await fetch(`${BASE}/weather?city=${encodeURIComponent(city)}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Ошибка запроса')
  }
  return res.json()
}
export async function fetchForecast(city: string): Promise<Forecast> {
  const res = await fetch(`${BASE}/forecast?city=${encodeURIComponent(city)}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Ошибка запроса прогноза')
  }
  return res.json()
}
export async function fetchMemes(category?: string): Promise<Meme[]> {
  const url = category ? `${BASE}/memes?category=${category}` : `${BASE}/memes`
  const res = await fetch(url)
  return res.json()
}
export async function addMeme(meme: Omit<Meme, 'id' | 'likes' | 'created_at'>): Promise<Meme> {
  const res = await fetch(`${BASE}/memes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(meme)
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Не удалось добавить мем')
  }
  return res.json()
}
export async function likeMeme(id: number): Promise<Meme> {
  const res = await fetch(`${BASE}/memes/${id}/like`, { method: 'POST' })
  return res.json()
}