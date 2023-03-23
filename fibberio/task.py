import json
from typing import Any
import pandas as pd
from pathlib import Path
from .distribution import Distribution, Source
from .helpers import Item


class Task:
    def __init__(self, file: str = None) -> None:
        self.sources: dict[str, Source] = {}
        self.features: dict[str, Distribution] = {}
        if file is not None:
            self.load(file)

    def load(self, file: str) -> None:
        self.file = Path(file).absolute().resolve()

        if not self.file.exists():
            raise FileNotFoundError(f"{str(self.file)} does not exist")

        # for relative file pathing
        path = Path(file).absolute().parent.resolve()

        # load description
        task = json.loads(self.file.read_text())

        # load sources - add path for rel paths
        sources = [Item.build(s, path) for s in task["sources"]]
        self.sources = {id: o for id, o in sources}

        # load features
        features = [Item.build(s) for s in task["features"]]
        self.features = {id: o for id, o in features}

        # hidrate "source" features
        for k in self.features.keys():
            # set up referential integrity
            self.features[k].id = k
            if type(self.features[k]) == Source:
                if self.features[k].src in self.sources:
                    self.features[k].source = self.sources[self.features[k].src]
                else:
                    raise ValueError(f"Source {self.features[k].src} not found in data sources")

    def sample(self) -> dict[str, Any]:
        d = {}
        for _, feature in self.features.items():
            # generate new data while passing in existing data
            d = {**d, **{k: v for k, v in feature.generate(**d)}}
        return d

    def generate(self, count: int) -> pd.DataFrame:
        return pd.DataFrame([self.sample() for _ in range(count)])
