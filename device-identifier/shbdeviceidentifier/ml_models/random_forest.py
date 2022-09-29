import pickle
from pathlib import Path

import pandas as pd
from loguru import logger
from sklearn.ensemble import RandomForestClassifier

from shbdeviceidentifier.models import MLModel
from ..utilities.app_utilities import resolve_file_path, DATA_DIR


class RandomForest(MLModel):
    """
    Random Forest Classifier
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.name = "Random Forest Classifier"
        self.alias = "RandomForest"
        self.ext_aliases = [
            "random_forest",
            "rf",
            "randomforest",
            "randomforestclassifier",
            "random_forest_classifier"
        ]
        self.version = "v0"
        self.description = "Random Forest Classifier"
        self.progress_range = range(0, 2, 1)

        # Get the save path (None if it does not exist)
        self.save_path = resolve_file_path(DATA_DIR / Path(f"ml_models/{self.alias}_{self.version}.pkl"))

        self.model_kwargs = dict(n_estimators=100, random_state=0)
        self.model_kwargs.update(kwargs)
        self.model = RandomForestClassifier(**self.model_kwargs)

    def train(self, X, y, progress_callback=None) -> bool:

        try:
            # Train
            self.model.fit(X, y)
        except Exception as e:
            logger.debug(e)
            return False

        # Update the progress bar
        # Since we only have one step, we can just set it to 100% once we're done
        # For more complicated models a callback should be used when fitting
        progress_callback(self.progress_range.step)
        return True

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        return X.assign(prediction=self.model.predict(X))

    def save(self, path: str = None) -> None:
        if not path:
            if not self.save_path:
                logger.error("No save path specified. Aborting save.")
                return
            path = self.save_path

        # Pickle model
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

        # Save the save path
        tmp_path = resolve_file_path(path)
        if not tmp_path:
            logger.warning(f"Cannot find ML model at {tmp_path} after saving. Saving path internally as {path}")
            tmp_path = path
        self.save_path = tmp_path

        logger.success(f"Saved model to {path}")

    def load(self, path: str = None) -> None:

        if not path:
            path = self.save_path
            if not path:
                raise FileNotFoundError("No model path found.")
        else:
            path = resolve_file_path(path)
            if not path:
                logger.error(f"Cannot find ML model at {path}. Aborting.")
                return

        with open(path, "rb") as f:
            self.model = pickle.load(f)

    @staticmethod
    def prepare_train_data(train_df: pd.DataFrame) -> pd.DataFrame:
        # Modify the data to be in the format required by the model
        # Drop columns and set time index
        relevant_columns = ["timestamp", "stream_id", "data_len", "L4_protocol"]
        train_df = train_df[relevant_columns]
        # TODO: Determine how the label is calculated. Currently only the source IP is used.
        #  Furthermore we could add them to the data frame and only supply the model with the column names for the labels.
        #  To add them as columns:
        # train_df['src_label'] = train_df.apply(lambda row: train_labels.get(row['src'].split(":")[0], "NoLabel"), axis=1)
        # train_df['dst_label'] = train_df.apply(lambda row: train_labels.get(row['dst'].split(":")[0], "NoLabel"), axis=1)
        return train_df
