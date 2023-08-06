from typing import Type
from abc import abstractmethod
from .step import BaseStep

Step = Type[BaseStep]


class BasePypeline:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self):
        raise NotImplementedError("A derived Pypeline needs to have a run() method!")
