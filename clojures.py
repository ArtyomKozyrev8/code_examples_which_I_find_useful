# Variables inside of functions are used to store data aboout function execution

# SOLUTION WITHOUT CLOSURES

class Avereger:
    def __init__(self):
        self.elements = []

    def __call__(self, element):
        self.elements.append(element)
        return sum(self.elements)/len(self.elements)


x = Avereger()
print("SOLUTION WITHOUT CLOSURES")
print(x(1))
print(x(3))
print(x(5))
print(x(21))


# SOLUTION WITH CLOSURES 1

def make_average():
    _list = []
    def avg(element):
        _list.append(element)
        return sum(_list)/len(_list)
    return avg

print("Example1:")
x = make_average()

print(x(2))
print(x(4))
print(x(3))
print(x(7))
print(x(24))

# SOLUTION WITH CLOSURES 2

def new_make_average():
    sum_of_elemnts = 0
    number_of_elements = 0
    def avg(element):
        nonlocal sum_of_elemnts, number_of_elements
        sum_of_elemnts += element
        number_of_elements += 1
        return sum_of_elemnts/number_of_elements
    return avg

y = new_make_average()
print("Example2:")
print(y(2))
print(y(4))
print(y(3))
print(y(7))
print(y(34))

# OUTPUT:
"""
SOLUTION WITHOUT CLOSURES
1.0
2.0
3.0
7.5

Example1:
2.0
3.0
3.0
4.0
8.0

Example2:
2.0
3.0
3.0
4.0
10.0
"""
