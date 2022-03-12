import sys
import abc
import numpy as np
from time import time
from .range import Range, RangeParser
from typing import Any, Tuple
from .source import PandasSource

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

    @staticmethod
    def build(id: str, feature: dict):
        # check conditional
        cond = feature.pop("conditional") if "conditional" in feature else None

        # class and args
        clsname = next(iter(feature))
        kwargs = feature[clsname]

        # create
        cl = getattr(sys.modules["fibberio"], clsname.capitalize())
        distribution: Distribution = cl.create(kwargs)
        distribution.id = id

        # create conditional
        if cond is not None:
            distribution.conditional = cond

        return distribution

    @property
    def conditional(self):
        return self._conditional

    @conditional.setter
    def conditional(self, desc) -> None:
        # nothing to do
        if desc is None:
            return
        elif type(desc) == Distribution:
            self._conditional = desc
        else:
            # pull conditional off if exists
            cond = desc.pop("conditional") if "conditional" in desc else None
            key = next(iter(desc))
            val: dict = desc[key]
            if self.discrete:
                self._conditional = Conditional()
                self._conditional.values = [k for k in val.keys()]
            else:
                self._conditional = RangeConditional()
                self._conditional.ranges = [parser.parse(k) for k in val.keys()]

            self._conditional.id = key
            self._conditional.distributions = [
                Distribution.build(key, v) for v in val.values()
            ]

            # only discrete if all d's are discrete
            self._conditional.discrete = all(
                d.discrete for d in self._conditional.distributions
            )

            self._conditional.conditional = cond

    @classmethod
    def create(cls, kwargs):
        if len(kwargs) > 0:
            return cls(**kwargs)
        else:
            return cls


class Conditional(Distribution):
    def __init__(self):
        super().__init__()
        self.values: list[Any] = []
        self.distributions: list[Distribution] = []

    def check(self, idx, val) -> bool:
        return self.values[idx] == val or self.values[idx] == "*"

    def sample(self) -> Any:
        pass

    def generate(self, val=None) -> list[Tuple[str, Any]]:
        if len(val) > 1:
            raise Exception(f"{val} too complex to conditionally process")

        for i in range(len(self.distributions)):
            if self.check(i, val[0][1]):
                g = self.distributions[i].generate()
                if self.conditional is not None:
                    return g + self.conditional.generate(g)
                else:
                    return g

        raise IndexError(f"could not match {val} in conditional")


class RangeConditional(Conditional):
    def __init__(self):
        super().__init__()
        self.ranges: list[Range] = []
        self.distributions: list[Distribution] = []

    def check(self, idx, val) -> bool:
        return self.ranges[idx].check(val)


class Source(Distribution):
    def __init__(self, id: str, target: str):
        super().__init__()
        self.discrete = True
        self.target = [s.strip() for s in target.split(",")]
        self.src_id = id
        self.source: PandasSource = None

    def sample(self):
        return self.source.sample()

    def generate(self):
        r = self.sample()
        return [(item, r[item].values[0]) for item in self.target]


class Discrete(Distribution):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.discrete = True
        self.rng = np.random.default_rng(int(time() * 1000))
        self.items = [k for k in kwargs.keys()]
        self.distribution = np.array(
            [kwargs[i] for i in kwargs.keys()], dtype=np.float32
        )
        self.normalized = self.distribution / np.sum(self.distribution)

    def sample(self) -> Any:
        return self.rng.choice(self.items, p=self.normalized)


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

    def sample(self) -> Any:
        if self.itype == "float":
            d = self.rng.uniform(self.low, self.high)
            return round(float(d), self.precision)
        else:
            return self.rng.integers(self.low, self.high)


class Normal(Distribution):
    def __init__(
        self, mean: float = 0, stddev: float = 1.0, precision: int = 2
    ) -> None:
        super().__init__()
        self.rng = np.random.default_rng(int(time() * 1000))
        self.mean = mean
        self.stddev = stddev
        self.precision = precision

    def sample(self) -> Any:
        d = self.rng.normal(loc=self.mean, scale=self.stddev)
        return round(d, self.precision)
