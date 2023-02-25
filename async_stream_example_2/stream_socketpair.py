import asyncio
import socket
from io import BytesIO


async def reader_task(rsock: socket.socket) -> None:
    # reader and writer are wrappers around rsock
    # which works as proxy for rsock when it communicates with wsock
    reader, writer = await asyncio.open_connection(sock=rsock)
    storage = BytesIO()
    while True:
        data = await reader.read(1024)  # waits for data from wsock
        storage.write(data)
        if storage.getvalue().endswith(b'exit'):
            break

    print("READER-task received:", storage.getvalue().decode("utf8"))
    del storage

    writer.write(b"beep!beep!beep!beep!")   # write to rsock
    await writer.drain()  # sends to wsock

    writer.close()
    await writer.wait_closed()
    print(f"READER-task is finished!")


async def writer_task(wsock: socket.socket) -> None:
    loop = asyncio.get_running_loop()
    loop.call_soon(wsock.send, b'my test application!')  # looks like working the same without loop.call_soon
    await asyncio.sleep(2)
    loop.call_soon(wsock.send, b'exit')  # looks like working the same without loop.call_soon
    await asyncio.sleep(4)
    data = wsock.recv(1024)
    print(f"WRITER-task received answer: {data.decode('utf8')}")
    await asyncio.sleep(2)
    print("WRITER-task is finished.")


async def amain():
    rsock, wsock = socket.socketpair()
    try:
        await asyncio.gather(reader_task(rsock), writer_task(wsock))
    finally:
        rsock.close()
        wsock.close()


if __name__ == '__main__':
    asyncio.run(amain())
