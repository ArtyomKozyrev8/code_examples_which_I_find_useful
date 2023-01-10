"""This should illustrate how future works (error handling part only)."""


from typing import Any, Optional, Callable


class Result:
    """Result wrapper which allows to return error or result."""
    def __init__(self, res: Optional[Any] = None, exc: Optional[Exception] = None) -> None:
        self._res = res
        self._exc = exc

    def result(self) -> Any:
        if self._res:
            return self._res

        if self._exc:
            raise self._exc


def some_func(x: float, y: float) -> float:
    """Just some func which can return result or raise error."""
    return x/y


def wrapper(word_print, f: Callable, /, *args, **kwargs) -> Result:  # always Result it is beneficial
    """Wrapper with callback function inside."""
    print(word_print)
    try:
        return Result(res=f"{word_print}_{f(*args, **kwargs)}")  # run callback function f here
    except Exception as ex:
        return Result(exc=ex)


if __name__ == '__main__':
    res1 = wrapper("Alfa", some_func, 1, 2)
    print(res1.result())  # fine result of callback function

    res2 = wrapper("Omega", some_func, x=1, y=0)  # result was returned despite the error in some_func
    res2.result()  # result - reraise error

