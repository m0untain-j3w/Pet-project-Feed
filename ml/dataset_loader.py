from pathlib import Path

import pandas as pd


def load_genre_names(genres_path: Path) -> list[str]:
    return pd.read_csv(
        genres_path,
        sep="|",
        header=None,
    )[0].tolist()


def load_movielens_items(
    movies_path: Path = Path("data/raw/ml-100k/u.item"),
    genres_path: Path = Path("data/raw/ml-100k/u.genre"),
) -> pd.DataFrame:
    genres = load_genre_names(genres_path)

    columns = [
        "movie_id",
        "title",
        "release_date",
        "video_release_date",
        "IMDb_URL",
        *genres,
    ]

    df = pd.read_csv(
        movies_path, sep="|", encoding="latin-1", header=None, names=columns
    )

    movies = []
    for _, row in df.iterrows():
        movie_genres = [g for g in genres if row[g] == 1]
        genres_str = ", ".join(movie_genres)

        release_year = None
        if pd.notna(row["release_date"]):
            try:
                release_year = int(str(row["release_date"])[-4:])
            except Exception:
                pass

        movies.append(
            {
                "movie_id": int(row["movie_id"]),
                "title": row["title"],
                "genres": genres_str,
                "year": release_year,
            }
        )

    return pd.DataFrame(movies)
