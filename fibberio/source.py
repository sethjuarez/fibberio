import abc
import pandas as pd
from pathlib import Path


class Source(metaclass=abc.ABCMeta):
    pass


class PandasSource(Source):
    def __init__(self, path: Path, call: str, argsv: dict) -> None:
        self.path = path
        cl = getattr(pd, call)
        if len(argsv) > 0:
            self.df: pd.DataFrame = cl(path, **argsv)
        else:
            self.df: pd.DataFrame = cl(path)

    def generate(self, features: list[str]) -> list:
        r = self.df.sample()
        return [r[item].values[0] for item in features]
