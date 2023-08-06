from fixed_list import FixedList


def test():
    x = FixedList(capacity=100)
    for i in range(99):
        assert len(x) == i
        x.append(i)
    assert len(x) == 99
    x.append(100)
    assert x[0] == 0
    x.append(101)
    assert len(x) == 100
    assert x[0] == 1
    assert x[-1] == 101
