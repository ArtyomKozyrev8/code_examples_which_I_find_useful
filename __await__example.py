import asyncio
import threading
import time


async def ticker():
    """Just some kind of async ticker function."""
    while True:
        await asyncio.sleep(1)
        print("tick tack sleep...")


class ThreadAwaitable:
    """Illustrates how to wrap Thread in awaitable object."""

    def __init__(self):
        self.done = threading.Event()  # sync between this and another thread

    def do_work(self):
        """Some target function for another Thread."""
        cur_th_name = threading.current_thread().getName()
        for i in range(5):
            print(f"Do work-{i} in {cur_th_name}")
            time.sleep(2)

        self.done.set()

    def __await__(self):
        """Magic method to create awaitable object."""
        th = threading.Thread(target=self.do_work)
        th.start()  # start another tread
        while True:
            if self.done.is_set():  # sync with another thread
                print(f"Work in {self.__class__.__name__} is done!")
                return "well done result!"

            # make loop switch between tasks while waiting another Thread to finish work.
            yield from asyncio.sleep(0.1).__await__()


async def amain():
    """Main asyncio entrypoint of the app."""
    t = asyncio.create_task(ticker())  # "daemon" task
    res = await ThreadAwaitable()
    t.cancel()  # cancel "daemon" task
    print(f"Result: {res}")


if __name__ == '__main__':
    asyncio.run(amain())
