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

    @staticmethod
    def prepare_train_data(train_df: pd.DataFrame) -> pd.DataFrame:
        # Modify the data to be in the format required by the model
        # Drop columns and set time index
        relevant_columns = ["timestamp", "src", "dst", "stream_id", "data_len", "L4_protocol"]
        train_df = train_df[relevant_columns]
        # TODO: Determine how the label is calculated. Currently only the source IP is used.
        #  Furthermore we could add them to the data frame and only supply the model with the column names for the labels.
        #  To add them as columns:
        # train_df['src_label'] = train_df.apply(lambda row: train_labels.get(row['src'].split(":")[0], "NoLabel"), axis=1)
        # train_df['dst_label'] = train_df.apply(lambda row: train_labels.get(row['dst'].split(":")[0], "NoLabel"), axis=1)
        return train_df
