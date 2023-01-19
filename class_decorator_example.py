import inspect
from functools import partial

METHOD_SIGNATURE = "(self, melody: str = None) -> None"
METHOD_NAME = "music"


def check_that_class_has_method_music(cls: object, method_name: str, method_signature: str) -> object:
    """This class decorator checks that class has method which have a certain signature."""

    base_error_message = f"class should implement '{method_name}' method," \
                         f" which have the following signature: '{method_signature}'."

    method = getattr(cls, method_name, None)

    if method is None:
        raise AttributeError(" ".join((base_error_message, "No such method.")))

    if not inspect.isfunction(method):
        raise AttributeError(" ".join((base_error_message, "No a method function.")))

    if str(inspect.signature(method)) != method_signature:
        raise AttributeError(" ".join((base_error_message, "Not a method.")))

    return cls


@partial(check_that_class_has_method_music, method_name=METHOD_NAME, method_signature=METHOD_SIGNATURE)
class MyMusic:
    """Some class which should implement 'music' method."""
    def music(self, melody: str = None) -> None:
        if melody is None:
            melody = "Lazy Melody"

        print(melody)


if __name__ == '__main__':
    MyMusic().music(melody="Class Decorator Melody.")
