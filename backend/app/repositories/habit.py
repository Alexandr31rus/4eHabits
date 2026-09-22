from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion
from app.repositories.base import BaseRepository


class HabitRepository(BaseRepository[Habit]):
    """Репозиторий для работы с привычками."""

    model = Habit

    async def get_all_by_user_id(
        self, session: AsyncSession, user_id: int
    ) -> list[Habit]:
        """Возвращает все привычки пользователя."""
        result = await session.execute(select(Habit).where(Habit.user_id == user_id))
        return list(result.scalars().all())

    async def get_by_id_and_user_id(
        self, session: AsyncSession, habit_id: int, user_id: int
    ) -> Habit | None:
        """Возвращает привычку, если она принадлежит пользователю."""
        result = await session.execute(
            select(Habit).where(Habit.id == habit_id, Habit.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def count_completions(self, session: AsyncSession, habit_id: int) -> int:
        """Считает количество успешных выполнений привычки."""
        result = await session.execute(
            select(func.count(HabitCompletion.id)).where(
                HabitCompletion.habit_id == habit_id,
                HabitCompletion.is_completed.is_(True),
            )
        )
        return result.scalar_one()

    async def get_habits_to_transfer(
        self, session: AsyncSession, user_id: int
    ) -> list[Habit]:
        """Возвращает привычки, выполненные менее target_days раз."""
        completion_count = func.count(HabitCompletion.id).label("completion_count")
        result = await session.execute(
            select(Habit)
            .outerjoin(
                HabitCompletion,
                (HabitCompletion.habit_id == Habit.id)
                & (HabitCompletion.is_completed.is_(True)),
            )
            .where(Habit.user_id == user_id)
            .group_by(Habit.id)
            .having(completion_count < Habit.target_days)
        )
        return list(result.scalars().all())


habit_repository = HabitRepository()
