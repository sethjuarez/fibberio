import abc
import numpy as np
from time import time
from .range import Range, RangeParser
from typing import Any, List, Tuple, Union
from .source import PandasSource
from .helpers import Item

parser = RangeParser()


class Distribution(metaclass=abc.ABCMeta):
    def __init__(self):
        self.id = ""
        self.discrete = False
        self._conditional: Distribution = None

    def generate(self, val=None) -> list[Tuple[str, Any]]:
        val = [(self.id, self.sample())]
        return val if self.conditional is None else val + self.conditional.generate(val)

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

    def sample(self) -> Any:
        pass

    def generate(self, val=None) -> list[Tuple[str, Any]]:
        if len(val) > 1:
            raise Exception(f"{val} too complex to conditionally process")

        for i in range(len(self.conditionals)):
            if self.conditionals[i].check(val[0][1]):
                return self.conditionals[i].generate(val[0][1])

        raise IndexError(f'could not marginal "{val}" in "{self.id}" conditional')


class Source(Distribution):
    def __init__(self, id: str, target: Union[str, List[str]]):
        super().__init__()
        self.discrete = True
        self.target = target if type(target) == list else [s.strip() for s in target.split(",")]
        self.src_id = id
        self.source: PandasSource = None

    def sample(self):
        return self.source.sample()

    def generate(self):
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
