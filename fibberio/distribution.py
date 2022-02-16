import abc
from typing import Any


class Distribution(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def parse(expr: str) -> bool:
        pass

    @abc.abstractclassmethod
    def generate(self) -> Any:
        pass
