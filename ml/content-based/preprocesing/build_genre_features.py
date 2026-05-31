from pathlib import Path

from ml.dataset_loader import load_movielens_items


def build_genre_features(
    movies_path: Path = Path("data/raw/ml-100k/u.item"),
    genres_path: Path = Path("data/raw/ml-100k/u.genre"),
    output_path: Path = Path("data/processed/movies_with_genres.parquet"),
):
    df = load_movielens_items(movies_path, genres_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    print(f"Saved {len(df)} movies to {output_path}")


if __name__ == "__main__":
    build_genre_features()