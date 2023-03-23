import json
from pathlib import Path
from fibberio import Discrete, Uniform, Normal, Source, Conditional, Item, GBM, Time

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
    id, distribution = Item.build(json.loads(item))
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
    id, distribution = Item.build(json.loads(item))
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
    id, distribution = Item.build(json.loads(item))
    assert id == "age"
    assert isinstance(distribution, Normal)


def test_gbm_load():
    item = (
        "{"
        '    "id": "timeseries",'
        '    "gbm": {'
        '      "period": 1,'
        '      "start": 100,'
        '      "drift": 0.01,'
        '      "volatility": 0.06,'
        '      "precision": 2'
        '    }'
        '}'
    )
    d = json.loads(item)
    id, distribution = Item.build(d)
    assert id == "timeseries"
    assert isinstance(distribution, GBM)


def test_time_load():
    item = (
        "{"
        '    "id": "date",'
        '    "time": {'
        '      "start": "2021-11-21",'
        '      "format": "%Y-%m-%d",'
        '      "days": 1'
        '    }'
        '}'
    )
    d = json.loads(item)
    id, distribution = Item.build(d)
    assert id == "date"
    assert isinstance(distribution, Time)


def test_source_load():
    item = (
        '{'
        '    "id": "last_name",'
        '    "source": {'
        '        "id": "names",'
        '        "target": "LastName"'
        '    }'
        '}'
    )
    data = json.loads(item)
    id, distribution = Item.build(data)
    assert id == "last_name"
    assert isinstance(distribution, Source)


def test_source_multi_list_load():
    item = (
        '{'
        '    "id": "last_name",'
        '    "source": {'
        '        "id": "names",'
        '        "target": ["LastName", "FirstName"]'
        '    }'
        '}'
    )
    data = json.loads(item)
    id, distribution = Item.build(data)
    assert id == "last_name"
    assert isinstance(distribution, Source)


def test_source_multi_str_load():
    item = (
        '{'
        '    "id": "last_name",'
        '    "source": {'
        '        "id": "names",'
        '        "target": "LastName, FirstName"'
        '    }'
        '}'
    )
    data = json.loads(item)
    id, distribution = Item.build(data)
    assert id == "last_name"
    assert isinstance(distribution, Source)


def test_conditional_load():
    item = (
        '{'
        '    "id": "yoe",'
        '    "conditional": {'
        '        "marginal": "style",'
        '        "posterior": ['
        '            {'
        '                "value": "tabs",'
        '                "uniform": {'
        '                    "low": 5,'
        '                    "high": 10,'
        '                    "precision": 0'
        '                }'
        '            },'
        '            {'
        '                "value": "spaces",'
        '                "normal": {'
        '                    "mean": 16,'
        '                    "stddev": 2,'
        '                    "precision": 0'
        '                }'
        '            }'
        '        ]'
        '    }'
        '}'
    )
    data = json.loads(item)
    id, distribution = Item.build(data)
    assert id == "yoe"
    assert isinstance(distribution, Conditional)


def test_conditional_range_load():
    item = (
        '{'
        '    "id": "yoe",'
        '    "conditional": {'
        '        "marginal": "style",'
        '        "posterior": ['
        '            {'
        '                "value": "[5, 10]",'
        '                "discrete": {'
        '                    "yes": 1,'
        '                    "no": 1'
        '                }'
        '            },'
        '            {'
        '                "value": "[11, 18]",'
        '                "discrete": {'
        '                    "yes": 23,'
        '                    "no": 2123'
        '                }'
        '            },'
        '            {'
        '                "value": "*",'
        '                "discrete": {'
        '                    "yes": 2232,'
        '                    "no": 10'
        '                }'
        '            }'
        '        ]'
        '    }'
        '}'
    )

    data = json.loads(item)
    id, distribution = Item.build(data)
    assert id == "yoe"
    assert isinstance(distribution, Conditional)
