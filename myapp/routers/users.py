from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db, Base, engine
# Импорт сервисного слоя
from ..services import user_service

# Создаем таблицы в БД при запуске
Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# Роут для создания пользователя - теперь без лишних проверок, используем только crud
@router.post("/", response_model=schemas.UserBase, status_code=201)
def create_user_route(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя."""

    # !!! ИСПРАВЛЕНИЕ: Удалена строка с ошибкой (например, crud_user = crud.get_user(db, user_id=1))

    return crud.create_user(db=db, user=user)


# Роут для получения списка пользователей остается без изменений
@router.get("/", response_model=list[schemas.UserBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получение списка пользователей."""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# Роут для получения одного пользователя - использует сервис
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получение информации о пользователе через сервисный слой."""

    # Роутер просто вызывает сервис, передавая ему ID и сессию БД
    user_data = user_service.get_user_info(db, user_id)

    # Роутер обрабатывает возможную ошибку, возвращенную сервисом
    if "error" in user_data:
        # Теперь роутер возвращает стандартный HTTP 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_data["error"]
        )

    return user_data