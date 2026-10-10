import type { Weather } from '../types'
export default function WeatherCard({ weather }: { weather: Weather }) {
  return (
    <div className="weather-card">
      <h2>{weather.city}</h2>
      <img src={`https://openweathermap.org/img/wn/${weather.icon}@2x.png`} alt={weather.description} className="weather-icon" />
      <div className="temp">{Math.round(weather.temp)}°C</div>
      <div className="desc">{weather.description}</div>
    </div>
  )
}