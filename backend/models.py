from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)          # ссылка на картинку
    text = Column(String, nullable=False)         # подпись/шутка
    category = Column(String, index=True, nullable=False)  # hot/cold/rain/snow/wind
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)