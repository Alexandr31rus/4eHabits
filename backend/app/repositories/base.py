from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.db.base import Base


class BaseRepository[ModelType: Base]:
    """Базовый репозиторий с общими CRUD-операциями."""

    model: type[ModelType]

    async def get_by_id(self, session: AsyncSession, obj_id: int) -> ModelType | None:
        """Возвращает объект по id или None."""
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self, session: AsyncSession, limit: int = 100, offset: int = 0
    ) -> list[ModelType]:
        """Возвращает список объектов с пагинацией."""
        result = await session.execute(select(self.model).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, **kwargs: Any) -> ModelType:
        """Создаёт объект и возвращает его с заполненным id.

        Использует flush вместо commit — транзакцию завершает вызывающий код.
        """
        obj = self.model(**kwargs)
        session.add(obj)
        await session.flush()
        logger.debug("Создан {} с id={}", self.model.__name__, obj.id)
        return obj

    async def update(
        self, session: AsyncSession, obj: ModelType, data: dict[str, Any]
    ) -> ModelType:
        """Обновляет поля объекта из словаря data.

        Обычно data — это model_dump(exclude_unset=True) из Pydantic-схемы.
        """
        for field, value in data.items():
            setattr(obj, field, value)
        await session.flush()
        logger.debug("Обновлён {} id={}", self.model.__name__, obj.id)
        return obj

    async def delete(self, session: AsyncSession, obj: ModelType) -> None:
        """Удаляет объект из БД (через flush, без commit)."""
        await session.delete(obj)
        await session.flush()
        logger.debug("Удалён {} id={}", self.model.__name__, obj.id)
