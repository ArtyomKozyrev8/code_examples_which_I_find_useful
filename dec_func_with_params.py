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
