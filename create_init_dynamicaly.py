"""Illustrates how to create __init__ dynamically."""


def create_init(*params):
    """Creates __init__ func dynamically"""
    line1 = f"def __init__(self, {', '.join([i for i in params])}):\n\t"
    line2 = '\n\t'.join([f'self.{i} = {i}' for i in params])

    gl = {}  # create global scope for exec
    exec(line1 + line2, gl)

    for i in gl.items():
        print(f"###   {i}   ###")

    return gl['__init__']  # get create func __init__ from gl


class Vector:
    __init__ = create_init('x', 'y', 'z')


if __name__ == '__main__':
    a = Vector(1, 2, 3)
    print(a)
