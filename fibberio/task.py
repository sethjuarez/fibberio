import json
from pathlib import Path
from .feature import Feature
from typing import Dict, List
from .parser import ItemParser
from .distribution import DiscreteDistribution, Distribution
from .source import DiscreteSource, FileSource, RangeSource, Source


class Task:
    def __init__(self, desc: str) -> None:
        self.task = Path(desc).absolute().resolve()
        # load modules
        self.module = __import__(self.__module__)

        if not self.task.exists():
            raise FileNotFoundError(f"{str(self.task)} does not exist")

        p = json.loads(self.task.read_text())

        # load inline file sources
        self.files: Dict[str, FileSource] = {}
        self._load_sources(p["sources"])

        # load features
        self.features: List[Source] = []
        self.parser = ItemParser()
        self._load_features(p["features"])

    def _load_sources(self, sources) -> None:
        for item in sources:
            if item["id"] in self.files:
                raise KeyError(f'{item["id"]} already exists')

            fs = FileSource()
            fs.reference = item["id"]
            fp = Path(item["data"])
            if not fp.is_absolute():
                fp = self.task.parent.joinpath(fp)

            fs.path = fp.absolute().resolve()
            if not fs.path.exists():
                raise FileNotFoundError(
                    f'source "{item["id"]}" file {item["data"]} does not exist'
                )
            self.files[item["id"]] = fs

    def _load_features(self, features) -> None:
        for item in features:
            f = Feature()
            f.target = item["feature"].split(",")

            # source
            f.source = self._load_source(item["source"])

            # distribution
            f.distribution = self._load_distribution(item["distribution"])

            self.features.append(f)

    def _load_source(self, source) -> Source:
        if type(source) == list:
            # discrete source
            return DiscreteSource(source)
        else:
            parsed = self.parser.parse(source)
            if parsed.name == "__range":
                return RangeSource(
                    start_open=parsed.start_open,
                    start=parsed.start,
                    end=parsed.end,
                    end_open=parsed.end_open,
                    val_type=parsed.val_type,
                    precision=parsed.precision,
                )
            else:
                if parsed.name not in self.files:
                    raise KeyError(f"{parsed.name} source reference does not exist")
                return self.files[parsed.name]

    def _load_distribution(self, distribution) -> Distribution:
        if type(distribution) == list:
            return DiscreteDistribution(distribution)
        else:
            parsed = self.parser.parse(distribution)
            clsname = f'{parsed.name.capitalize()}Distribution'
            cl = getattr(self.module, clsname)
            if len(parsed.argsv) > 0:
                return cl(**parsed.argsv)
            else:
                return cl()

    def process(self) -> None:
        x = self.task
        return x
