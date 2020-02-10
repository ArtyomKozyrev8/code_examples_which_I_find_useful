# mother.py

import asyncio
from asyncio import CancelledError


async def speak_with_child(p):
    x = await asyncio.create_subprocess_shell(
        "python child.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    while True:
        line = await x.stdout.readline()
        if not line:
            break
        print(line.decode('utf8').rstrip("\n"))

    p.cancel()  # stop pinger Task


async def pinger():
    while True:
        print("Beep!")
        await asyncio.sleep(0.5)


async def main():
    start = asyncio.get_running_loop().time()
    print("Started")
    p = asyncio.create_task(pinger())
    sp = asyncio.create_task(speak_with_child(p))
    await sp
    try:
        await p
    except CancelledError:
        print("Pinger stopped!")

    ended = asyncio.get_running_loop().time()
    print(f"Ended within: {ended - start}")


if __name__ == '__main__':
    loop = asyncio.ProactorEventLoop()
    loop.run_until_complete(main())
    loop.close()
    
########################################################################################################################################

# child.py

import time
import sys

if __name__ == '__main__':
    for i in range(10):
        print(f"Child Message {i}")
        time.sleep(1)
        sys.stderr.write("Small error ")

    sys.stderr.write("Terrible Error")
    
