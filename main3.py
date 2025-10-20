from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Модель задачи (Task Model)
class Task(BaseModel):
    id: int
    title: str
    done: bool = False

# Хранилище (пока список в памяти) (In-memory storage)
tasks = []

# ---

## 1. Получить список всех задач (GET)
@app.get("/tasks")
def get_tasks():
    """Возвращает полный список задач."""
    return tasks



## 2. Добавить новую задачу (POST)
@app.post("/tasks")
def create_task(task: Task):
    """Создает новую задачу и добавляет ее в список."""
    # Проверка на дублирование id (простая реализация для примера)
    if any(t.id == task.id for t in tasks):
        raise HTTPException(status_code=400, detail=f"Task with id {task.id} already exists")

    tasks.append(task)
    return {"message": "Task created", "task": task}


## 3. Обновить задачу по id (PUT)
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    """Обновляет существующую задачу по ее ID."""
    for i, task in enumerate(tasks):
        if task.id == task_id:
            # Важно: убедиться, что ID в URL и в теле запроса совпадают
            if task_id != updated_task.id:
                 raise HTTPException(status_code=400, detail="ID in path and body must match")

            tasks[i] = updated_task
            return {"message": "Task updated", "task": updated_task}

    # Если задача не найдена, выбрасываем исключение
    raise HTTPException(status_code=404, detail="Task not found")


## 4. Удалить задачу по id (DELETE)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Удаляет задачу по ее ID."""
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return {"message": "Task deleted"}

    # Если задача не найдена, выбрасываем исключение
    raise HTTPException(status_code=404, detail="Task not found")





