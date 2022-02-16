import pytest
from fibberio import Parser


@pytest.fixture
def grammar():
    return Parser()


def test_source_parse():
    p = Parser()
    o = p.parse("expr([12, 59), float)")
    print(o)
