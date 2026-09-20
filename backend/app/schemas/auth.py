from pydantic import BaseModel


class Token(BaseModel):
    """Схема JWT-токена для ответа API.

    Возвращается эндпоинтом POST /auth/login.
    token_type всегда "bearer" — стандарт OAuth2.
    """

    access_token: str
    token_type: str = "bearer"
