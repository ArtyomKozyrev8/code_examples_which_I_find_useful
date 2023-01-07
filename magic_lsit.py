from typing import Optional, List, Any


class MagicList:
    """The list does not change if there was any error, while class instance was used as context manager."""
    def __init__(self, items: Optional[List] = None) -> None:
        if items is not None:
            self._items = items
        else:
            self._items = []

    def __enter__(self) -> List:
        self._temp_items = self._items[:]  # makes shallow copy
        return self._temp_items

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        # exc_type - is the type of exception if any was raised,
        # in case of the problem it is ValueError (could be any other).

        if exc_val is None:  # checks if there were no errors
            self._items = self._temp_items[:]  # makes shallow copy

    def __repr__(self) -> List:
        return str(self._items)


if __name__ == '__main__':
    some_list = MagicList([1, 2, 3])
    with some_list as _list:
        _list.append(4)
        _list.append(5)
    assert str(some_list) == str([1, 2, 3, 4, 5])

    try:
        with some_list as _list:
            _list.append(100)
            _list.append(200)
            raise ValueError("error here!!!")
    except ValueError:
        pass

    # no changes due to error
    # 100 and 200 were not added !
    assert str(some_list) == str([1, 2, 3, 4, 5])
