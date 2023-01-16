import json
from pathlib import Path
from fibberio import Task, Pandas

BASE_PATH = str(Path(__file__).absolute().parent.as_posix())


def test_pandas_source():
    item = (
        "{"
        '    "id": "names",'
        '    "pandas": {'
        f'       "path": "{BASE_PATH}/data/full_names.csv",'
        '        "read_csv": {'
        '            "encoding": "unicode_escape",'
        '            "engine": "python"'
        '        }'
        '    }'
        '}'
    )
    id, source = Task.build(json.loads(item))
    assert id == "names"
    assert isinstance(source, Pandas)
