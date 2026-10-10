import { useState, FormEvent } from 'react'
import { addMeme } from '../api'

const CATEGORIES = [
  { value: 'hot', label: '🔥 Жарко' },
  { value: 'cold', label: '❄️ Холодно' },
  { value: 'rain', label: '🌧️ Дождь' },
  { value: 'snow', label: '🌨️ Снег' },
  { value: 'wind', label: '💨 Ветрено' },
]

export default function AddMemeForm({ onAdded }: { onAdded?: () => void }) {
  const [url, setUrl] = useState('')
  const [text, setText] = useState('')
  const [category, setCategory] = useState('hot')
  const [msg, setMsg] = useState('')
  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    try {
      await addMeme({ url, text, category })
      setMsg('✅ Мем добавлен!'); setUrl(''); setText('')
      onAdded?.()
    } catch (err) {
      setMsg('❌ ' + (err instanceof Error ? err.message : 'Ошибка'))
    }
  }
  return (
    <form className="add-form" onSubmit={handleSubmit}>
      <h3>Добавить мем</h3>
      <input placeholder="Ссылка на картинку" value={url} onChange={(e) => setUrl(e.target.value)} required />
      <input placeholder="Текст шутки" value={text} onChange={(e) => setText(e.target.value)} required />
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        {CATEGORIES.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
      </select>
      <button type="submit">Добавить</button>
      {msg && <p className="msg">{msg}</p>}
    </form>
  )
}