import abc
from pathlib import Path
from typing import Any

from .distribution import Distribution


class Source(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def generate(distribution: Distribution) -> Any:
        pass

    @abc.abstractclassmethod
    def validate(self) -> bool:
        pass


class InlineSource(Source):
    def __init__(self) -> None:
        self.reference = ""
        self.path = Path(".")

    def generate(distribution: Distribution) -> Any:
        pass

    def validate(self) -> bool:
        # check reference
        pass

    def __repr__(self) -> str:
        return f'InlineSource({self.reference}, {self.path})'


class RangeSource(Source):
    def __init__(self) -> None:
        self.type = "float"
        self.start = 0.0
        self.end = 1.0
        self.start_open = False
        self.end_open = False
        self.precision = 2

    def generate(distribution: Distribution) -> Any:
        pass
