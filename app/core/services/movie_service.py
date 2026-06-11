from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repositories.movies import MovieRepository


class MovieService:

    @staticmethod
    async def get_movies(
        session: AsyncSession,
        limit: int,
        offset: int,
    ):
        return await MovieRepository.get_all(
            session=session,
            limit=limit,
            offset=offset,
        )

    @staticmethod
    async def get_movie(
        session: AsyncSession,
        movie_id: int,
    ):
        return await MovieRepository.get_by_id(
            session=session,
            movie_id=movie_id,
        )