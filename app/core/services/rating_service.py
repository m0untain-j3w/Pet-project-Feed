from app.core.repositories.ratings import RatingRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schemas.rating import RatingCreate


class RatingService:

    @staticmethod
    async def rate_movie(
        session: AsyncSession,
        user_id: int,
        raiting_data: RatingCreate,
    ) -> None:
        if not 1 <= raiting_data.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        existing = await RatingRepository.get_user_movie_rating(
            session=session,
            user_id=user_id,
            movie_id=raiting_data.movie_id,
        )

        if existing:
            await RatingRepository.update(
                session=session,
                rating_id=existing.id,
                new_rating=raiting_data.rating,
            )
        else:
            await RatingRepository.create(
                session=session,
                user_id=user_id,
                movie_id=raiting_data.movie_id,
                rating=raiting_data.rating,
            )

    @staticmethod
    async def get_user_ratings(
        session: AsyncSession,
        user_id: int,
    ):
        return await RatingRepository.get_user_ratings(
            session=session,
            user_id=user_id,
        )
