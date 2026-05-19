from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Movie(Base):

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    genres: Mapped[str] = mapped_column(String(255))

    year: Mapped[int | None]