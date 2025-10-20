from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Строка подключения к вашей базе данных
# Убедитесь, что user:pass и dbname верны
DATABASE_URL = "postgresql+psycopg2://postgres:admin123@localhost:5432/testdb"

# 2. Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL)

# 3. Создание фабрики сессий, которая будет создавать новые сессии базы данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# (Опционально: здесь же можно определить Base, если вы не определили его в main.py)
# from sqlalchemy.orm import declarative_base
# Base = declarative_base()