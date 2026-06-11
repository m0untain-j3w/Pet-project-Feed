from pathlib import Path

import joblib

from ml.recommender import Recommender

MODEL_PATH = Path("ml/models/collaborative/model.joblib")


class CollabRecommender(Recommender):
    def __init__(self, model_path: Path = MODEL_PATH):
        super().__init__(model_path)
        data = joblib.load(model_path)
        self.rating_counts = data.get("rating_counts", {})
