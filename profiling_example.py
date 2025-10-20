import time
from fastapi import FastAPI
import logging
import random

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")

app = FastAPI(title="Profiling Example - BEFORE Optimization")

# Устанавливаем счетчик для имитации различных "тяжелых" операций
CALL_COUNT = 0


@app.get("/hot-endpoint")
def hot_endpoint():
    """
    Неоптимизированный эндпоинт, который выполняет тяжелую CPU-операцию
    (суммирование квадратов 10 миллионов чисел).
    """
    global CALL_COUNT
    CALL_COUNT += 1

    start = time.time()

    # Очень тяжелая операция, занимающая много времени CPU
    # 10,000,000 чисел
    # NOTE: Это самая медленная часть кода, которую мы будем оптимизировать.
    result = sum([i ** 2 for i in range(10_000_000)])

    duration = time.time() - start

    logging.info(f"Вызов #{CALL_COUNT}: Заняло {duration:.4f} сек.")

    return {
        "result": "Calculation completed",
        "sum": result,
        "duration_seconds": f"{duration:.4f}",
        "status": "UNOPTIMIZED"
    }