import asyncio
from io import BytesIO


async def main():
    reader, writer = await asyncio.open_connection(host="localhost", port=8888)
    # remove comment to test slow client
    # await asyncio.sleep(20)
    for i in range(15):
        writer.write(f"hello-{i}_hello-{i}_hello-{i}\n".encode("utf8"))  # prepare data
        await asyncio.sleep(1)
        await writer.drain()  # send data

    if writer.can_write_eof():
        writer.write_eof()  # tell server that we sent all data

    # better use BytesIO than += if you gonna concat many times
    data_from_server = BytesIO()  # now get server answer
    try:
        while True:
            # read chunk up to 8 kbytes
            data = await asyncio.wait_for(reader.read(8192), timeout=1.0)
            data_from_server.write(data)
            # if server told use that no more data
            if reader.at_eof():
                break

        print(data_from_server.getvalue().decode('utf8'))
        writer.close()
        await writer.wait_closed()
    except ConnectionAbortedError:
        # if our client was too slow
        print("Server timed out connection")
        writer.close()
    except (asyncio.TimeoutError, asyncio.CancelledError):
        # if server was too slow
        print("Did not get answer from server due to timeout")
        writer.close()

if __name__ == '__main__':
    asyncio.run(main())
