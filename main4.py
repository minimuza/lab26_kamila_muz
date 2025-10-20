from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Task Manager API",
    description="Простое REST API для управления списком задач. Демонстрация документации OpenAPI.",
    version="1.0.0",
    contact={
        "name": "Студент",
        "email": "muzanbekova_kamila@example.com",
    },
)

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

tasks = []

@app.get("/tasks", summary="Список задач", description="Возвращает список всех задач из хранилища")
def get_tasks():
    return tasks

@app.post("/tasks", summary="Создать задачу", description="Добавляет новую задачу в список")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Задача создана", "task": task}

@app.get("/tasks/{task_id}", summary="Получить задачу", description="Возвращает задачу по её ID")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return {"error": "Задача не найдена"}