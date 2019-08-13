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
