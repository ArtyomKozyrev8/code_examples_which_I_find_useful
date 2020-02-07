import asyncio
from asyncio import CancelledError, shield


async def shielded(i):
    await asyncio.sleep(7)
    print(f"shielded {i}")


async def not_so_shielded(i):
    await asyncio.sleep(7)
    print(f"Not shielded {i}")


async def ordinary_task(i):
    print(f"Task({i}) started")
    await shield(shielded(i))
    await asyncio.create_task(not_so_shielded(i))
    await asyncio.sleep(3)
    print(f"Task({i}) stopped")


async def cancel(tasks):
    await asyncio.sleep(1)
    for i, t in enumerate(tasks):
        if i % 2 == 0:
            t.cancel()


async def main():
    tasks = [asyncio.create_task(ordinary_task(i)) for i in range(1, 11)]
    can = asyncio.create_task(cancel(tasks))
    for t in tasks:
        try:
            await t
        except CancelledError:
            pass

    await can

if __name__ == '__main__':
    asyncio.run(main())
