import asyncio
from functools import partial
import socket
import logging

from async_stream_plus_structs.logger import logger as log
from async_stream_plus_structs.structs_for_server_clients import (
    ServerSidePrepareResultOps,
)


CHUNK_READ_SIZE = 1024

CLIENT_TIMEOUT = 30.0

HOST = "0.0.0.0"

PORT = 7676

STOP_SERVER_EVENT = asyncio.Event()  # used to "prevent" new connections


async def server_callback(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    *,
    chunk_read_size: int,
    client_timeout: float,
) -> None:
    """
    This Callback function which should always have only two args: reader and writer, which are 'stream' objects.

    "chunk_read_size" and "client_timeout" are additional args, hereby the function should be used with partial.
    """
    if STOP_SERVER_EVENT.is_set():
        writer.close()
        return

    server_host, server_port = writer.get_extra_info("sockname")  # server own host and port
    in_host, in_port = writer.get_extra_info("peername")  # client host and port

    log.debug(f"Server {server_host}:{server_port} has connection from {in_host}:{in_port}")

    input_bytes = bytearray()

    while True:
        try:
            data = await asyncio.wait_for(reader.read(chunk_read_size), timeout=client_timeout)

            if data == b'' or reader.at_eof():
                break

            input_bytes.extend(data)

        except asyncio.TimeoutError:
            log.error(f"Server {server_host}:{server_port} broke connection with {in_host}:{in_port} due to timeout.")
            writer.close()
            return

    offset = 0
    server_results_bytearray = bytearray(len(input_bytes))
    server_ops = ServerSidePrepareResultOps(input_bytes)
    while offset is not None:
        offset = server_ops.create_result_message(server_results_bytearray, offset=offset)

    writer.write(server_results_bytearray)  # it writes data to buffer storage, rather than sending data
    await writer.drain()  # actually sends data to client

    if writer.can_write_eof():
        writer.write_eof()

    writer.close()
    log.debug(f"Server {server_host}:{server_port} successfully closed connection with {in_host}:{in_port}")


async def run_server(
    host: str,
    port: int,
    *,
    client_timeout: float,
    chunk_read_size: int = 8192,
) -> None:
    server = await asyncio.start_server(
        partial(
            server_callback,
            chunk_read_size=chunk_read_size,
            client_timeout=client_timeout,
        ),
        host=host,
        port=port,
        family=socket.AF_INET,  # ipv4
    )
    async with server:
        log.info(f"Server started on {host}:{port}")
        await server.serve_forever()


async def grateful_shutdown() -> None:
    STOP_SERVER_EVENT.set()
    cur_task = asyncio.current_task()
    tasks = [t for t in asyncio.all_tasks() if t is not cur_task]
    done, pending = await asyncio.wait(tasks, timeout=CLIENT_TIMEOUT)
    [t.cancel() for t in pending]

    await asyncio.gather(*pending, return_exceptions=True)  # "eat" CancelError messages


def server_done_callback(fut: asyncio.Future, server_name: str) -> None:
    if fut.cancelled():
        log.info(f"Server {server_name} was stopped!")


if __name__ == '__main__':
    log.setLevel(logging.INFO)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        server_tasks = (
            loop.create_task(
                run_server(HOST, PORT, chunk_read_size=CHUNK_READ_SIZE, client_timeout=CLIENT_TIMEOUT)
            ),
        )
        names = (f"{HOST}:{PORT}", )
        [t.add_done_callback(partial(server_done_callback, server_name=name)) for name, t in zip(names, server_tasks)]
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            loop.run_until_complete(grateful_shutdown())
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(loop.shutdown_default_executor())
        finally:
            asyncio.set_event_loop(None)
            if not loop.is_closed():
                loop.close()
