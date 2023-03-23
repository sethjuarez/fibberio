import pytest
import pandas as pd
from pathlib import Path
from fibberio import Task

BASE_PATH = str(Path(__file__).absolute().parent.as_posix())


@pytest.mark.parametrize("taskfile", ["programmers.json", "storesales.json", "simple_gbm.json"])
def test_task_load(taskfile: str):
    file = f"{BASE_PATH}/data/{taskfile}"
    task = Task(file)
    assert task is not None


@pytest.mark.parametrize("taskfile", ["programmers.json", "storesales.json", "simple_gbm.json"])
def test_task_run(taskfile: str):
    file = f"{BASE_PATH}/data/{taskfile}"
    task = Task(file)
    df: pd.DataFrame = task.generate(1000)
    assert df.count()[0] == 1000
