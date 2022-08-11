from shbdeviceidentifier.ml_models import RandomForest
from shbdeviceidentifier.models import MLModel


def get_model(selector: str) -> MLModel:
    """
    Returns the model for the given selector.
    """
    # TODO: implement multiple models
    if selector == 'default' or selector == 'rf' or selector == 'RandomForest':
        return RandomForest()
    else:
        raise ValueError(f"Unknown model selector: {selector}")
