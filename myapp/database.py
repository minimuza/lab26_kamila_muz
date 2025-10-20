from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Используем in-memory SQLite для примера.
# В реальном проекте здесь будет PostgreSQL или MySQL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# connect_args нужен только для SQLite, чтобы разрешить многопоточность
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Вспомогательная функция для получения сессии БД (зависимость для роутеров)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()