import asyncio
from random import randint


def my_factory(loop, coro):
    f = asyncio.Task(coro, loop=loop)
    f.name = f"TaskNameIs {randint(100, 999)}"
    return f


async def test():
    for i in range(5):
        print(f"Step-{i}")
        await asyncio.sleep(1)


async def main():
    x = asyncio.create_task(test())
    y = asyncio.create_task(test())
    await x
    await y
    print(x.name)
    print(y.name)

if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    _loop.set_debug(True)
    _loop.set_task_factory(my_factory)
    _loop.run_until_complete(main())
    _loop.close()
