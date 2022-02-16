import pytest
from fibberio import SourceParser


@pytest.fixture
def parser():
    return SourceParser()


def test_source_parse(parser):
    o = parser.parse("expr((100000, 200000], float(2))")
    print(o)
