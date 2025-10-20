from sqlalchemy.orm import Session
from . import models, schemas


# random больше не нужен
# import random

# В CRUD оставляем только чистую работу с БД
def get_user_by_id(db: Session, user_id: int):
    """Получить пользователя по ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_password_hash(password: str):
    # Используем простую имитацию хэширования
    return f"hashed_{password}"


def create_user(db: Session, user: schemas.UserCreate):
    """Создать нового пользователя."""
    fake_hashed_password = get_password_hash(user.password)

    # Модель SQLAlchemy сама позаботится об ID
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=fake_hashed_password
    )

    db.add(db_user)
    # Сохраняем изменения
    db.commit()
    # Обновляем объект, чтобы получить ID, который сгенерировала БД
    db.refresh(db_user)

    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получить список пользователей."""
    return db.query(models.User).offset(skip).limit(limit).all()