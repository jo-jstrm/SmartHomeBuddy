from shbdeviceidentifier.models import MLModel
from ..db import Database


def get_model(selector: str = "default") -> MLModel:
    """
    Returns the model for the given selector.
    """
    # TODO: implement multiple models
    # TODO: make sure selectors are the same as aliases in the model classes
    if selector in ["", "default", "rf", "RandomForest"]:
        from shbdeviceidentifier.ml_models import RandomForest

        return RandomForest()
    else:
        raise ValueError(f"Unknown model selector: {selector}")
