import abc
import numpy as np
from time import time
from .source import PandasSource
from typing import Any, Tuple


class Distribution(metaclass=abc.ABCMeta):
    def __init__(self):
        self.id = ""

    @abc.abstractclassmethod
    def generate(self, val=None) -> list[Tuple[str, Any]]:
        pass

    def conditional(self, desc: dict) -> None:
        pass


class Source(Distribution):
    def __init__(self, id: str, target: str):
        super().__init__()
        self.target = [s.strip() for s in target.split(",")]
        self.src_id = id
        self.source: PandasSource = None

    def generate(self, val=None) -> list[Tuple[str, Any]]:
        r = self.source.sample()
        return [(item, r[item].values[0]) for item in self.target]


class Discrete(Distribution):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.rng = np.random.default_rng(int(time() * 1000))
        self.items = [k for k in kwargs.keys()]
        self.distribution = np.array(
            [kwargs[i] for i in kwargs.keys()], dtype=np.float32
        )
        self.normalized = self.distribution / np.sum(self.distribution)

    def generate(self) -> list[Tuple[str, Any]]:
        return [(self.id, self.rng.choice(self.items, p=self.normalized))]


class Uniform(Distribution):
    def __init__(
        self, low: float, high: float, itype: str = "float", precision: int = 2
    ) -> None:
        super().__init__()
        self.rng = np.random.default_rng(int(time() * 1000))
        self.low = low
        self.high = high
        self.itype = itype
        self.precision = precision

    def generate(self) -> list[Tuple[str, Any]]:
        if self.itype == "float":
            d = self.rng.uniform(self.low, self.high)
            return [(self.id, round(float(d), self.precision))]
        else:
            return [(self.id, self.rng.integers(self.low, self.high))]


class Normal(Distribution):
    def __init__(self, mean: float = 0, stddev: float = 1.0) -> None:
        super().__init__()
        self.rng = np.random.default_rng(int(time() * 1000))
        self.mean = mean
        self.stddev = stddev

    def generate(self) -> float:
        return [(self.id, self.rng.normal(loc=self.mean, scale=self.stddev))]
