import logging
import sys
from pathlib import Path

from loguru import logger

from app.core.config import settings

LOGS_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame = logging.currentframe().f_back
            depth = 1
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )
        except Exception:  # noqa: BLE001
            self.handleError(record)


def setup_logging():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(sys.stdout, level=settings.LOG_LEVEL, format=LOG_FORMAT, colorize=True)

    logger.add(
        LOGS_DIR / "debug.log",
        encoding="utf-8",
        filter=lambda record: record["level"].name == "DEBUG",
        rotation="10 MB",
        retention="1 month",
        compression="gz",
    )
    logger.add(
        LOGS_DIR / "info.log",
        encoding="utf-8",
        filter=lambda record: record["level"].name == "INFO",
        rotation="10 MB",
        retention="1 month",
        compression="gz",
    )
    logger.add(
        LOGS_DIR / "warning.log",
        encoding="utf-8",
        filter=lambda record: record["level"].name == "WARNING",
        rotation="10 MB",
        retention="1 month",
        compression="gz",
    )
    logger.add(
        LOGS_DIR / "error.log",
        encoding="utf-8",
        level="ERROR",
        rotation="10 MB",
        retention="1 month",
        compression="gz",
    )
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=0,
        force=True,
    )

    for name in (
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "sqlalchemy.engine",
        "aiogram",
    ):
        logging.getLogger(name).handlers = [InterceptHandler()]
        logging.getLogger(name).propagate = False
