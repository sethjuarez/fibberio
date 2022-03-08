# from doctest import UnexpectedException
# from .source import PandasSource
from .distribution import Distribution
from .range import Range


class Feature:
    def __init__(self, id: str) -> None:
        self.id = id
        self.distribution: Distribution = None

    def generate(self) -> list:
        return self.distribution.generate()


class Conditional(Feature):
    def __init__(self, id: str) -> None:
        self.__init__(id)
        self.conditionals: list[Range] = []
        self.distributions: list[Distribution] = []

    def generate(self, val) -> list:
        pass
