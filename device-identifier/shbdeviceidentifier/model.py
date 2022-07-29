from abc import ABC, abstractmethod


class Model(ABC):
    name: str = None
    version: str = None
    description: str = None

    def __init__(self):
        ...

    @abstractmethod
    def train(self, data: list) -> None:
        ...

    @abstractmethod
    def predict(self, data: list) -> list:
        ...

    @abstractmethod
    def save(self, path: str) -> None:
        ...

    @abstractmethod
    def load(self, path: str) -> None:
        ...
   