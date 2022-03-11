import pandas as pd
from pathlib import Path


class PandasSource():
    def __init__(self, path: Path, call: str, argsv: dict) -> None:
        self.path = path
        cl = getattr(pd, call)
        if len(argsv) > 0:
            self.df: pd.DataFrame = cl(path, **argsv)
        else:
            self.df: pd.DataFrame = cl(path)

    def sample(self) -> pd.DataFrame:
        return self.df.sample()
