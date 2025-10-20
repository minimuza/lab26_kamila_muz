import time
from fastapi import FastAPI, HTTPException
import redis
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")

app = FastAPI(title="Profiling Example - AFTER Optimization (Redis)")

# --- 1. Подключение к Redis (Кеширование) ---
try:
    r = redis.Redis(host="localhost", port=6379, db=0)
    r.ping()
    logging.info("✅ Успешное подключение к Redis. Кеширование активно.")
    REDIS_CONNECTED = True
except redis.exceptions.ConnectionError:
    logging.warning("❌ Redis Server не запущен. Оптимизация кешированием отключена.")
    REDIS_CONNECTED = False

# Константы для кеша
CACHE_KEY = "heavy_sum_result"
CACHE_TTL_SECONDS = 300  # Кешируем результат на 5 минут


@app.get("/optimized-endpoint")
def optimized_endpoint():
    """
    Оптимизированный эндпоинт, который использует кеширование Redis,
    чтобы избежать повторного выполнения тяжелой CPU-операции.
    """
    start = time.time()

    # --- 2. Проверяем Кеш ---
    if REDIS_CONNECTED:
        if (cached_data_bytes := r.get(CACHE_KEY)):
            duration = time.time() - start
            result_sum = int(cached_data_bytes.decode("utf-8"))
            logging.info(f"➡️ Вызов: Заняло {duration:.4f} сек. (КЕШ ХИТ)")
            return {
                "result": "Calculation completed (CACHED)",
                "sum": result_sum,
                "duration_seconds": f"{duration:.4f}",
                "status": "OPTIMIZED (Redis)"
            }

    # --- 3. Тяжелая операция (Кеш Мисс) ---
    logging.info("🔄 Генерация новых данных (медленный запрос).")

    # Выполняем ту же тяжелую операцию
    # NOTE: Это выполняется только один раз за 5 минут!
    result_sum = sum([i ** 2 for i in range(10_000_000)])

    # --- 4. Записываем в Кеш ---
    if REDIS_CONNECTED:
        r.setex(CACHE_KEY, CACHE_TTL_SECONDS, result_sum)
        logging.info("✅ Результат сохранен в кеш.")

    duration = time.time() - start

    return {
        "result": "Calculation completed (RECALCULATED)",
        "sum": result_sum,
        "duration_seconds": f"{duration:.4f}",
        "status": "OPTIMIZED (Recalculated)"
    }

