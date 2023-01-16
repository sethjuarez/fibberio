import sys
import json
from typing import Any, Dict, Tuple
import pandas as pd
from pathlib import Path
from .source import PandasSource
from .distribution import Distribution, Source


class TaskF:
    def __init__(self) -> None:
        pass


class Task:
    def __init__(self, f: str) -> None:
        self.task = Path(f).absolute().resolve()

        if not self.task.exists():
            raise FileNotFoundError(f"{str(self.task)} does not exist")

        # load description
        p = json.loads(self.task.read_text())

        # load sources
        self.files: dict[str, PandasSource] = {}
        self._load_sources(p["sources"])

        # load features
        features = p["features"]
        self.features = [self._load_feature(id, features[id]) for id in features]

    @staticmethod
    def build(item: Dict[str, Any]) -> Tuple[str, Any]:
        # item = json.loads(data)

        # retrieve id
        id = item.pop("id")

        # class and args
        clsname = next(iter(item))
        kwargs = item[clsname]
        cl = getattr(sys.modules["fibberio"], clsname.capitalize())
        cls = cl(**kwargs)
        return id, cls
    
    @staticmethod
    def path(f: str) -> Path:
        return Path(f).absolute().resolve()
        
    def _load_sources(self, sources: dict) -> None:
        for key in sources.keys():
            if key in self.files:
                raise KeyError(f"{key} already exists")

            item = sources[key]
            fp = Path(item.pop("path"))
            if not fp.is_absolute():
                fp = self.task.parent.joinpath(fp)

            fp = fp.absolute().resolve()
            if not fp.exists():
                raise FileNotFoundError(f'source "{key}" file {fp} does not exist')

            call: str = next(iter(item))
            self.files[key] = PandasSource(path=fp, call=call, argsv=item[call])

    def _load_feature(self, id: str, feature: dict) -> Distribution:
        distribution: Distribution = Distribution.build(id, feature)

        if type(distribution) == Source:
            if distribution.src_id not in self.files:
                raise KeyError(f"{distribution.src_id} source reference does not exist")
            distribution.source = self.files[distribution.src_id]

        return distribution

    def generate(self, count: int) -> pd.DataFrame:
        d = [
            {k: v for distr in self.features for k, v in distr.generate()}
            for _ in range(count)
        ]
        return pd.DataFrame(d)
