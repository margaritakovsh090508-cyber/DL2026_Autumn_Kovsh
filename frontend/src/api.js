// Обёртки над fetch для обращения к бэкенду
const BASE = '/api'

export async function fetchWeather(city) {
  const res = await fetch(`${BASE}/weather?city=${encodeURIComponent(city)}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Ошибка запроса')
  }
  return res.json()
}

export async function fetchMemes(category) {
  const url = category ? `${BASE}/memes?category=${category}` : `${BASE}/memes`
  const res = await fetch(url)
  return res.json()
}

export async function addMeme(meme) {
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

export async function likeMeme(id) {
  const res = await fetch(`${BASE}/memes/${id}/like`, { method: 'POST' })
  return res.json()
}
export async function fetchForecast(city) {
  const res = await fetch(`${BASE}/forecast?city=${encodeURIComponent(city)}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Ошибка запроса прогноза')
  }
  return res.json()
}
