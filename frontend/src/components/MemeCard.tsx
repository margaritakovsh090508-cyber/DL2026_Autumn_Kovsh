import { useState } from 'react'
import { likeMeme } from '../api'
import type { Meme } from '../types'

export default function MemeCard({ meme }: { meme: Meme }) {
  const [likes, setLikes] = useState(meme.likes)
  async function handleLike() {
    try { setLikes((await likeMeme(meme.id)).likes) } catch (e) { console.error(e) }
  }
  function share() {
    const text = `Погода: ${meme.text}`
    if (navigator.share) navigator.share({ title: 'Погода с настроением', text, url: meme.url })
    else { navigator.clipboard.writeText(`${text} ${meme.url}`); alert('Скопировано в буфер обмена!') }
  }
  return (
    <div className="meme-card">
      <img src={meme.url} alt={meme.text} className="meme-img"
           onError={(e) => { (e.target as HTMLImageElement).src = 'https://via.placeholder.com/400x300?text=Meme' }} />
      <p className="meme-text">{meme.text}</p>
      <div className="meme-actions">
        <button onClick={handleLike}>❤️ {likes}</button>
        <button onClick={share}>📤 Поделиться</button>
      </div>
    </div>
  )
}