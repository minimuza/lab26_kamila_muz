import logging
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from typing import List
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")

app = FastAPI()

# Глобальный список для хранения всех активных WebSocket-подключений
clients: List[WebSocket] = []


# --- Шаг 3: Функция для рассылки уведомлений (Улучшенная версия) ---
async def broadcast(message: str):
    """Рассылает сообщение всем активным клиентам, корректно обрабатывая отключения."""
    logging.info(f"⚡ BROADCAST: Рассылка уведомления: {message}")

    # Список для хранения клиентов, которых нужно удалить после рассылки
    disconnected_clients = []

    for client in clients:
        try:
            # Попытка отправить сообщение
            await client.send_text(message)
        except (WebSocketDisconnect, RuntimeError) as e:
            # Если возникла ошибка (например, клиент закрыл соединение), помечаем его для удаления
            logging.warning(
                f"⚠️ Клиент {client.client.host if client.client else 'Unknown'} отключился во время рассылки: {e.__class__.__name__}")
            disconnected_clients.append(client)
        except Exception as e:
            logging.error(f"Неизвестная ошибка при отправке клиенту: {e}")
            disconnected_clients.append(client)

    # Удаление всех отключившихся клиентов из основного списка
    for client in disconnected_clients:
        try:
            clients.remove(client)
            logging.info(f"🔴 Удален неактивный клиент. Осталось: {len(clients)}")
        except ValueError:
            pass  # Клиент уже был удален другим потоком


# --- Шаг 2: WebSocket Роут ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Принятие подключения
    await websocket.accept()
    clients.append(websocket)

    client_host = websocket.client.host if websocket.client else "Unknown"
    logging.info(f"🟢 [WS CONNECT] Клиент {client_host} подключен. Всего: {len(clients)}")

    try:
        # Цикл для приема входящих сообщений от клиента (оригинальный код ЛР)
        while True:
            # receive_text() - ждет сообщение от клиента
            data = await websocket.receive_text()
            # Эхо-сообщение отправителю, чтобы убедиться, что канал работает
            await websocket.send_text(f"Вы отправили: {data}")

    except WebSocketDisconnect:
        # Обработка отключения, когда клиент закрывает соединение
        clients.remove(websocket)
        logging.info(f"🔴 [WS DISCONNECT] Клиент {client_host} отключен. Осталось: {len(clients)}")
    except Exception as e:
        # Обработка других ошибок
        logging.error(f"Ошибка в WebSocket-цикле для {client_host}: {e}")
        try:
            clients.remove(websocket)
        except ValueError:
            pass  # Уже удален


# --- Шаг 4: Эндпоинт для отправки уведомлений (HTTP POST) ---
@app.post("/notify")
async def send_notification(request: Request):
    try:
        data = await request.json()
        message = data.get('message', 'Нет сообщения')

        # Запускаем рассылку
        await broadcast(f"🚀 Уведомление: {message}")

        return JSONResponse(
            status_code=200,
            content={"status": "ok", "message_sent": message, "recipients": len(clients)}
        )
    except json.JSONDecodeError:
        return JSONResponse(status_code=400, content={"status": "error", "detail": "Неверный формат JSON"})
    except Exception as e:
        logging.error(f"Ошибка при обработке /notify: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "detail": "Внутренняя ошибка сервера"})
