from pydantic import BaseModel


# Схема для создания нового пользователя (принимаемые данные)
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# Схема для ответа (возвращаемые данные, исключаем пароль)
class UserBase(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        # Указываем Pydantic работать с объектами SQLAlchemy
        from_attributes = True
