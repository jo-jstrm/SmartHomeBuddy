from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class MLModel(ABC):
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
