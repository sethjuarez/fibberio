import abc
import numpy as np
from typing import Union


class Distribution(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def parse(expr: str) -> bool:
        pass

    @abc.abstractclassmethod
    def generate(self) -> float:
        pass


class DiscreteDistribution(Distribution):
    def __init__(self, distribution: list[Union[float, int]] = [0]) -> None:
        self.distribution = np.array(distribution, dtype=np.float16)
        self.normalized = self.distribution / np.sum(self.distribution)

    def parse(expr: str) -> bool:
        pass

    def generate(self) -> float:
        pass


class UniformDistribution(Distribution):
    def __init__(self, ) -> None:
        pass

    def parse(expr: str) -> bool:
        pass

    def generate(self) -> float:
        pass


class NormalDistribution(Distribution):
    def __init__(self, mean=0.5, stddev=.1) -> None:
        self.mean = mean
        self.stddev = stddev

    def parse(expr: str) -> bool:
        pass

    def generate(self) -> float:
        pass