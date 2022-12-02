
def f(a, *args, **kwargs):
    print(args)
    print(kwargs)


def test_basic_thing():
    f('a', 1, 2, 3, 4, b=2, c=3)
    assert 1 == 1
