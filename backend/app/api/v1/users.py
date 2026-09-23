from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """Возвращает профиль текущего пользователя.

    Требует авторизации через JWT-токен.
    """
    return current_user
