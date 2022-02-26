import abc
import numpy as np
from time import time
from typing import Any, Union


class Distribution(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.rng = np.random.default_rng(int(time() * 1000))

    @abc.abstractclassmethod
    def generate(self) -> Any:
        pass


class Discrete(Distribution):
    def __init__(self, items: list[Any], distribution: list[Union[float, int]]) -> None:
        super().__init__()
        self.distribution = np.array(distribution, dtype=np.float32)
        self.normalized = self.distribution / np.sum(self.distribution)
        self.items = items

    def generate(self) -> Any:
        return self.rng.choice(self.items, p=self.normalized)


class Uniform(Distribution):
    def __init__(
        self, low: float, high: float, itype: str = "float", precision: int = 2
    ) -> None:
        super().__init__()
        self.low = low
        self.high = high
        self.itype = itype
        self.precision = precision

    def generate(self) -> Union[float, int]:
        if self.itype == "float":
            d = self.rng.uniform(self.low, self.high)
            return round(float(d), self.precision)
        else:
            return self.rng.integers(self.low, self.high)


class Normal(Distribution):
    def __init__(self, mean: float = 0, stddev: float = 1.0) -> None:
        super().__init__()
        self.mean = mean
        self.stddev = stddev

    def generate(self) -> float:
        return self.rng.normal(loc=self.mean, scale=self.stddev)
