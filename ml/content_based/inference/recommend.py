from pathlib import Path

from ml.recommender import Recommender

MODEL_PATH = Path("ml/models/content_based/model.joblib")

class CBRecommender(Recommender):
    def __init__(self, model_path: Path = MODEL_PATH):
        super().__init__(model_path)