import MemeCard from './MemeCard'
import type { Forecast } from '../types'

function formatDate(iso: string): string {
  const d = new Date(iso)
  const months = ['янв','фев','мар','апр','май','июн','июл','авг','сен','окт','ноя','дек']
  return `${d.getDate()} ${months[d.getMonth()]}`
}

export default function ForecastList({ forecast }: { forecast: Forecast }) {
  return (
    <div className="forecast">
      <h2>Прогноз на 5 дней · {forecast.city}</h2>
      <div className="forecast-days">
        {forecast.days.map((day, i) => (
          <div className="forecast-day" key={i}>
            <div className="forecast-date">{formatDate(day.date)}</div>
            <img src={`https://openweathermap.org/img/wn/${day.icon}@2x.png`} alt={day.description} className="forecast-icon" />
            <div className="forecast-temp">{Math.round(day.temp)}°C</div>
            <div className="forecast-desc">{day.description}</div>
            {day.meme && <MemeCard meme={day.meme} />}
          </div>
        ))}
      </div>
    </div>
  )
}