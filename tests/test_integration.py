# Импортируем синхронного клиента FastAPI
from fastapi.testclient import TestClient
# Импортируем наше приложение
from main import app

# Создаем клиента для тестирования всего приложения
client = TestClient(app)


# ----------------------------------------------------
# Основные тесты (Задание 3)
# ----------------------------------------------------

def test_read_root():
    """Проверка GET-запроса к корневому эндпоинту."""
    response = client.get("/")
    # Проверяем статус-код 200 (ОК)
    assert response.status_code == 200
    # Проверяем, что ответ содержит нужное сообщение
    assert "Hello" in response.json()["message"]


def test_create_user_success():
    """Проверка POST-запроса для создания пользователя с валидными данными."""
    user_data = {"name": "Ivan", "age": 25}
    response = client.post("/users", json=user_data)

    # Проверяем статус-код 200 (ОК)
    assert response.status_code == 200
    # Проверяем, что ответ содержит отправленное имя
    assert response.json()["name"] == "Ivan"


# ----------------------------------------------------
# Дополнительные тесты для проверки ошибок (Задание 6)
# ----------------------------------------------------

def test_create_user_invalid_data_error():
    """Проверка ошибки при отправке невалидных данных (age <= 0)."""
    # Отправляем данные, которые нарушают условие age > 0 в main.py
    invalid_data = {"name": "Bad User", "age": 0}
    response = client.post("/users", json=invalid_data)

    # Ожидаем ошибку валидации Pydantic: 422 Unprocessable Entity
    assert response.status_code == 422


def test_nonexistent_endpoint_error():
    """Проверка ошибки 404 для несуществующего эндпоинта."""
    # Отправляем запрос на URL, которого нет в main.py
    response = client.get("/nonexistent-path-abc")

    # Ожидаем статус "Not Found"
    assert response.status_code == 404
