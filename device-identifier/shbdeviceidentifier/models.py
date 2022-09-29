from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd


class MLModel(ABC):
    """Base class for all ML models. Derived models must implement all methods."""

    name: str
    alias: str
    ext_aliases: List[str]
    version: str
    description: str
    progress_range: range
    save_path: Optional[Path]

    def __init__(self):
        ...

    @abstractmethod
    def train(self, X: pd.DataFrame, y: np.ndarray, progress_callback=None) -> bool:
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def save(self, path: str = None) -> None:
        pass

    @abstractmethod
    def load(self, path: str = None) -> None:
        pass

    @staticmethod
    @abstractmethod
    def prepare_train_data(train_df: pd.DataFrame) -> pd.DataFrame:
        pass
