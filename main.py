from fastapi import FastAPI
from pydantic import BaseModel, Field


# 1. Модель данных для пользователя
class User(BaseModel):
    name: str
    # Ограничиваем возраст, чтобы тест на ошибку сработал (возраст > 0)
    age: int = Field(..., gt=0, description="Возраст должен быть больше 0")


# Инициализация приложения
app = FastAPI()


# ----------------------------------------------------
# Эндпоинты API
# ----------------------------------------------------

# Эндпоинт 1: GET / (проверяется в test_read_root)
@app.get("/")
def read_root():
    """Простой корневой эндпоинт."""
    return {"message": "Hello World"}  # "Hello" должно быть в сообщении


# Эндпоинт 2: POST /users (проверяется в test_create_user)
@app.post("/users")
def create_user(user: User):
    """Принимает данные пользователя и возвращает их."""
    # В реальном приложении здесь было бы сохранение в БД
    return {"status": "User created successfully", "name": user.name, "age": user.age}
