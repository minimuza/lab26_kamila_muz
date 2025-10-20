import redis
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")

app = FastAPI(
    title="Redis Caching Example",
    description="Пример кеширования ответа API на 10 секунд с использованием Redis."
)

# 3. Подключение к Redis
# Используем localhost:6379 (стандартный порт Redis)
try:
    r = redis.Redis(host="localhost", port=6379, db=0)
    # Проверка соединения: выполним ping
    r.ping()
    logging.info("✅ Успешное подключение к Redis.")
except redis.exceptions.ConnectionError as e:
    # Если Redis не запущен, приложение выдаст ошибку
    logging.error(f"❌ Ошибка подключения к Redis. Убедитесь, что redis-server запущен: {e}")
    # Можно поднять HTTPException или просто работать без кеша, но для ЛР лучше выйти
    raise HTTPException(status_code=503, detail="Redis service is unavailable")


# 4. Реализация эндпоинта с кешированием
@app.get("/data")
def get_data():
    """
    Возвращает данные либо из кеша Redis (если TTL не истек),
    либо генерирует новые данные и сохраняет их в кеш на 10 секунд.
    """

    CACHE_KEY = "my_data"
    CACHE_TTL_SECONDS = 10  # Time To Live (время жизни) кеша

    # 1. Проверяем кеш (r.get возвращает байты или None)
    if (cached_data_bytes := r.get(CACHE_KEY)):
        # Данные найдены в кеше. Декодируем их из байтов в строку
        data = cached_data_bytes.decode("utf-8")
        logging.info("➡️ Данные получены из кеша.")
        return JSONResponse(content={"data": data, "cached": True})

    # 2. Если данных нет в кеше — генерируем "тяжелый" результат
    logging.info("🔄 Генерация новых данных (медленный запрос).")
    # Имитируем задержку в 1 секунду, как будто это долгий запрос к БД
    time.sleep(1)
    result = f"Сгенерировано в: {time.time()}"

    # 3. Сохраняем результат в кеш с TTL (Time To Live)
    # setex устанавливает ключ и время жизни в секундах
    r.setex(CACHE_KEY, CACHE_TTL_SECONDS, result)

    return JSONResponse(content={"data": result, "cached": False})
