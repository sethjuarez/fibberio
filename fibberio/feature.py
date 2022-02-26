from .source import PandasSource
from .distribution import Distribution


class Feature:
    def __init__(self) -> None:
        self.target: list[str] = []
        self.source: PandasSource = None
        self.distribution: Distribution = None

    def generate(self) -> list:
        if self.source is not None:
            return [f for f in self.source.generate(self.target)]
        else:
            return [self.distribution.generate() for _ in self.target]
