import inspect


METHOD_SIGNATURE = "(self, melody: str = None, repeat_times: int = None) -> str"
METHOD_NAME = "music_land"


class Music:
    def __init_subclass__(cls, method_name, method_signature, **kwargs) -> None:
        base_error_message = (
            f"class should implement '{method_name}' method, "
            f"which have the following signature: '{method_signature}'."
        )

        method = getattr(cls, method_name, None)

        if method is None:
            raise AttributeError(" ".join((base_error_message, "No such method.")))

        if not inspect.isfunction(method):
            raise AttributeError(" ".join((base_error_message, "No a method function.")))

        if str(inspect.signature(method)) != method_signature:
            raise AttributeError(" ".join((base_error_message, "Not a method.")))


class TheMusic(Music, method_name=METHOD_NAME, method_signature=METHOD_SIGNATURE):
    """Some class which should implement 'music_land' method."""
    def music_land(self, melody: str = None, repeat_times: int = None) -> str:
        if melody is None:
            melody = "Lazy Melody!"

        if repeat_times is None:
            repeat_times = 1

        return " ".join([melody] * repeat_times)


if __name__ == '__main__':
    print(TheMusic().music_land(melody="Subclass Melody!", repeat_times=3))
