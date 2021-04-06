import asyncio
import socket
from io import BytesIO


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print(len(asyncio.all_tasks()))  # let's show number of tasks
    ip, port = writer.get_extra_info('peername')  # get info about incoming connection
    print(f"Incoming connection from {ip}: {port}")
    # better use BytesIO than += if you gonna concat many times
    all_data = BytesIO()
    while True:
        try:
            # read chunk up to 8 kbytes
            data = await asyncio.wait_for(reader.read(8192), timeout=2.0)
            all_data.write(data)
            if reader.at_eof():
                print(f"Received data:\n{all_data.getvalue().decode('utf8')}")
                break
        except (asyncio.CancelledError, asyncio.TimeoutError):
            print("Too slow connection aborted")
            break

    writer.write(b"FROM_SERVER:\n")  # prepare data
    writer.write(all_data.getvalue())  # prepare more data
    # simulate slow server
    # await asyncio.sleep(5)
    await writer.drain()  # send all prepared data

    if writer.can_write_eof():
        writer.write_eof()

    writer.close()  # do not forget to close stream
    await writer.wait_closed()


async def main_server():
    server = await asyncio.start_server(
        client_connected_cb=handler,
        host="localhost",
        port=8888,
        family=socket.AF_INET,  # ipv4
    )

    ip, port = server.sockets[0].getsockname()
    print(f"Serving on: {ip}:{port}")
    print("*" * 200)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main_server())
