from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Integer, DateTime
from sqlalchemy.orm import mapped_column

from app.core.models.base import Base
from app.core.models.mixins.id_int_pk import IdIntPkMixin


class Rating(Base, IdIntPkMixin):
    user_id = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    movie_id = mapped_column(
        Integer,
        ForeignKey("movies.id"),
        nullable=False,
    )
    rating = mapped_column(
        Integer,
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
