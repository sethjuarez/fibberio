import pandas as pd
from pathlib import Path
from fibberio import Task

BASE_PATH = str(Path(__file__).absolute().parent.as_posix())


def test_task_load():
    file = f"{BASE_PATH}/data/programmers.json"
    task = Task(file)
    assert task is not None


def test_programmers():
    f = f"{BASE_PATH}/data/programmers.json"
    task = Task(f)
    df: pd.DataFrame = task.generate(1000)
    assert df.count().age == 1000
