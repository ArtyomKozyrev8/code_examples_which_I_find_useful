from abc import abstractmethod, ABC
from typing import Any, Optional


class Typed(ABC):
    """Base Descriptor class."""

    # __set_name__ is used to create field self.private_name
    # which is "connected" with field in parent class
    def __set_name__(self, owner: object, field_name: str) -> None:
        self.private_name = field_name

    def __get__(self, instance: object, owner: object) -> Any:
        return getattr(self, self.private_name)

    def __set__(self, instance: object, value: Any) -> None:
        self.validate(value)
        setattr(self, self.private_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Should be defined in child classes."""
        pass


class Integer(Typed):
    """Descriptor class Integer."""
    def __init__(self, min_val: Optional[int] = None, max_val: Optional[int] = None) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError("Should be integer.")

        if self.min_val is not None:
            if value < self.min_val:
                raise ValueError("Too small number.")

        if self.max_val is not None:
            if value > self.max_val:
                raise ValueError("Too big number.")


class String(Typed):
    """Descriptor class String."""
    def __init__(self, min_len: Optional[int] = None, max_len: Optional[int] = None) -> None:
        self.min_length = min_len
        self.max_length = max_len

    def validate(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("Should be string.")

        if self.min_length is not None:
            if len(value) < self.min_length:
                raise ValueError("Too short string.")

        if self.max_length is not None:
            if len(value) > self.max_length:
                raise ValueError("Too long string.")


class TargetClass:
    """Class which use descriptors."""
    name = String(5, 15)
    age = Integer(0, 199)

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name}, {self.age})"

    def increase_age(self) -> None:
        self.age += 1


if __name__ == '__main__':
    x = TargetClass(name="Alfa1", age=1)  # no errors
    assert str(x) == "TargetClass(Alfa1, 1)"

    names = ["Alfa", "Alfa1", "Alfa1", "Alfa1", 1, "Alfa1" * 100]
    ages = [1, 200, -1, "1", 1, 1]
    errors = [
        "Too short string.", "Too big number.", "Too small number.",
        "Should be integer.", "Should be string.", "Too long string.",
    ]

    for name, age, error in zip(names, ages, errors):
        try:
            TargetClass(name=name, age=age)
        except (ValueError, TypeError) as ex:
            assert error == str(ex)

    x.increase_age()
    assert str(x) == "TargetClass(Alfa1, 2)"
