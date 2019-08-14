# Example1

def easy_decorator(f):
    def improved_f(*args, **kwags):
        if kwags.get("pip"):
            print("GREAT")
            result = f(*args)
            print("WORK")
            return result
        else:
            print("Hello")
            result = f(*args, 100)
            print("Bye")
            return result
    return improved_f


@easy_decorator
def do_sum(*args, **kwargs):
    return sum(args)


print(do_sum(1, 2, 3, 4, 5, pip=1))

# Example2

from operator import mul
from functools import reduce


def decorate_function(f):
    def decorator(*args, **kwargs):
        print("Hello")
        if "_k" in kwargs.keys():
            new_args = []
            for i in args:
                i += 1
                new_args.append(i)
            print(new_args)
            result = f(new_args, **kwargs)
        else:
            new_args = []
            for i in args:
                i -= 1
                new_args.append(i)
            print(new_args)
            result = f(new_args, **kwargs)
        return result
    return decorator


@decorate_function
def g(*args, **kwargs):
    if "_k" in kwargs.keys():
        return sum(*args)
    else:
        return reduce(mul, *args)
