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


def classify_devices(db: Database):
    """Dummy function."""
    devices = [
        {"name": "Google Home Mini", "mac_address": "ef:00:49:01:1a:ff"},
        {"name": "Amazon Echo Dot", "mac_address": "00:a0:00:19:2e:01"},
    ]
    for device in devices:
        db.write_device(device["name"], device["mac_address"])