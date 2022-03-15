from fibberio import Task
from pathlib import Path
import pandas as pd


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