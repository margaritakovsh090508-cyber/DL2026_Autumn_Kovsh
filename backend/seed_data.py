from sqlalchemy.orm import Session
from models import Meme

# Стартовый набор мемов (картинки — локальные SVG в frontend/public/memes/)
SEED_MEMES = [
    # hot
    {"url": "/memes/mem1.svg",  "text": "Когда +35, а ты забыл воду дома", "category": "hot"},
    {"url": "/memes/mem2.svg",  "text": "Пекло. Я просто существую и плавлюсь", "category": "hot"},
    {"url": "/memes/mem3.svg",  "text": "Кондиционер — мой лучший друг", "category": "hot"},
    # cold
    {"url": "/memes/mem4.svg",  "text": "−20. Три свитера не помогают", "category": "cold"},
    {"url": "/memes/mem5.svg",  "text": "Зима близко. И не Игра престолов", "category": "cold"},
    # rain
    {"url": "/memes/mem6.svg",  "text": "Дождь. Я как утка — мне норм", "category": "rain"},
    {"url": "/memes/mem7.svg",  "text": "Забыл зонт. Классика", "category": "rain"},
    {"url": "/memes/mem8.svg",  "text": "Лужи — это бесплатный бассейн", "category": "rain"},
    # snow
    {"url": "/memes/mem9.svg",  "text": "Снег. Дороги — каток", "category": "snow"},
    {"url": "/memes/mem10.svg", "text": "Снеговик из меня так себе", "category": "snow"},
    # wind
    {"url": "/memes/mem11.svg", "text": "Ветер сдувает. Держись!", "category": "wind"},
    {"url": "/memes/mem12.svg", "text": "Причёска? Не, не слышала", "category": "wind"},
]


def seed(db: Session):
    """Заполняет БД мемами, если она пуста."""
    if db.query(Meme).count() == 0:
        for m in SEED_MEMES:
            db.add(Meme(**m))
        db.commit()
        print(f"OK: Добавлено {len(SEED_MEMES)} мемов")
