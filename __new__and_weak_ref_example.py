from weakref import WeakValueDictionary


class UniqueStrings:
    """
    Creates class instances with only unique string_name.

    Otherwise, the existent instance is returned.
    """
    _instances = WeakValueDictionary()

    def __new__(cls, string_name: str) -> "UniqueStrings":
        if self := cls._instances.get(string_name, None):
            return self

        self = super().__new__(cls)  # use parent class to prevent infinite recursion
        self.string_name = string_name
        cls._instances[string_name] = self  # value is reference to instance

        return self

    def __init__(self, string_name: str) -> None:
        pass

    def __repr__(self):
        return f"UniqueStrings({self.string_name})"


if __name__ == '__main__':
    x1, x2, x3 = UniqueStrings("x1"), UniqueStrings("x1"), UniqueStrings("x3")
    assert x1 is x2
    assert not (x3 is x1 and x3 is x2)
    print(list(UniqueStrings._instances.items()))
    del x3
    print(list(UniqueStrings._instances.items()))
    x4 = UniqueStrings("x3")
    print(x4)
    print(list(UniqueStrings._instances.items()))
