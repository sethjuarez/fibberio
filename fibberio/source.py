import abc
from typing import Any
from pathlib import Path
from .distribution import Distribution


class Source(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def generate(distribution: Distribution) -> Any:
        pass

    @abc.abstractclassmethod
    def validate(self) -> bool:
        pass


class FileSource(Source):
    def __init__(self) -> None:
        self.reference = ""
        self.path = Path(".")

    def generate(distribution: Distribution) -> Any:
        pass

    def validate(self) -> bool:
        # check reference
        pass

    def __repr__(self) -> str:
        return f"InlineSource({self.reference}, {self.path})"


class RangeSource(Source):
    def __init__(
        self,
        start_open: bool = False,
        start: float = 0,
        end: float = 0,
        end_open: bool = False,
        val_type: str = "float",
        precision: int = 2
    ) -> None:
        self.start_open = start_open
        self.start = start
        self.end = end
        self.end_open = end_open
        self.type = val_type
        self.precision = precision

    def generate(distribution: Distribution) -> Any:
        pass

    def validate(self) -> bool:
        pass


class DiscreteSource(Source):
    def __init__(self, source: list = []) -> None:
        self.source = source

    def generate(distribution: Distribution) -> Any:
        pass

    def validate(self) -> bool:
        pass
