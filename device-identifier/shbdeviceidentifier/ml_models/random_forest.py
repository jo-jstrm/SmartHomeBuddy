import pickle

import pandas as pd
from loguru import logger
from sklearn.ensemble import RandomForestClassifier

from shbdeviceidentifier.models import MLModel
from ..utilities.app_utilities import resolve_file_path


class RandomForest(MLModel):
    """
    Random Forest Classifier
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.name = "Random Forest Classifier"
        self.version = "0.0"
        self.description = "Random Forest Classifier"

        self.model_kwargs = dict(n_estimators=100, random_state=0)
        self.model_kwargs.update(kwargs)
        self.model = RandomForestClassifier(**self.model_kwargs)

    def train(self, X, y) -> None:
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        return X.assign(prediction=self.model.predict(X))

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.model, f)
        logger.success(f"Saved model to {path}")

    def load(self, path: str) -> None:
        path = resolve_file_path(path)
        if path:
            with open(path, "rb") as f:
                self.model = pickle.load(f)
        else:
            logger.error(f"Cannot find ML model at {path}")
