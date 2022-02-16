import abc
from typing import Any


class Source(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def load(source: str) -> bool:
        pass

    @abc.abstractclassmethod
    def generate(self) -> Any:
        pass
