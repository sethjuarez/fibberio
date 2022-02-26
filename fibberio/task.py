import json
import pandas as pd
from pathlib import Path
from .feature import Feature
from .source import PandasSource
from .distribution import Distribution


class Task:
    def __init__(self, desc: str) -> None:
        self.task = Path(desc).absolute().resolve()
        # load modules
        self.module = __import__(self.__module__)

        if not self.task.exists():
            raise FileNotFoundError(f"{str(self.task)} does not exist")

        p = json.loads(self.task.read_text())

        # load sources
        self.files: dict[str, PandasSource] = {}
        self._load_sources(p["sources"])

        # load features
        self.features: list[Feature] = []
        self._load_features(p["features"])

    def _load_sources(self, sources) -> None:
        for item in sources:
            if item["id"] in self.files:
                raise KeyError(f'{item["id"]} already exists')

            ref = item.pop("id")
            fp = Path(item.pop("path"))
            if not fp.is_absolute():
                fp = self.task.parent.joinpath(fp)

            fp = fp.absolute().resolve()
            if not fp.exists():
                raise FileNotFoundError(f'source "{ref}" file {fp} does not exist')

            call: str = next(iter(item))
            self.files[ref] = PandasSource(path=fp, call=call, argsv=item[call])

    def _load_features(self, features) -> None:
        for item in features:
            f = Feature()
            f.target = [f.strip() for f in item["target"].split(",")]

            # inline source ref
            if "source" in item:
                if item["source"] not in self.files:
                    raise KeyError(f"{item['source']} source reference does not exist")
                f.source = self.files[item["source"]]

            # distribution
            if "distribution" in item:
                f.distribution = self._load_distribution(item["distribution"])

            self.features.append(f)

    def _load_distribution(self, d: dict) -> Distribution:
        if len(d.keys()) != 1:
            raise KeyError(f"incorrect items in {d}")

        clsname: str = next(iter(d))
        argsv = d[clsname]

        cl = getattr(self.module, clsname.capitalize())
        if len(argsv) > 0:
            return cl(**argsv)
        else:
            return cl()

    def headers(self) -> list:
        return [fi for f in self.features for fi in f.target]

    def generate_row(self) -> list:
        return [v for f in self.features for v in f.generate()]

    def generate(self, count: int) -> pd.DataFrame:
        return pd.DataFrame(
            [self.generate_row() for _ in range(count)],
            columns=[f for f in self.headers()],
        )
