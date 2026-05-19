from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.models.access_tokens import AccessToken


async def get_access_token_db(
        session: AsyncSession = Depends(db_helper.get_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)