from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей.

    Содержит общее поле id — primary key для всех таблиц.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
