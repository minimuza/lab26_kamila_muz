from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# ----------------------------------------------------
# 1. Модель данных для пользователя (для POST /users)
# ----------------------------------------------------
class User(BaseModel):
    name: str
    # Ограничиваем возраст, чтобы тест на ошибку (age: -5) сработал
    age: int = Field(..., gt=0, description="Возраст должен быть больше 0")


# ----------------------------------------------------
# 2. Инициализация приложения и "базы данных"
# ----------------------------------------------------
app = FastAPI()

# Имитация базы данных (пустой список)
fake_db = []
user_counter = 0


# ----------------------------------------------------
# 3. Эндпоинты, которые проверяются в тестах
# ----------------------------------------------------

# Тест 1: GET / (test_read_root)
@app.get("/")
def read_root():
    """Корневой эндпоинт, который проверяется на статус 200 и сообщение."""
    return {"message": "Hello World! Welcome to the API."}


# Тест 2 и 3: POST /users (test_create_user_success, test_create_user_invalid_age)
@app.post("/users")
def create_user(user: User):
    """
    Создает нового пользователя.

    FastAPI автоматически проверяет валидность данных Pydantic (age > 0).
    Если age <= 0, FastAPI вернет статус 422 (как и ожидается в тесте).
    """
    global user_counter
    user_counter += 1

    new_user = user.model_dump()
    new_user["id"] = user_counter

    # Сохраняем в нашу "базу данных"
    fake_db.append(new_user)

    return {"status": "User created", "name": new_user["name"], "id": new_user["id"]}


# ----------------------------------------------------
# Дополнительный эндпоинт для более сложных тестов (не обязателен для ЛР25)
# ----------------------------------------------------
@app.get("/users/{user_id}")
def read_user(user_id: int):
    """Возвращает данные пользователя по ID (для демонстрации 404)."""
    for user in fake_db:
        if user["id"] == user_id:
            return user

    # Эндпоинт, который возвращает ошибку 404, если пользователь не найден
    raise HTTPException(status_code=404, detail="User not found")

