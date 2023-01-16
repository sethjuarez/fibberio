import json
from pathlib import Path
from fibberio import Task, Discrete, Uniform, Normal

BASE_PATH = str(Path(__file__).absolute().parent.as_posix())


def test_discrete_load():
    item = (
        "{"
        '    "id": "location",'
        '    "discrete": {'
        '        "North America": 500,'
        '        "South America": 200,'
        '        "Europe": 200,'
        '        "Africa": 100,'
        '        "Asia": 100,'
        '        "Oceania": 100,'
        '        "Antartica": 1'
        '    }'
        '}'
    )
    id, distribution = Task.build(json.loads(item))
    assert id == "location"
    assert isinstance(distribution, Discrete)


def test_uniform_load():
    item = (
        "{"
        '    "id": "toodles",'
        '    "uniform": {'
        '      "low": 5,'
        '      "high": 10,'
        '      "precision": 0'
        '    }'
        '}'
    )
    id, distribution = Task.build(json.loads(item))
    assert id == "toodles"
    assert isinstance(distribution, Uniform)


def test_normal_load():
    item = (
        "{"
        '    "id": "age",'
        '    "normal": {'
        '      "mean": 36,'
        '      "stddev": 5,'
        '      "precision": 0'
        '    }'
        '}'
    )
    id, distribution = Task.build(json.loads(item))
    assert id == "age"
    assert isinstance(distribution, Normal)
