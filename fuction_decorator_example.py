from functools import wraps


def magic_with_param(op_type=None, param=None):
    """magic_with_param desc."""
    def magic_decorator(f):
        """magic_decorator desc."""
        @wraps(f)
        def inner(*args, **kwargs):
            """inner desc."""
            if op_type == "mul":
                result = f(*args, **kwargs) * param
            elif op_type == "div":
                result = f(*args, **kwargs) / param
            else:
                result = f(*args, **kwargs)

            return result

        return inner

    return magic_decorator


@magic_with_param(op_type="mul", param=100)
def plus(x: int, y: int, z: int) -> int:
    """Plus desc."""
    return x + y + z


@magic_with_param(op_type="div", param=100)
def minus(x, y):
    """Minus desc."""
    return x - y


if __name__ == '__main__':
    print(plus(1, 2, 3))
    print(minus(4, 3))
    print(help(plus))
