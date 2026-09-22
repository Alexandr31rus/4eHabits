from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit_completion import HabitCompletion
from app.repositories.base import BaseRepository


class HabitCompletionRepository(BaseRepository[HabitCompletion]):
    """Репозиторий для работы с отметками выполнения."""

    model = HabitCompletion

    async def get_by_habit_and_date(
        self, session: AsyncSession, habit_id: int, completion_date: date
    ) -> HabitCompletion | None:
        """Возвращает отметку привычки на конкретную дату или None."""
        result = await session.execute(
            select(HabitCompletion).where(
                HabitCompletion.habit_id == habit_id,
                HabitCompletion.completion_date == completion_date,
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_habit(
        self, session: AsyncSession, habit_id: int
    ) -> list[HabitCompletion]:
        """Возвращает все отметки привычки."""
        result = await session.execute(
            select(HabitCompletion).where(HabitCompletion.habit_id == habit_id)
        )
        return list(result.scalars().all())


habit_completion_repository = HabitCompletionRepository()
