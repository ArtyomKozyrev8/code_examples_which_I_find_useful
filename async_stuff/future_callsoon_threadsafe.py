import asyncio
from threading import Thread
from queue import Queue
import queue
import time
from functools import partial
from random import randint


class SomeMagicConnector(Thread):
    """The class represent some imaginary connection not compatible with asyncio"""
    def __init__(self):
        super().__init__()
        self.task_q = Queue()
        self._active = False
        self.daemon = True

    def connect(self):
        """Actually starts connector Thread"""
        self._active = True
        self.start()

    def run(self) -> None:
        """run is what happens why you call Thread().start() - check Python stdlib docs"""
        while True:
            try:
                fut, func = self.task_q.get(timeout=0.1)  # get tasks from Main Tread
            except queue.Empty:
                if self._active:
                    continue
                else:
                    break
            else:
                loop = fut.get_loop()
                try:
                    res = func()
                except Exception as ex:
                    loop.call_soon_threadsafe(fut.set_exception, ex)
                else:
                    loop.call_soon_threadsafe(fut.set_result, res)

    def _exec(self, func, *args, **kwargs) -> asyncio.Future:
        """Wrapper around all sync methods of the class"""
        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        self.task_q.put((fut, partial(func, *args, **kwargs)))
        return fut

    @staticmethod
    def _heavy_work(a: int, b: int) -> int:
        """Some random sync method"""
        time.sleep(5)
        if a == 5 or b == 5:
            raise ValueError(f"Bad params for heavy work: a={a}, b={b}")
        return 10 + a + b

    async def heavy_work(self, a: int, b: int) -> int:
        """async wrapper around _heavy_work"""
        fut = self._exec(self._heavy_work, a, b)
        await fut  # fut will be provided with result by Child Thread (this Class)
        return fut.result()


async def ticker() -> None:
    """Just ticker"""
    for i in range(6):
        await asyncio.sleep(1)
        print(i)


async def amain() -> None:
    """Main async function of the app"""
    conn = SomeMagicConnector()
    conn.connect()
    while True:
        a = randint(0, 5)
        await asyncio.sleep(1)
        b = (randint(0, 5))
        r = await asyncio.gather(ticker(), conn.heavy_work(a, b), return_exceptions=True)
        print(r)

if __name__ == '__main__':
    asyncio.run(amain())
