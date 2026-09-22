from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.core.security import create_access_token, hash_password, verify_password
from app.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserLogin


class AuthService:
    """Сервис аутентификации и регистрации."""

    async def register(self, session: AsyncSession, data: UserCreate) -> User:
        """Регистрирует нового пользователя.

        Raises:
            UserAlreadyExistsError: если telegram_id уже занят.
        """
        existing = await user_repository.get_by_telegram_id(session, data.telegram_id)
        if existing is not None:
            raise UserAlreadyExistsError(data.telegram_id)
        hashed_password = hash_password(data.password)
        user = await user_repository.create(
            session,
            telegram_id=data.telegram_id,
            username=data.username,
            hashed_password=hashed_password,
        )
        await session.commit()
        logger.info(
            "Зарегистрирован пользователь id={} telegram_id={}",
            user.id,
            data.telegram_id,
        )
        return user

    async def authenticate(self, session: AsyncSession, data: UserLogin) -> User:
        """Проверяет учётные данные и возвращает пользователя.

        Raises:
            InvalidCredentialsError: если пользователь не найден или пароль неверный.
        """
        user = await user_repository.get_by_telegram_id(session, data.telegram_id)
        if user is None or not verify_password(data.password, user.hashed_password):
            logger.warning(
                "Неудачная попытка входа для telegram_id={}", data.telegram_id
            )
            raise InvalidCredentialsError()
        logger.info("Успешный вход для user id={}", user.id)
        return user

    def create_token(self, user: User) -> str:
        """Создаёт JWT-токен для пользователя."""
        payload = {"sub": str(user.id)}
        return create_access_token(payload)


auth_service = AuthService()
