import asyncio
import sys


async def get_date():
    # sys.executable is a path to python interpreter

    code = (
        "import datetime\n"
        "import time\n"
        "for _ in range(10):"
        "\n\ttime.sleep(2)"
        "\n\tprint(datetime.datetime.now())"
    )

    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-c', code,  # run the code
        stdout=asyncio.subprocess.PIPE,
    )

    while res := await proc.stdout.readline():
        print(res.decode("utf8").strip())

    await proc.wait()  # await the end of task

    print(proc.returncode)


if __name__ == '__main__':
    date = asyncio.run(get_date())
