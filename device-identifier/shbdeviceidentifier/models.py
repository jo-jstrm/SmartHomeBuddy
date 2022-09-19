from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class MLModel(ABC):
    """Base class for all ML models. Derived models must implement all methods."""

    name: str = None
    version: str = None
    description: str = None

    def __init__(self):
        ...

    @abstractmethod
    def train(self, X: pd.DataFrame, y: np.ndarray) -> bool:
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def prepare_train_data(train_df: pd.DataFrame) -> pd.DataFrame:
        pass
