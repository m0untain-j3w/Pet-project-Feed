import asyncio

from sqlalchemy import insert

from app.core.models import Movie, db_helper
from ml.dataset_loader import load_movielens_items


async def import_movies_into_db():
    df = load_movielens_items()

    movies = df.rename(columns={"movie_id": "id"}).to_dict(orient="records")

    async with db_helper.session_factory() as session:
        await session.execute(insert(Movie), movies)
        await session.commit()

    print(f"Imported {len(movies)} movies into DB")


if __name__ == "__main__":
    asyncio.run(import_movies_into_db())