# iterator class example:


class MyIterator:
    def __init__(self, repeat):
        self.repeat = repeat

    def __iter__(self):
        return self

    def __next__(self):
        if self.repeat >= 0:
            temp = self.repeat**2 + 100
            self.repeat -= 1
            return temp  # pay attention that it is not yield but return
        raise StopIteration  # do not forget to raise error to stop iteration

    def __repr__(self):
        return f"{self.__class__.__name__}({self.repeat})"

# generator function example


def mygenerator(repeat):
    i = 0
    while i <= repeat:
        temp = i**2 + 100
        i += 1
        yield temp

# function for generator sequence example


def minus_value(seq):
    for i in seq:
        yield i - 100


def multiply(seq, number):
    for i in seq:
        yield i * number


def square(seq):
    for i in seq:
        yield i * i


if __name__ == '__main__':
    # this is iterator class example:

    x = MyIterator(10)
    print(next(x))
    for i in x:
        print(i)
    print(x)
    print("*" * 100)

    # this is generaror function example:

    for i in mygenerator(10):
        print(i)
    print("*" * 100)

    # this is unnamed generator
    print(type(i**2 + 100 for i in range(0, 11)))
    for j in (i**2 + 100 for i in range(0, 11)):
        print(j)

    print("*" * 100)

    # this is generator sequence

    for j in square(multiply(minus_value(i for i in range(0, 11)), -1)):
        print(j)
