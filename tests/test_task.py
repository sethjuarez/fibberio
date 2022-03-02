from fibberio import Task
from pathlib import Path
import pandas as pd

BASE_PATH = str(Path(__file__).absolute().parent)


def test_simple():
    f = f"{BASE_PATH}/data/simple.json"
    task = Task(f)
    assert task.files
    assert task.features


def test_simple_headers():
    f = f"{BASE_PATH}/data/simple.json"
    task = Task(f)
    actual = ["FirstName", "LastName", "Age", "Farther", "TabsVSpaces"]
    assert task.headers() == actual


def test_generation():
    f = f"{BASE_PATH}/data/simple.json"
    task = Task(f)
    df: pd.DataFrame = task.generate(1000)
    assert df.count().Age == 1000


def test_simple_cond():
    f = f"{BASE_PATH}/data/simple.json"
    task = Task(f)
    df: pd.DataFrame = task.generate(1000)
    assert df.count().Age == 1000
