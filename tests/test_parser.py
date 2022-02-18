import pytest
from fibberio import ItemParser, ParseResult


@pytest.mark.parametrize(
    "source, actual",
    [
        ("namedref", ParseResult(name="namedref")),
        (
            "(100000, 200000] -> float(2)",
            ParseResult(
                start_open=True,
                end_open=False,
                precision=2,
                start=100000,
                end=200000,
                val_type="float",
            ),
        ),
        (
            "[52, 102) -> int",
            ParseResult(
                start_open=False, end_open=True, start=52, end=102, val_type="int"
            ),
        ),
        (
            "(1.1, 5.1]",
            ParseResult(
                start_open=True, end_open=False, start=1.1, end=5.1, val_type="float"
            ),
        ),
        (
            "(5, 10)",
            ParseResult(
                start_open=True, end_open=True, start=5, end=10, val_type="int"
            ),
        ),
        (
            "*",
            ParseResult(floor=True, ceil=True),
        ),
        (
            "[*, 10000)",
            ParseResult(
                start_open=False, end_open=True, end=10000, floor=True, val_type="int"
            ),
        ),
        (
            "[20, *)",
            ParseResult(
                start_open=False, end_open=True, start=20, ceil=True, val_type="int"
            ),
        ),
        (
            "[1.1, *)",
            ParseResult(
                start_open=False, end_open=True, start=1.1, ceil=True, val_type="float"
            ),
        ),
        (
            "uniform(mean=1, std=2)",
            ParseResult(name="uniform", argsv={'mean': 1, 'std': 2}),
        ),
        (
            "newthing()",
            ParseResult(name="newthing"),
        ),
        (
            "rtf(sd=sd23, gfd=12)",
            ParseResult(name="rtf", argsv={'sd': 'sd23', 'gfd': 12}),
        ),
        (
            "zee(sd=1)",
            ParseResult(name="zee", argsv={'sd': 1}),
        ),
    ],
)
def test_parser(source: str, actual: ParseResult):
    p = ItemParser()
    parsed = p.parse(source)
    assert parsed.start_open == actual.start_open
    assert parsed.end_open == actual.end_open
    assert parsed.val_type == actual.val_type
    assert parsed.precision == actual.precision
    assert parsed.start == actual.start
    assert parsed.end == actual.end
    assert parsed.name == actual.name
    assert parsed.argsv == actual.argsv
