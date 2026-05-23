import asyncio
from pathlib import Path

import pandas as pd
from sqlalchemy import insert

from app.core.models import (
    Movie,
    db_helper,
)


async def import_movies_into_db():
    DATASET_PATH = Path("data/raw/ml-100k/u.item")
    GENRES_PATH = Path("data/raw/ml-100k/u.genre")

    GENRES = pd.read_csv(  # type: ignore
        GENRES_PATH,
        sep="|",
        header=None,
    )[0]

    COLUMNS = [
        "movie_id",
        "title",
        "release_date",
        "video_release_date",
        "IMDb_URL",
        *GENRES,
    ]

    df = pd.read_csv(
        DATASET_PATH,
        sep="|",
        encoding="latin-1",
        header=None,
        names=COLUMNS,
    )
    movies = []

    for _, row in df.iterrows():  # type: ignore
        movie_genres = []
        for genre in GENRES:
            if row[genre] == 1:
                movie_genres.append(genre)

        # TODO: Строка жанров временна, потом разделить, наверно
        genres_str = ", ".join(movie_genres)

        release_year = None
        if pd.notna(row["movie_id"]):
            try:
                release_year = int(str(row["release_date"])[-4:])
            except Exception:
                pass

        movie = {
            "id": int(row["movie_id"]),
            "title": row["title"],
            "genres": genres_str,
            "year": release_year,
        }
        movies.append(movie)

    async with db_helper.session_factory() as session:
        await session.execute(
            insert(Movie), movies,
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(import_movies_into_db())
