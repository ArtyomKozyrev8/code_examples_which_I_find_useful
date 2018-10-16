import threading
import time

# lock.acquire() is used to block other threads (which use the same lock instance) from doing their job, lock.release() release lock and 
# another thread can start doing its work.

def hello(lock):
    lock.acquire()
    print("Hello function started")
    for i in range(5):
        time.sleep(1)
        print(f"Hello {threading.current_thread().getName()}")
    time.sleep(1)
    print("Hello function is finished")
    lock.release()
        
def hey(lock):
    lock.acquire()
    print("HEY function started")
    for i in range(5):
        time.sleep(1)
        print(f"HEY {threading.current_thread().getName()}")
    time.sleep(1)
    print("HEY function is finished")
    lock.release()
    
lock =threading.Lock()
a=threading.Thread(target=hello,name="HELLO_THREAD",args=(lock,),)
b=threading.Thread(target=lol,name="HEY_THREAD",args=(lock,),)

a.start()
b.start()

for i in threading.enumerate():
    if i.getName() != 'MainThread':
        i.join()
    else: pass
print("Program is finished")
for i in threading.enumerate():
    print(i.getName())
time.sleep(5)
