import json
import pandas as pd
from pathlib import Path
from .source import PandasSource
from .distribution import Distribution, Source


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

        # load modules
        self.module = __import__(self.__module__)

        # load features
        features = p["features"]
        self.features = [self._load_feature(id, features[id]) for id in features]

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
        # check conditionals
        cond = feature.pop("conditional") if "conditional" in feature else None

        clsname = next(iter(feature))
        kwargs = feature[clsname]

        cl = getattr(self.module, clsname.capitalize())
        distribution: Distribution = None
        if len(kwargs) > 0:
            distribution = cl(**kwargs)
        else:
            distribution = cl()

        distribution.id = id
        if cond is not None:
            distribution.conditional(cond)

        if type(distribution) == Source:
            if distribution.src_id not in self.files:
                raise KeyError(f"{distribution.src_id} source reference does not exist")
            distribution.source = self.files[distribution.src_id]

        return distribution

    def generate(self, count: int) -> pd.DataFrame:
        d = [
            {t[0]: t[1] for distr in self.features for t in distr.generate()}
            for _ in range(count)
        ]
        return pd.DataFrame(d)
