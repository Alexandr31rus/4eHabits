from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitCreate(BaseModel):
    """Схема создания новой привычки.

    Используется в эндпоинте POST /habits.
    target_days по умолчанию 21 — столько раз нужно выполнить привычку для закрепления.
    """

    title: str = Field(min_length=1, max_length=60)
    description: str | None = Field(default=None, max_length=255)
    goal: str | None = Field(default=None, max_length=100)
    target_days: int = Field(default=21, ge=1, le=365)


class HabitUpdate(BaseModel):
    """Схема частичного обновления привычки.

    Все поля опциональны. Применяется в PATCH /habits/{habit_id}.
    Используйте model_dump(exclude_unset=True), чтобы обновлять только переданные поля.
    """

    title: str | None = Field(default=None, min_length=1, max_length=60)
    description: str | None = Field(default=None, max_length=255)
    goal: str | None = Field(default=None, max_length=100)
    target_days: int | None = Field(default=None, ge=1, le=365)


class HabitRead(BaseModel):
    """Схема привычки для ответа API.

    Поддерживает создание из ORM-объекта благодаря from_attributes=True.
    Поля description и goal могут быть None (nullable в БД).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    goal: str | None
    target_days: int
    created_at: datetime
    user_id: int
