from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column='users.id', ondelete="cascade"),
        nullable=False,
    )
