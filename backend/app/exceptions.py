class AppError(Exception):
    """Базовое исключение приложения."""


class UserAlreadyExistsError(AppError):
    """Пользователь с таким telegram_id уже зарегистрирован."""

    def __init__(self, telegram_id: int) -> None:
        self.telegram_id = telegram_id
        super().__init__("Пользователь уже зарегистрирован")


class InvalidCredentialsError(AppError):
    """Неверный telegram_id или пароль."""

    def __init__(self) -> None:
        super().__init__("Неверные учётные данные")
