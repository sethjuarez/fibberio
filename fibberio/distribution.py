import abc


class Distribution(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def parse(expr: str) -> bool:
        pass

    @abc.abstractclassmethod
    def generate(self) -> float:
        pass
