export interface Meme {
  id: number
  url: string
  text: string
  category: string
  likes: number
  created_at: string
}
export interface Weather {
  city: string
  temp: number
  description: string
  icon: string
  category: string
  meme: Meme | null
}
export interface ForecastDay {
  date: string
  temp: number
  description: string
  icon: string
  category: string
  meme: Meme | null
}
export interface Forecast {
  city: string
  days: ForecastDay[]
}