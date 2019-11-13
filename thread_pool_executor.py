from concurrent.futures import ThreadPoolExecutor, Future
import time
from threading import current_thread


def rsquare(x):
    """
    :param x: Future object 
    :return: int or float
    """
    if x == 5:
        raise ValueError("Hello World")
    time.sleep(1)
    return x**2


def on_action(x):
    """
    :param x: Future
    :return: None
    The function runs when Future is called
    """
    if x.cancelled():  # if Future was canceled in main thread
        print(f"LOL Task {x.xenon} was canceled in {current_thread().getName()}")
    else:
        if x.exception():  # if there was an exception if Future
            print(f"Task {x.xenon} was finished with exception {x.exception()} in {current_thread().getName()}")
        else:
            if x.result():  # if there was no exceptions in Future, show result
                print(f"Task {x.xenon} was finished fine with result {x.result()} in {current_thread().getName()}")


if __name__ == '__main__':
    pool = ThreadPoolExecutor(4)  # create thread pool
    tasks = [i for i in range(1, 11)] 
    my_futures = [pool.submit(rsquare, t) for t in tasks]  # alternative to pool which sends futures to pool one by one
    k = 1
    for i in my_futures:
        i.xenon = k
        i.add_done_callback(on_action)  # add action to Future
        k += 1
    for i in my_futures:
        if i.cancel():  # try to cancel some Futures before they start running
            print(f"Task {i.xenon} was successfully canceled in {current_thread().getName()}")
