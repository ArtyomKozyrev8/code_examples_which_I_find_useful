class SlotX:
    """
    Check docs https://docs.python.org/3/reference/datamodel.html#slots
    Slots have some advantages, but have some drawbacks.
    Advantages: better speed and memory save.
    Disadvantages: 'difficult' inheritance, no __dict__, other.
    """
    __slots__ = ["a", "b"]

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def plus(self):
        return self.a + self.b

    def __repr__(self):
        return f"{type(self).__name__}({self.a, self.b})"


if __name__ == '__main__':
    item = SlotX(a=1, b=2)
    assert str(item) == "SlotX((1, 2))"
    assert item.plus() == 3
    # item.c = 10  # it will raise AttributeError: 'SlotX' object has no attribute 'c'
