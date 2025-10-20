from sqlalchemy.orm import Session
from .. import crud
from ..schemas import UserBase


def get_user_info(db: Session, user_id: int):
    """
    Бизнес-логика: получает пользователя, проверяет его наличие
    и возвращает только нужные данные.
    """

    # 1. Вызываем чистую функцию из CRUD
    user = crud.get_user_by_id(db, user_id)

    # 2. Бизнес-правило (Проверка, которая была бы в сервисе)
    if not user:
        # В реальном приложении здесь была бы HTTPException,
        # но для простоты ЛР возвращаем словарь.
        return {"error": "User not found"}

    # 3. Форматирование ответа
    # Используем схему Pydantic для корректного форматирования данных
    return UserBase.model_validate(user).model_dump()

# Примечание: Для создания пользователя логику также нужно перенести сюда,
# но для ЛР достаточно показать логику чтения.