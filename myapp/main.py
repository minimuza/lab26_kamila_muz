from fastapi import FastAPI
from .routers import users # Импортируем модуль роутера
from .database import Base, engine

# Создаем таблицы в БД (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Refactoring Example")

# 7. Подключение роутеров
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the modular FastAPI application!"}

