from typing import Annotated
from fastapi import Depends
from app.core.models import db_helper
from app.core.models import Rating
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class RatingRepository:

    @staticmethod
    async def create(
        session: AsyncSession,
        user_id: int,
        movie_id: int,
        rating: int,
    ):
        raiting_obj = Rating(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating,
        )
        session.add(raiting_obj)
        await session.commit()

    @staticmethod
    async def update(
        session: AsyncSession,
        rating_id: int,
        new_rating: int,
    ) -> None:
        await session.execute(
            select(Rating)
            .where(Rating.id == rating_id)
            .update({Rating.rating: new_rating})
        )
        await session.commit()

    @staticmethod
    async def get_user_ratings(
        session: AsyncSession,
        user_id: int,
    ) -> list[Rating]:
        result = await session.execute(
            select(Rating)
            .where(Rating.user_id == user_id)
            .order_by(Rating.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_user_movie_rating(
        session: AsyncSession,
        user_id: int,
        movie_id: int,
    ) -> Rating | None:
        result = await session.execute(
            select(Rating).where(
                Rating.user_id == user_id,
                Rating.movie_id == movie_id,
            )
        )
        return result.scalar_one_or_none()
