import asyncio

TASK_NUMBER = 10


async def worker(mark: int, condition: asyncio.Condition) -> None:
    async with condition:
        print(f"Started-{mark}")
        await asyncio.sleep(1)
        await condition.wait()
        print(f"Work started-{mark}")
        await asyncio.sleep(1)
        print(f"Work done-{mark}")


async def notifier(condition: asyncio.Condition) -> None:
    while True:
        await asyncio.sleep(4)
        if condition.locked():
            condition.notify(2)
            print("Notified two!")
        else:
            # this part is used to exclude deadlock
            # it turnt out that  condition.notify does not work
            # if lock is not locked
            print("Can't notify without locked lock.")
            async with condition:
                condition.notify(1)
                print("Notified one!")


async def amain() -> None:
    condition = asyncio.Condition()
    notifier_task = asyncio.create_task(notifier(condition))
    await asyncio.gather(*[worker(i, condition) for i in range(1, TASK_NUMBER + 1)])
    notifier_task.cancel()
    try:
        await notifier_task  # await task cancel here
    except asyncio.CancelledError:
        print("notifier_task was cancelled")


if __name__ == '__main__':
    asyncio.run(amain())
