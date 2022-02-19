from .source import Source
from .distribution import Distribution


class Feature:
    def __init__(self) -> None:
        self._target: list[str] = []
        self._source: Source = None
        self._distribution: Distribution = None

    def _validate(self) -> bool:
        return True

    @property
    def target(self) -> list[str]:
        return self._target

    @target.setter
    def target(self, target: list[str]) -> None:
        self._target = target
        self._validate()

    @property
    def source(self) -> Source:
        return self._source

    @source.setter
    def source(self, source: Source) -> None:
        self._source = source
        self._validate()

    @property
    def distribution(self) -> Distribution:
        return self._distribution

    @distribution.setter
    def distribution(self, distribution: Distribution) -> None:
        self._distribution = distribution
        self._validate()
