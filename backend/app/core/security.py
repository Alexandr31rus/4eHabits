from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from app.core.config import settings
from app.core.logger import logger

password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    """Хеширует пароль с помощью Argon2.

    Args:
        password: пароль в открытом виде.

    Returns:
        Строка с Argon2-хешем (включая соль).
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли пароль сохранённому хешу."""
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создаёт JWT-токен доступа.

    Args:
        data: данные для payload (например, {"sub": "42"}).
        expires_delta: время жизни токена. Если не указано,
            берётся из settings.JWT_EXPIRE_MINUTES.

    Returns:
        Подписанный JWT-токен в виде строки.
    """
    payload = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    )
    payload["exp"] = expire
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Декодирует JWT и возвращает payload.

    Args:
        token: JWT-строка.

    Returns:
        Payload словаря, если токен валиден и не истёк.
        None, если токен истёк или невалиден.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Токен истёк")
        return None
    except jwt.InvalidTokenError as error:
        logger.warning("Невалидный токен: {} - {}", type(error).__name__, str(error))
        return None
