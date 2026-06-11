from pathlib import Path

import joblib
import numpy as np

MODEL_PATH = Path("ml/models/content_based/model.joblib")


class Recommender:
    def __init__(self, model_path: Path = MODEL_PATH):
        """
            Load the trained model (movie_ids + similarity matrix) from disk
        """
        data = joblib.load(model_path)
        self.movie_ids = data["movie_ids"]
        self.similarity_matrix = data["similarity_matrix"]

    def recommend(self, movie_id: int, top_n: int = 10) -> list[dict]:
        """
            Return top-N most similar movies for a given movie_id

            Results exclude the input movie itself.
            Each result: {"movie_id": int, "score": float}
        """
        try:
            idx = self.movie_ids.index(movie_id)
        except ValueError:
            return []

        scores = self.similarity_matrix[idx]
        return self._top_n(scores, exclude={movie_id}, top_n=top_n)

    def recommend_multiple(
        self, movie_ids: list[int], top_n: int = 10
    ) -> list[dict]:
        """
            Return top-N movies based on averaged similarity from multiple liked movies

            Useful when a user has rated several movies — average their similarity
            vectors and recommend the closest matches
        """
        indices = []
        for m_id in movie_ids:
            try:
                indices.append(self.movie_ids.index(m_id))
            except ValueError:
                continue

        if not indices:
            return []

        avg_scores = self.similarity_matrix[indices].mean(axis=0)
        return self._top_n(avg_scores, exclude=set(movie_ids), top_n=top_n)

    def _top_n(
        self,
        scores: np.ndarray,
        exclude: set[int],
        top_n: int,
    ) -> list[dict]:
        """
            Extract top-N results from a scores array, excluding specified IDs
        """
        top_indices = np.argsort(scores)[::-1]
        results = []
        for i in top_indices:
            mid = self.movie_ids[i]
            if mid in exclude:
                continue
            results.append({"movie_id": mid, "score": float(scores[i])})
            if len(results) == top_n:
                break
        return results
