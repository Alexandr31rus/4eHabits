from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user import User
from app.repositories.user import user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
) -> User:
    """Возвращает текущего пользователя по JWT-токену.

    Raises:
        HTTPException: 401, если токен невалиден или пользователь не найден.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user_id_to_int = int(user_id)
    except (TypeError, ValueError):
        raise credentials_exception from None

    user = await user_repository.get_by_id(session, user_id_to_int)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    """Обёртка над get_current_user для проверки активности пользователя.

    Сейчас просто возвращает пользователя. В будущем здесь можно
    добавить проверку is_active / is_banned и бросать 403.
    """
    return user
