import threading
import time
import random

def day(semaph):
    sema.acquire()
    for i in range(0,5):
        print("DAY")
        time.sleep(3)
    sema.release()
        
def month(semaph):
    sema.acquire()
    for i in range(0,5):
        print("MONTH")
        time.sleep(3)
    sema.release()
        
def century(semaph):
    sema.acquire()
    for i in range(0,5):
        print("CENTURY")
        time.sleep(3)
    sema.release()
        
def minute(semaph):
    sema.acquire()
    for i in range(0,5):
        print("MINUTE")
        time.sleep(3)
    sema.release()
        
semaph=threading.Semaphore(3)
threads=[]
wrapper=[day,month,century,minute]
for i in range(4):
    threads.append(threading.Thread(target=wrapper[i],args=(sema,),))
for i in threads:
    i.start()
