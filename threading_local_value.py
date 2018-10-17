import threading
import time
import random

def give_to_local_arg_value(a):
    while(True):
        try:
            h=a.value
        except AttributeError:
            print("No value was given to local variable")
            a.value=random.randint(1,100)
            time.sleep(5)
        else:
            print(f"{h}")
            break
    print("End")

a=threading.local()
a.value=5 # value is not defined attribute of local class, you can print instead of 
# a.value a.x or a.y or any other you want
g=threading.Thread(target=give_to_local_arg_value,args=(a,),)
g.start()


# if you want to have local.value as soon as you create thread:

class MyThreadLocal(threading.local):
    def __init__(self):
        super().__init__()
        self.value = random.randint(1,100)
        
def give_show_local_value(a):
    while(True):
        try:
            h=a.value
        except AttributeError:
            print("No value was given to local variable")
            a.value=random.randint(1,100)
            time.sleep(5)
        else:
            print(f"{h}")
            break
    print("End")
    
a=MyThreadLocal() 
print(a.value) # it is value which exists in the main thread
g=threading.Thread(target=give_show_local_value,args=(a,),)
g.start()
