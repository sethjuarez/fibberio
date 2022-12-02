from fibberio import Task
from pathlib import Path
import pandas as pd
import json


BASE_PATH = str(Path(__file__).absolute().parent)


def test_simple_cond():
    f = f"{BASE_PATH}/data/conditional.json"
    task = Task(f)
    df: pd.DataFrame = task.generate(1000)
    assert df.count().age == 1000


def test_programmers():
    f = f"{BASE_PATH}/data/programmers.json"
    task = Task(f)
    df: pd.DataFrame = task.generate(1000)
    assert df.count().age == 1000


class TaskDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode(self, s, _w=json.decoder.WHITESPACE.match):
        print("decode", s)
        return super().decode(s, _w)

    def encode(self, o):
        print("encode", o)
        return super().encode(o)


class TaskEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def encode(self, o):
        print("encode", o)
        return super().encode(o)


def test_random():
    f = Path(f"{BASE_PATH}/data/conditional.json").absolute().resolve()
    print("\n=====================")
    json.loads(f.read_text(), object_pairs_hook=print)

