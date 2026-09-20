from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Схема регистрации нового пользователя.

    Используется в эндпоинте POST /auth/register.
    Пароль приходит в открытом виде и хешируется перед сохранением в БД.
    """

    telegram_id: int = Field(gt=0)
    username: str | None = Field(default=None, min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    """Схема пользователя для ответа API.

    Не содержит hashed_password — пароль и его хеш никогда не покидают сервер.
    Поддерживает создание из ORM-объекта благодаря from_attributes=True.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    telegram_id: int
    username: str | None
    created_at: datetime


class UserLogin(BaseModel):
    """Схема аутентификации пользователя.

    Используется в эндпоинте POST /auth/login.
    Идентификация по telegram_id, подтверждение — паролем.
    """

    telegram_id: int = Field(gt=0)
    password: str
