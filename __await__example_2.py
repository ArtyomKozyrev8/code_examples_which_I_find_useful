"""Better way to use threads without async long polling like in example_1."""

import asyncio
import threading
import time


async def ticker():
    """Just some kind of async ticker function."""
    while True:
        await asyncio.sleep(1)
        print("tick tack sleep...")


class ThreadAwaitableWithToThread:
    """Illustrates how to wrap Thread in awaitable object."""
    def do_work(self):
        """Some target function for another Thread."""
        cur_th_name = threading.current_thread().getName()
        for i in range(5):
            print(f"Do work-{i} in {cur_th_name}")
            time.sleep(2)

        return "well done result!"

    def __await__(self):
        """Magic method to create awaitable object."""
        # to_thread is wrapper around run_in_executor
        result = yield from asyncio.to_thread(self.do_work).__await__()
        # The same without asyncio.to_thread:
        # result = yield from loop.run_in_executor(None, self.do_work).__await__()
        return result


async def amain():
    """Main asyncio entrypoint of the app."""
    t = asyncio.create_task(ticker())  # "daemon" task
    res = await ThreadAwaitableWithToThread()
    t.cancel()  # cancel "daemon" task
    print(f"Result: {res}")

if __name__ == '__main__':
    asyncio.run(amain())
