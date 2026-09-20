from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class HabitCompletionCreate(BaseModel):
    """Схема отметки выполнения привычки.

    Используется в эндпоинте POST /habits/{habit_id}/completions.
    По умолчанию is_completed=False — пользователь может отметить
    как «выполнено», так и «не выполнено».
    """

    habit_id: int = Field(gt=0)
    completion_date: date
    is_completed: bool = False


class HabitCompletionRead(BaseModel):
    """Схема отметки выполнения для ответа API.

    Поддерживает создание из ORM-объекта благодаря from_attributes=True.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    habit_id: int
    completion_date: date
    is_completed: bool
