from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.exceptions import HabitNotFoundError
from app.models.habit import Habit
from app.models.habit_completion import HabitCompletion
from app.repositories.habit import habit_repository
from app.repositories.habit_completion import habit_completion_repository
from app.schemas.habit import HabitCreate, HabitUpdate


class HabitService:
    """Сервис для работы с привычками."""

    async def create_habit(
        self, session: AsyncSession, user_id: int, data: HabitCreate
    ) -> Habit:
        """Создаёт новую привычку для пользователя."""
        habit = await habit_repository.create(
            session,
            user_id=user_id,
            title=data.title,
            description=data.description,
            goal=data.goal,
            target_days=data.target_days,
        )
        await session.commit()
        logger.info("Создана привычка id={} для user id={}", habit.id, user_id)
        return habit

    async def get_user_habits(self, session: AsyncSession, user_id: int) -> list[Habit]:
        """Возвращает все привычки пользователя."""
        return await habit_repository.get_all_by_user_id(session, user_id)

    async def get_habit(
        self, session: AsyncSession, habit_id: int, user_id: int
    ) -> Habit:
        """Возвращает привычку пользователя.

        Raises:
            HabitNotFoundError: привычка не найдена или не принадлежит пользователю.
        """
        habit = await habit_repository.get_by_id_and_user_id(session, habit_id, user_id)
        if habit is None:
            raise HabitNotFoundError(habit_id)
        return habit

    async def update_habit(
        self, session: AsyncSession, habit: Habit, data: HabitUpdate
    ) -> Habit:
        """Обновляет поля привычки.

        Обновляются только переданные поля (exclude_unset=True).
        """
        update_data = data.model_dump(exclude_unset=True)
        habit = await habit_repository.update(session, habit, update_data)
        await session.commit()
        logger.info("Обновлена привычка id={}", habit.id)
        return habit

    async def delete_habit(self, session: AsyncSession, habit: Habit) -> None:
        """Удаляет привычку и все её отметки (через CASCADE)."""
        await habit_repository.delete(session, habit)
        await session.commit()
        logger.info("Удалена привычка id={}", habit.id)

    async def track_habit(
        self,
        session: AsyncSession,
        habit_id: int,
        completion_date: date,
        is_completed: bool,
    ) -> HabitCompletion:
        """Отмечает выполнение привычки на дату.

        Если отметка на эту дату уже есть — обновляет её.
        Если нет — создаёт новую.
        """
        completion = await habit_completion_repository.get_by_habit_and_date(
            session, habit_id, completion_date
        )
        if completion is not None:
            completion = await habit_completion_repository.update(
                session, completion, {"is_completed": is_completed}
            )
        else:
            completion = await habit_completion_repository.create(
                session,
                habit_id=habit_id,
                completion_date=completion_date,
                is_completed=is_completed,
            )
        await session.commit()
        logger.info(
            "Отметка habit id={} на {}: is_completed={}",
            habit_id,
            completion_date,
            is_completed,
        )
        return completion

    async def get_habit_stats(self, session: AsyncSession, habit: Habit) -> dict:
        """Возвращает статистику выполнения привычки."""
        count = await habit_repository.count_completions(session, habit.id)
        return {
            "habit_id": habit.id,
            "total_completions": count,
            "target_days": habit.target_days,
            "is_achieved": count >= habit.target_days,
        }


habit_service = HabitService()
