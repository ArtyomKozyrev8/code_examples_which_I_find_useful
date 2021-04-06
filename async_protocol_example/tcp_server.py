"""
clients are based on streams! see async_stream_example
"""

import asyncio
import socket
from collections import defaultdict
from io import BytesIO
from time import sleep


class TestServerPrTCP(asyncio.Transport):
    def __init__(self, ip, port):
        self.transport = None
        self.ip = ip
        self.port = port
        self.storage = defaultdict(BytesIO)

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        self.transport.set_write_buffer_limits(high=1024)
        ip, port = self.transport.get_extra_info("peername")
        print(f"Server received incoming connection from {ip}:{port}")

    def connection_lost(self, exc):
        ip, port = self.transport.get_extra_info("peername")
        if exc:
            print(f"Connection with {ip}:{port} was lost due to error")
        else:
            print(f"Connection with {ip}:{port} was closed")

    def pause_writing(self):
        print(self.transport.get_write_buffer_size())
        print("too big fuck came")

    def resume_writing(self):
        print("continue fucking")

    def data_received(self, data):
        ip, port = self.transport.get_extra_info("peername")
        self.storage[f"{ip}:{port}"].write(data)

    def eof_received(self):
        ip, port = self.transport.get_extra_info("peername")
        data = self.storage[f"{ip}:{port}"].getvalue()
        print(f"All data received from {ip}:{port}:\n{data.decode('utf8')}")
        self.transport.write(b"Hello from Server|\n")
        self.transport.write(data)
        del self.storage[f"{ip}:{port}"]
        self.transport.write_eof()
        self.transport.close()
        return False


async def main_server():
    loop = asyncio.get_event_loop()
    serv = await loop.create_server(
        lambda: TestServerPrTCP(
            ip="localhost",
            port=8888,
        ),
        host="localhost",
        port=8888,
        family=socket.AF_INET
    )

    async with serv:
        await serv.serve_forever()

if __name__ == '__main__':
    asyncio.run(main_server())
