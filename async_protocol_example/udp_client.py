import asyncio
import socket
import time


class UdpServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, msg: str, all_done: asyncio.Future):
        self.msg = msg
        self.all_done = all_done  # used to stop client
        self.transport = None

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport
        data = self.msg.encode("utf8")
        for i in range(10):
            self.transport.sendto(data)
            time.sleep(1)
        self.transport.sendto(b"ok")  # notify receiver that it is last message

    def datagram_received(self, data: bytes, addr):
        if data == b"ok":
            self.all_done.set_result(100)  # if receiver answered stop all work

    def connection_lost(self, exc) -> None:
        if exc:
            print(f"Connection lost due to error: {exc}")


async def main_server():
    loop = asyncio.get_event_loop()
    all_done = asyncio.Future()
    message = "Hello world Dear Friends!"
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpServerProtocol(
            msg=message,
            all_done=all_done
        ),
        remote_addr=("localhost", 8888, ),  # address of our udp server, which we want to connect to
        family=socket.AF_INET,
    )
    try:
        await asyncio.wait_for(all_done, timeout=60.0)
    except asyncio.TimeoutError:
        print("Client session is closed due to timeout")
    except Exception as ex:
        print(ex)  # catch all other exceptions
    else:
        print(f"Get answer from server: {all_done.result()}")
    finally:
        transport.close()


if __name__ == '__main__':
    asyncio.run(main_server())
