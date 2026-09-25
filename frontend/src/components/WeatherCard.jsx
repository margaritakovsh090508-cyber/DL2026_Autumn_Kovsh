export default function WeatherCard({ weather }) {
  const iconUrl = `https://openweathermap.org/img/wn/${weather.icon}@2x.png`
  return (
    <div className="weather-card">
      <h2>{weather.city}</h2>
      <img src={iconUrl} alt={weather.description} className="weather-icon" />
      <div className="temp">{Math.round(weather.temp)}°C</div>
      <div className="desc">{weather.description}</div>
    </div>
  )
}