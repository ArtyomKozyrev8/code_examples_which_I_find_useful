import types
from itertools import accumulate


class SomeMathBase:
    def __init__(self, /, *args):
        self.args = args

    def sum(self):
        return sum(self.args)


def mul(self):
    *_, last = accumulate(self.args, lambda a, b: a * b, initial=1)
    return last


def minus(self):
    *_, last = accumulate(self.args, lambda a, b: a - b)
    return last


namespace_dict = {
    "mul": mul,
    "minus": minus,
}

SomeMathExtend = types.new_class(
    name="SomeMathExtend",
    bases=(SomeMathBase, ),
    exec_body=lambda ns: ns.update(namespace_dict),
)


if __name__ == '__main__':
    assert SomeMathExtend(1, 2, 3, 4, 5, 6, 7, 8, 9).sum() == 45
    assert SomeMathExtend(1, 2, 3, 4, 5).mul() == 120
    assert SomeMathExtend(1, 2, 3, 4, 5).minus() == -13
    assert isinstance(SomeMathExtend(1), SomeMathBase) is True
