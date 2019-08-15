# Example1

def overlap(show=True):
    def decorate_smth(f):
        def new_func():
            if show:
                print("Hello")
                f()
                print("World")
            else:
                print("BYE")
                f()
                print("ME")
        return new_func
    return decorate_smth


@overlap(False)
def print_word():
    print("WORD")


#Example2

def overlap_func_with_params(_sum=True):
    def decorator(f):
        def new_f(a, b):
            if _sum:
                a += 1
                b += 1
            else:
                a -= 1
                b -= 1
            return f(a, b)
        return new_f
    return decorator


@overlap_func_with_params(False)
def print_sum(a, b):
    return a + b


#Example3

def return_formatted_text(text_format="Name: {} Surname: {}"):
    def decorator(f):
        def decorated_func(name, surname):
            _name, _surname = f(name, surname)
            return text_format.format(_name, _surname)
        return decorated_func
    return decorator


@return_formatted_text("n: {} s: {}")
def return_n_s(name, surname):
    return name, surname

print(return_n_s("Mark", "Stew"))

#Example4
def word_decorator(_struct="{}_"):
    def decorator(f):
        def decorated_f(*args):
            new_args = f(*args)
            n = len(new_args)
            new_struct = _struct * n
            print(new_struct)
            print(new_args)
            return new_struct.format(*new_args)
        return decorated_f
    return decorator


@word_decorator("Structure  {} ")
def take_return(*args):
    new_args = []
    for i in args:
        new_args.append(i + "X")
    return new_args

print(take_return("X1", "Y1", "Z1", "G", "H", "O"))

#Example5 timeit with args increase decorator

import time


def increased_args_timeit(increase=False):
    def timeit_dec(f):
        def decorated_f(*args, **kwargs):
            t1 = time.perf_counter()
            print("Start work...")
            if increase:
                new_args = [i + 1 for i in args]
            else:
                new_args = args
            result = f(*new_args, **kwargs)
            print("End work: {}".format(time.perf_counter() - t1))
            return result
        return decorated_f
    return timeit_dec


@increased_args_timeit(True)
def do_some_work(*args, **kwargs):
    _sum = 0
    for i in args:
        _sum += i
        time.sleep(0.3)
    for j in kwargs.values():
        _sum += j
        time.sleep(0.3)
    return _sum


print(do_some_work(1, 2, 3, 4, 5, 6, 3, 3, 3, k1=1, k2=2, k3=3))
