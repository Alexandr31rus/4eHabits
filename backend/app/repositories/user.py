from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с пользователями."""

    model = User

    async def get_by_telegram_id(
        self, session: AsyncSession, telegram_id: int
    ) -> User | None:
        """Возвращает пользователя по telegram_id или None."""
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()


user_repository = UserRepository()
