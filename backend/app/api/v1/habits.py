from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_active_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.schemas.habit_completion import HabitCompletionCreate, HabitCompletionRead
from app.services.habit import habit_service

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
async def create_habit(
    data: HabitCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Создаёт новую привычку для текущего пользователя."""
    return await habit_service.create_habit(session, current_user.id, data)


@router.get("", response_model=list[HabitRead])
async def get_habits(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Возвращает список привычек текущего пользователя."""
    return await habit_service.get_user_habits(session, current_user.id)


@router.get("/{habit_id}", response_model=HabitRead)
async def get_habit(
    habit_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Возвращает привычку по id, если она принадлежит пользователю."""
    return await habit_service.get_habit(session, habit_id, current_user.id)


@router.patch("/{habit_id}", response_model=HabitRead)
async def update_habit(
    habit_id: int,
    data: HabitUpdate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Обновляет поля привычки.

    Обновляются только переданные поля.
    """
    habit = await habit_service.get_habit(session, habit_id, current_user.id)
    return await habit_service.update_habit(session, habit, data)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Удаляет привычку и все её отметки."""
    habit = await habit_service.get_habit(session, habit_id, current_user.id)
    await habit_service.delete_habit(session, habit)


@router.post("/{habit_id}/track", response_model=HabitCompletionRead)
async def track_habit(
    habit_id: int,
    data: HabitCompletionCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
):
    """Отмечает выполнение привычки на указанную дату.

    Если отметка на эту дату уже есть — обновляет её.
    """
    await habit_service.get_habit(session, habit_id, current_user.id)
    return await habit_service.track_habit(
        session,
        habit_id=habit_id,
        completion_date=data.completion_date,
        is_completed=data.is_completed,
    )


@router.get("/{habit_id}/stats")
async def get_habit_stats(
    habit_id: int,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Возвращает статистику выполнения привычки."""
    habit = await habit_service.get_habit(session, habit_id, current_user.id)
    return await habit_service.get_habit_stats(session, habit)
