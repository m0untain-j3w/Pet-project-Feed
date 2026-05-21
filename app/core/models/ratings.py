from sqlalchemy import ForeignKey, Integer, mapped_column

from .base import Base
from .mixins.id_int_pk import IdIntPkMixin


class Rating(Base, IdIntPkMixin):
    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    movie_id = mapped_column(Integer, ForeignKey("movie.id"), nullable=False)
    rating = mapped_column(Integer, nullable=False)
    created_at = mapped_column(Integer, nullable=False)