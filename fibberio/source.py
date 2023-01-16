import abc
import pandas as pd
from typing import Any


class DataSource(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        pass

    @abc.abstractclassmethod
    def load(self) -> Any:
        pass

    @abc.abstractclassmethod
    def sample(self) -> Any:
        pass


class PandasSource:
    pass


class Pandas(DataSource):
    def __init__(self, **kwargs) -> None:
        # retrieve path
        path = kwargs.pop("path")

        # retrieve pandas call
        call = next(iter(kwargs))
        kw = kwargs[call]
        cl = getattr(pd, call)
        if len(kw) > 0:
            self.df: pd.DataFrame = cl(path, **kw)
        else:
            self.df: pd.DataFrame = cl(path)

    def load(self):
        pass

    def sample(self, *args):
        r = self.df.sample()
        return [r[item].values[0] for item in args]
