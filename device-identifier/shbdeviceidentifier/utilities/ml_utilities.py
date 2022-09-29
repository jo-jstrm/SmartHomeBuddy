from shbdeviceidentifier.models import MLModel
from ..db import Database


def get_model(selector: str) -> MLModel:
    """
    Returns the model for the given selector.
    """
    # TODO: implement multiple models
    if selector in ["", "default", "rf", "RandomForest"]:
        from shbdeviceidentifier.ml_models import RandomForest

        return RandomForest()
    else:
        raise ValueError(f"Unknown model selector: {selector}")
