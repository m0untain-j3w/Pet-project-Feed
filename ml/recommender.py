from pathlib import Path

import joblib
import numpy as np


class Recommender:
    def __init__(self, model_path: Path):
        data = joblib.load(model_path)
        self.movie_ids = data["movie_ids"]
        self.similarity_matrix = data["similarity_matrix"]

    def recommend(self, movie_id: int, top_n: int = 10) -> list[dict]:
        try:
            idx = self.movie_ids.index(movie_id)
        except ValueError:
            return []

        scores = self.similarity_matrix[idx]
        return self._top_n(scores, exclude={movie_id}, top_n=top_n)

    def _top_n(
        self,
        scores: np.ndarray,
        exclude: set[int],
        top_n: int,
    ) -> list[dict]:
        top_indices = np.argsort(scores)[::-1]
        results = []
        for i in top_indices:
            mid = self.movie_ids[i]
            if mid in exclude:
                continue
            results.append({"movie_id": mid, "score": round(float(scores[i]), 2)})
            if len(results) == top_n:
                break
        return results
