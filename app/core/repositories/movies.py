from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Movie, db_helper


class MovieRepository:

    @staticmethod
    async def get_all(
            session: Annotated[
                "AsyncSession",
                Depends(db_helper.session_getter),
            ],
            limit: int = 20,
            offset: int = 0,
    ):
        stmt = (
            select(Movie)
            .limit(limit)
            .offset(offset)
        )

        result = await session.execute(stmt)

        return result.scalars().all()

    @staticmethod
    async def get_by_id(
            session: AsyncSession,
            movie_id: int,
    ):
        stmt = select(Movie).where(Movie.id == movie_id)

        result = await session.execute(stmt)

        return result.scalar_one_or_none()
