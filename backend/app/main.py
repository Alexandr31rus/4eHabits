from app.core.logger import setup_logging

setup_logging()

from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI, Request  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

from app.api.v1.router import api_router  # noqa: E402
from app.core.logger import logger  # noqa: E402
from app.db.session import engine  # noqa: E402
from app.exceptions import (  # noqa: E402
    HabitNotFoundError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управляет жизненным циклом приложения."""
    logger.info("Запуск Habit Tracker API")
    yield
    logger.info("Остановка Habit Tracker API")
    await engine.dispose()


app = FastAPI(
    title="Habit Tracker API",
    description="API для трекинга привычек через Telegram-бот",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(
    request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(HabitNotFoundError)
async def habit_not_found_handler(
    request: Request, exc: HabitNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(api_router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Проверка доступности сервиса."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
