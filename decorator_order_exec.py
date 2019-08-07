# PAY ATTENTION THAT DECORATOR do its' work first. See lines: myfunclist.append(f) and  print(f)
# And only when decorator finish its' step, f functions (improved_f) are run !!
# Actually I expected that myfunclist will be empty

myfunclist = []


def decorator_ffunc(f):
    myfunclist.append(f)
    print(f)
    
    def improved_f():
        print("__________")
        f()
        print("__________")
    return improved_f


@decorator_ffunc
def f1():
    print("Start f1")


@decorator_ffunc
def f2():
    print("Start f2")


def f3():
    print("Start f3")


def main():
    print(myfunclist)
    f1()
    f2()
    f3()


if __name__ == "__main__":
    main()
    
# OUTPUT:    
"""
<function f1 at 0x000002488509A620>
<function f2 at 0x000002488509A730>
[<function f1 at 0x000002488509A620>, <function f2 at 0x000002488509A730>]
__________
Start f1
__________
__________
Start f2
__________
Start f3

Process finished with exit code 0
"""
