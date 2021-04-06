import asyncio
import socket


class UdpServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.transport = None

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport
        print(f"Start working on {self.ip}:{self.port}")

    def datagram_received(self, data: bytes, addr: str):
        print(f"{addr}: {data.decode('utf8')}")
        if data == b"ok":
            self.transport.sendto(b"ok", addr=addr)

    def connection_lost(self, exc) -> None:
        if exc:
            print(f"Connection lost due to error: {exc}")
        else:
            print(f"Connection closed")


async def main_server():
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpServerProtocol(
            ip="localhost",
            port=8888,
        ),
        local_addr=("localhost", 8888, ),
        family=socket.AF_INET,
    )
    try:
        await asyncio.sleep(3600)
    finally:
        transport.close()


if __name__ == '__main__':
    asyncio.run(main_server())
