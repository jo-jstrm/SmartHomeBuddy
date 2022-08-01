from shbdeviceidentifier.models import MLModel


class RandomForestClassifier(MLModel):
    """
    Random Forest Classifier
    """

    def __init__(self):
        super().__init__()
        self.name = "Random Forest Classifier"
        self.version = "0.0"
        self.description = "Random Forest Classifier"

    def train(self, data: list) -> None:
        ...

    def predict(self, data: list) -> list:
        ...

    def save(self, path: str) -> None:
        ...

    def load(self, path: str) -> None:
        ...
