from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(column='user.id', ondelete="cascade"),
        nullable=False,
    )
