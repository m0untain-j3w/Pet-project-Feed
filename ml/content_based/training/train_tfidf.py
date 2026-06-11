from pathlib import Path
import joblib
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.core.logger import setup_logging

import pandas as pd


def train_tfidf(
    features_path: Path = Path("data/processed/movies_with_genres.parquet"),
    model_path: Path = Path("ml/models/content_based/model.joblib"),
) -> None:
    df = pd.read_parquet(features_path)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df["genres"])
    similarity_matrix = cosine_similarity(tfidf_matrix)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "movie_ids": df["movie_id"].tolist(),
            "similarity_matrix": similarity_matrix,
        },
        model_path,
    )
    log.info(f"Trained TF-IDF on {len(df)} movies. Saved to {model_path}")


if __name__ == "__main__":
    setup_logging()
    log = logging.getLogger(__name__)
    train_tfidf()
