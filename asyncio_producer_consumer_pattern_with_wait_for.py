import asyncio
from functools import partial
from time import monotonic

WORKERS_NUM = 20
TASKS_NUM = 1000


def callback(fut: asyncio.Future, name: str) -> None:
    if fut.cancelled():
        print(f"{name} was cancelled.")


async def producer(q: asyncio.Queue, task_num: int) -> None:
    for i in range(1, task_num + 1):
        await q.put(f"Task-{i}")
        await asyncio.sleep(0.5)


async def worker(q: asyncio.Queue) -> None:
    timeout = 2  # each task has its own timeout
    while True:
        try:
            task_name = asyncio.current_task().get_name()
            res = await asyncio.wait_for(q.get(), timeout=timeout)
        except asyncio.TimeoutError:
            print(f"{task_name} got timeout, when timeout time was {timeout}")
            timeout += 1.0  # increase timeout if too fast
        else:
            print(f"{task_name}: {res}")
            if timeout > 0:
                timeout -= 0.1  # decrease timeout
            q.task_done()


async def amain() -> None:
    q = asyncio.Queue(5)
    prod_task = asyncio.create_task(producer(q, TASKS_NUM))

    worker_tasks = [asyncio.create_task(worker(q)) for _ in range(WORKERS_NUM)]
    [t.set_name(f"Worker-{i}") for i, t in enumerate(worker_tasks, start=1)]
    [t.add_done_callback(partial(callback, name=t.get_name())) for t in worker_tasks]

    await prod_task
    await q.join()  # ensure that all tasks were done

    for t in worker_tasks:
        t.cancel()

    await asyncio.gather(*worker_tasks, return_exceptions=True)  # to catch all cancel errors

if __name__ == '__main__':
    start = monotonic()
    asyncio.run(amain())
    print(f"Time passed: {monotonic() - start}")
