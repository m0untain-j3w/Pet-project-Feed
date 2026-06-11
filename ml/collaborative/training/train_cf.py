import logging
from pathlib import Path

import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

from app.core.logger import setup_logging

DATA_PATH = Path("data/raw/ml-100k/u.data")
MODEL_PATH = Path("ml/models/collaborative/model.joblib")

setup_logging()
log = logging.getLogger(__name__)


def train_cf(
    data_path: Path = DATA_PATH,
    model_path: Path = MODEL_PATH,
) -> None:
    df = pd.read_csv(
        data_path,
        sep="\t",
        names=["user_id", "item_id", "rating", "timestamp"],
    )

    pivot = df.pivot_table(
        index="user_id",
        columns="item_id",
        values="rating",
    ).fillna(0)

    similarity_matrix = cosine_similarity(pivot.T)

    movie_ids = sorted(pivot.columns.tolist())

    rating_counts = df.groupby("item_id")["rating"].count().to_dict()

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "movie_ids": movie_ids,
            "similarity_matrix": similarity_matrix,
            "rating_counts": rating_counts,
        },
        model_path,
    )
    log.info(f"Model saved to {model_path}")


if __name__ == "__main__":
    train_cf()
