from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schemas.recommendation import MovieWithScore
from app.core.repositories.movies import MovieRepository
from app.core.repositories.ratings import RatingRepository
from ml.content_based.inference.recommend import Recommender


class RecommendationService:
    def __init__(self, recommender: Recommender):
        self.recommender = recommender

    async def for_user(
        self,
        session: AsyncSession,
        user_id: int,
        threshold: float = 4.0,
        top_n: int = 10,
    ) -> list[MovieWithScore]:
        ratings = await RatingRepository.get_user_ratings(
            session=session, user_id=user_id
        )
        if not ratings:
            return []

        liked_ids = [r.movie_id for r in ratings if r.rating >= threshold]
        results = self.recommender.recommend_multiple(liked_ids, top_n=top_n)

        return await self._enrich(session, results)

    async def for_movie(
        self,
        session: AsyncSession,
        movie_id: int,
        top_n: int = 10,
    ) -> list[MovieWithScore]:
        results = self.recommender.recommend(movie_id, top_n=top_n)
        return await self._enrich(session, results)

    @staticmethod
    async def _enrich(
        session: AsyncSession,
        results: list[dict],
    ) -> list[MovieWithScore]:
        if not results:
            return []

        movie_ids = [r["movie_id"] for r in results]
        movies = await MovieRepository.get_by_ids(session, movie_ids)
        movie_map = {m.id: m for m in movies}

        enriched = []
        for r in results:
            movie = movie_map.get(r["movie_id"])
            if movie is None:
                continue
            enriched.append(
                MovieWithScore(
                    id=movie.id,
                    title=movie.title,
                    genres=movie.genres,
                    year=movie.year,
                    score=round(r["score"], 3),
                )
            )
        return enriched
