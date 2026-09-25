from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


class MemeBase(BaseModel):
    url: str
    text: str
    category: str


class MemeCreate(MemeBase):
    pass


class MemeOut(MemeBase):
    id: int
    likes: int
    created_at: datetime

    class Config:
        from_attributes = True


class WeatherResponse(BaseModel):
    city: str
    temp: float
    description: str
    icon: str
    category: str
    meme: Optional[MemeOut] = None


class ForecastDay(BaseModel):
    date: str
    temp: float
    description: str
    icon: str
    category: str
    meme: Optional[MemeOut] = None


class ForecastResponse(BaseModel):
    city: str
    days: List[ForecastDay]