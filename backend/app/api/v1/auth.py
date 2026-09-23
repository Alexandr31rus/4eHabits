from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """Регистрирует нового пользователя.

    Returns:
        Данные созданного пользователя без пароля.

    Raises:
        UserAlreadyExistsError: если telegram_id уже занят.
    """
    return await auth_service.register(session, data)


@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> Token:
    """Аутентифицирует пользователя и возвращает JWT-токен.

    Raises:
        InvalidCredentialsError: если telegram_id не найден или пароль неверный.
    """
    user = await auth_service.authenticate(session, data)
    token = auth_service.create_token(user)
    return Token(access_token=token)
