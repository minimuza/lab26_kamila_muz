import pytest
# Для асинхронных фикстур нам нужен AsyncClient
from httpx import AsyncClient
from main import app, fake_db
# Использование специализированной фикстуры для асинхронного режима
# Это решает проблему "async_generator"
from pytest_asyncio import fixture as async_fixture


# NOTE: Для работы асинхронных тестов и фикстур необходим плагин pytest-asyncio (pip install pytest-asyncio)

# ----------------------------------------------------
# Задание 1: Создание фикстуры для тестового клиента API
# ----------------------------------------------------
@async_fixture(scope="session")  # Асинхронная фикстура, создается один раз
async def client():
    """
    Создает асинхронный тестовый клиент для всех тестов.
    Scope="session" означает, что клиент создается один раз за сессию.
    """
    # pytest-asyncio гарантирует, что yield будет обработан правильно
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# ----------------------------------------------------
# Задание 2: Создание фикстуры для тестовой базы данных (подготовка/очистка)
# ----------------------------------------------------
@pytest.fixture(scope="function")  # Обычная синхронная фикстура, очистка перед каждым тестом
def fake_db_fixture():
    """
    Очищает тестовую базу данных перед каждым тестом.
    Scope="function" означает, что фикстура вызывается перед каждым тестом.
    """
    # Подготовка (Setup) перед тестом
    fake_db.clear()

    yield fake_db  # Передача управления тесту


# ----------------------------------------------------
# Задание 4: Тест для проверки работы эндпоинта GET /health
# ----------------------------------------------------
@async_fixture(scope="function")  # Теперь это async_fixture, а не просто async def test
async def test_read_health(client: AsyncClient):
    """
    Проверяет, что эндпоинт /health возвращает статус 200 и корректный JSON.
    """
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ----------------------------------------------------
# Задание 5: Тест для эндпоинта POST /items
# ----------------------------------------------------
@async_fixture(scope="function")  # Теперь это async_fixture
async def test_create_item_success(client: AsyncClient, fake_db_fixture):
    """
    Проверяет успешное создание элемента (201) и его сохранение.
    """
    test_data = {
        "name": "Test Item (Fixture)",
        "price": 20.0,
        "is_offer": True
    }

    response = await client.post("/items", json=test_data)

    assert response.status_code == 201

    response_json = response.json()
    assert response_json["item"]["name"] == "Test Item (Fixture)"

    # Проверяем, что элемент действительно добавлен
    assert len(fake_db) == 1
    assert fake_db[0]["name"] == "Test Item (Fixture)"


# ----------------------------------------------------
# Дополнительный тест: Проверка поведения при неверных данных (400)
# ----------------------------------------------------
@async_fixture(scope="function")  # Теперь это async_fixture
async def test_create_item_invalid_data(client: AsyncClient):
    """
    Проверяет, что при отправке неверных данных возвращается статус 400 Bad Request.
    """
    error_data = {
        "name": "Error Item",
        "price": -5.00,
        "is_offer": False
    }

    response = await client.post("/items/error_test", json=error_data)

    assert response.status_code == 400
    assert "Price cannot be negative" in response.json().get("detail", "")