from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base
from app.core.models.mixins.id_int_pk import IdIntPkMixin


class Movie(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(String(255))
    genres: Mapped[str] = mapped_column(String(255))

    year: Mapped[int | None]