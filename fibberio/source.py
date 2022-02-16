import abc
from typing import Any

from .distribution import Distribution


class Source(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def generate(distribution: Distribution) -> Any:
        pass


class FileSource(Source):
    def __init__(self, file: str) -> None:
        self.file = file
        self.thing = {
            "prop1": 2,
            "prop2": 'setting'
        }
        # load
        pass

    def generate(distribution: Distribution) -> Any:
        pass


class RangeSource(Source):
    def __init__(self) -> None:
        # [a, b] the closed interval {x ∈ ℝ : a ⩽ x ⩽ b}
        # [a, b) the interval {x ∈ ℝ : a ⩽ x < b}
        # (a, b] the interval {x ∈ ℝ : a < x ⩽ b}
        # (a, b) the open interval {x ∈ ℝ : a < x < b}
        self.type = "float"
        self.start = 0.0
        self.end = 1.0
        self.start_open = False
        self.end_open = False
        self.precision = 2

    def generate(distribution: Distribution) -> Any:
        pass
