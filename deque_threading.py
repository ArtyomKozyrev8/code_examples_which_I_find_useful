import threading
import collections
import time

def take_form_queue(q:collections.deque, direction:"str" ='right') ->"None":
    if direction=='right':
        for i in range(len(q)):
            try:
                element=q.pop()
            except IndexError:
                print("No values left")
                break
            else:
                print(element)
                time.sleep(1)
        
    elif direction=="left":
        for i in range(len(q)):
            try:
                element=q.popleft()
            except IndexError:
                print("No values left")
                break
            else: 
                print(element)
                time.sleep(1)
    else:
        raise Exception("wrong arg type")
        
if __name__=="__main__":
    massive=collections.deque("abcdefg")
    rightThread=threading.Thread(target=take_form_queue,args=(massive,'right',),)
    leftThread=threading.Thread(target=take_form_queue,args=(massive,'left',),)
    rightThread.start()
    leftThread.start()
    rightThread.join()
    leftThread.join()
    print("Work is done")
    time.sleep(5)
