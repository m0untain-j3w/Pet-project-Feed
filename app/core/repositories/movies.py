from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Movie, db_helper


class MovieRepository:

    @staticmethod
    async def get_all(
        session: AsyncSession,
        limit: int = 20,
        offset: int = 0,
    ):
        result = await session.execute(
            select(Movie).limit(limit).offset(offset),
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id(
        session: AsyncSession,
        movie_id: int,
    ):
        result = await session.execute(
            select(Movie).where(Movie.id == movie_id),
        )
        return result.scalar_one_or_none()
