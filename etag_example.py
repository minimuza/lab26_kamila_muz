import hashlib
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")

app = FastAPI(title="ETag Optimization Example")

# 1. Данные, которые будут обслуживаться (и хешироваться)
# В реальном приложении это был бы результат запроса к базе данных
data = {"id": 1, "title": "Test resource", "version": 1}


@app.get("/resource")
async def get_resource(request: Request):
    """
    Эндпоинт, который возвращает ресурс и его ETag,
    используя заголовок If-None-Match для условного запроса.
    """
    global data

    # 2. Генерация ETag
    # Превращаем данные в строку JSON и кодируем в байты для хеширования
    body_str = json.dumps(data, sort_keys=True).encode("utf-8")
    # Вычисляем MD5 хеш от тела (это наш ETag)
    etag = hashlib.md5(body_str).hexdigest()

    logging.info(f"Сгенерирован ETag: {etag}")

    # 3. Проверка заголовка If-None-Match
    client_etag = request.headers.get("if-none-match")

    if client_etag == etag:
        # ETag клиента совпадает с текущим ETag ресурса.
        # Ресурс не изменился. Отправляем ответ 304.
        logging.info(f"➡️ ETag совпал ({etag}). Ответ 304 Not Modified.")
        return JSONResponse(status_code=304, content=None)

    # 4. Если ETag не совпал (или это первый запрос)

    logging.info("🔄 ETag не совпал / Первый запрос. Возвращаем 200 OK.")

    # Создаем стандартный ответ 200 OK
    response = JSONResponse(content=data)

    # Добавляем сгенерированный ETag в заголовок ответа
    response.headers["ETag"] = etag

    return response


# Дополнительный эндпоинт для имитации изменения данных (Шаг 7)
@app.post("/update")
def update_resource():
    """Имитирует изменение данных, что приведет к новому ETag."""
    global data
    data["version"] += 1
    data["title"] = f"Updated resource v{data['version']}"
    logging.warning(f"🚨 Данные обновлены. Новый ETag будет сгенерирован при следующем запросе.")
    return {"status": "ok", "new_version": data['version']}
