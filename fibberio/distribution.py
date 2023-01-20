import abc
import numpy as np
from time import time
from .helpers import Item
from .source import DataSource
from .range import Range, RangeParser
from typing import Any, List, Tuple, Union

parser = RangeParser()


class Distribution(metaclass=abc.ABCMeta):
    def __init__(self):
        self._id = ""
        self.discrete = False
        self._conditional: Distribution = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def generate(self, **kwargs) -> list[Tuple[str, Any]]:
        return [(self.id, self.sample())]

    @abc.abstractclassmethod
    def sample(self) -> Any:
        pass


class Condition:
    def __init__(self, marginal: Union[Range, int, float, str], posterior: Distribution):
        self.marginal = marginal
        self.posterior = posterior

    def check(self, val):
        if type(self.marginal) == Range:
            return self.marginal.check(val)
        else:
            return self.marginal == val or self.marginal == "*"

    def generate(self, val) -> list[Tuple[str, Any]]:
        if self.check(val):
            return self.posterior.generate()
        else:
            raise ValueError(f'marginal "{self.marginal}" does not match "{val}"')


class Conditional(Distribution):
    def __init__(self, marginal: str, posterior: Union[List[Condition], List[dict]]):
        super().__init__()
        self.marginal = marginal
        self.posterior = []
        isRange = False
        for item in posterior:
            if type(item) == dict:
                v = item.pop("value")
                if v.find("[") > -1 or v.find("(") > -1:
                    v = parser.parse(v)
                    isRange = True

                elif isRange and v == "*":
                    v = parser.parse(v)

                # id doesn't matter here
                _, distr = Item.build(item)
                self.posterior.append(Condition(v, distr))
            else:
                self.posterior.append(item)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        for item in self.posterior:
            item.posterior.id = value

    def sample(self) -> Any:
        pass

    def generate(self, **kwargs) -> list[Tuple[str, Any]]:
        if self.marginal not in kwargs:
            raise KeyError(f'could not find marginal "{self.marginal}" in generated data')

        val = kwargs[self.marginal]

        for i in range(len(self.posterior)):
            if self.posterior[i].check(val):
                return self.posterior[i].generate(val)

        raise IndexError(f'could not find marginal "{val}" in "{self.id}" conditional')


class Source(Distribution):
    def __init__(self, id: str, target: Union[str, List[str]]):
        super().__init__()
        self.target = target if type(target) == list else [s.strip() for s in target.split(",")]
        self.src = id
        self.source: DataSource = None

    def sample(self):
        return self.source.sample()

    def generate(self, **kwargs) -> list[Tuple[str, Any]]:
        r = self.sample()
        if len(self.target) == 1:
            return [(self.id, r[self.target[0]].values[0])]
        else:
            return [(item, r[item].values[0]) for item in self.target]


class Discrete(Distribution):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.discrete = True
        self.rng = np.random.default_rng(int(time() * 1000))
        self.items = [k for k in kwargs.keys()]
        self.distribution = np.array([kwargs[i] for i in kwargs.keys()], dtype=np.float32)
        self.normalized = self.distribution / np.sum(self.distribution)

    def sample(self) -> Any:
        return self.rng.choice(self.items, p=self.normalized)


class Uniform(Distribution):
    def __init__(self, low: float, high: float, itype: str = "float", precision: int = 2) -> None:
        super().__init__()
        self.rng = np.random.default_rng(int(time() * 1000))
        self.low = low
        self.high = high
        self.itype = itype
        self.precision = precision

    def sample(self) -> Any:
        if self.itype == "float":
            d = self.rng.uniform(self.low, self.high)
            return round(float(d), self.precision)
        else:
            return self.rng.integers(self.low, self.high)


class Normal(Distribution):
    def __init__(self, mean: float = 0, stddev: float = 1.0, precision: int = 2) -> None:
        super().__init__()
        self.rng = np.random.default_rng(int(time() * 1000))
        self.mean = mean
        self.stddev = stddev
        self.precision = precision

    def sample(self) -> Any:
        d = self.rng.normal(loc=self.mean, scale=self.stddev)
        return round(d, self.precision)
