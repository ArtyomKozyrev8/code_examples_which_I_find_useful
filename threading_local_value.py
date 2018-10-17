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
g=threading.Thread(target=give_to_local_arg_value,args=(a,),)
g.start()
