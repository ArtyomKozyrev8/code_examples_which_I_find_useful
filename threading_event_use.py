'''The example shows how to use thread.Event() to control start, stop of different Threads'''


import time
import threading

def start_another_thread(e):
    '''It is thread which starts twor other threads'''
    time.sleep(3)
    print("game was started")
    e.set()
       
def infinity(h,e):
    '''It is thread which start printing word h,
    when e is True and stops when e is made to False when stop()
    method change e to False '''
    e.wait(100) # waits 100 seconds for e event comes True, otherwise never happens
    while(e.is_set()):
        time.sleep(2)
        print(f"{h}")
        
def stop(e):
    '''Change e event value again to False'''
    e.wait(20) # waits 20 seconds for e event comes True, otherwise never happens
    print("We stop now")
    time.sleep(4)
    e.clear()
    
   
   
e=threading.Event()
h="Hello"
a = threading.Thread(target=infinity,name="infinity",args=(h,e,))
b = threading.Thread(target=start_another_thread,name="start", args=(e,))
c = threading.Thread(target=stop, name="stop", args=(e,))
a.start()
b.start()
c.start()
