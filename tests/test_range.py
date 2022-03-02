import pytest
from fibberio import RangeParser, Range


@pytest.mark.parametrize(
    "source, actual",
    [
        (
            "[52, 102) -> int",
            Range(start_open=False, end_open=True, start=52, end=102, val_type="int"),
        ),
        (
            "[52, 102) -> float(2)",
            Range(
                start_open=False,
                end_open=True,
                start=52,
                end=102,
                val_type="float",
                precision=2,
            ),
        ),
        (
            "[52, 102) -> float",
            Range(start_open=False, end_open=True, start=52, end=102, val_type="float"),
        ),
        (
            "(1.1, 5.1]",
            Range(
                start_open=True, end_open=False, start=1.1, end=5.1, val_type="float"
            ),
        ),
        (
            "(5, 10)",
            Range(start_open=True, end_open=True, start=5, end=10, val_type="int"),
        ),
        (
            "[*, 10000)",
            Range(
                start_open=False, end_open=True, end=10000, floor=True, val_type="int"
            ),
        ),
        (
            "[20, *)",
            Range(start_open=False, end_open=True, start=20, ceil=True, val_type="int"),
        ),
        (
            "[1.1, *)",
            Range(
                start_open=False, end_open=True, start=1.1, ceil=True, val_type="float"
            ),
        ),
        (
            "*",
            Range(ceil=True, floor=True),
        ),
        (
            "1",
            Range(start_open=False, end_open=False, start=1, end=1, val_type="int"),
        ),
        (
            "23.2",
            Range(
                start_open=False, end_open=False, start=23.2, end=23.2, val_type="float"
            ),
        ),
    ],
)
def test_parser(source: str, actual: Range):
    p = RangeParser()
    parsed = p.parse(source)
    assert parsed.start_open == actual.start_open
    assert parsed.end_open == actual.end_open
    assert parsed.precision == actual.precision
    assert parsed.start == actual.start
    assert parsed.end == actual.end
    assert parsed.val_type == actual.val_type
    assert parsed.floor == actual.floor
    assert parsed.ceil == actual.ceil


@pytest.mark.parametrize(
    "source, test, val",
    [
        ("[52, 102) -> int", 52, True),
        ("[52, 102) -> int", 102, False),
        ("[52, 102) -> float(2)", 52.1, True),
        ("[52, 102) -> float(2)", 102, False),
        ("[52, 102) -> float(2)", 101.99999, False),
        ("[52, 102) -> float(2)", 101.91, True),
        ("[52, 102) -> float", 102, False),
        ("(1.1, 5.1]", 1.1, False),
        ("(5, 10)", 7, True),
        ("[*, 10000)", -1000, True),
        ("[*, 10000)", 10000, False),
        ("[20, *)", 1000000, True),
        ("[20, *)", 19, False),
        ("[1.1, *)", 20000, True),
        ("*", 42, True),
        ("1", 1, True),
        ("1", 0.9999, False),
        ("1", 1.11, True),
        ("23.2", 23.2, True),
        ("23.2", 23.1, False),
    ],
)
def test_range(source: str, test: float, val):
    p = RangeParser()
    r = p.parse(source)
    assert r.check(test) == val
