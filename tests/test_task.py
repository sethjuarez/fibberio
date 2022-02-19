from fibberio import Task
from pathlib import Path

BASE_PATH = str(Path(__file__).absolute().parent)


def test_simple():
    f = f'{BASE_PATH}/data/simple.json'
    task = Task(f)
    assert task.files
    assert task.features
