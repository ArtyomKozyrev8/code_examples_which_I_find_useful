import asyncio
from datetime import datetime
from functools import partial
import io
import platform
import socket


def time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[0:-3]


async def server_callback(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    *,
    welcome_slogan: str,
    chunk_read_size: int,
    client_timeout: float,
) -> None:
    """Callback function which should always have only two args: reader and writer, which are 'stream' objects."""
    server_host, server_port = writer.get_extra_info("sockname")  # server own host and port
    in_host, in_port = writer.get_extra_info("peername")  # client host and port

    print(f"[{time()}]: Server {server_host}:{server_port} has connection from {in_host}:{in_port}")

    data_buffer = io.BytesIO()

    while True:
        try:
            data = await asyncio.wait_for(reader.read(chunk_read_size), timeout=client_timeout)

            if data == b'' or reader.at_eof():  # check if it was end message
                break

            data_buffer.write(data)

            if reader.at_eof():
                break

            if data_buffer.getvalue().endswith(b"\r\n\r\n"):  # check if it was end of http message
                break

        except asyncio.TimeoutError:
            print(f"[{time()}]: Server {server_host}:{server_port}"
                  f" broke connection with {in_host}:{in_port} due to timeout.")
            await writer.drain()  # clear buffer, though it is expected to be empty
            writer.close()

            return

    results = data_buffer.getvalue().decode('utf8').strip("\r\n\r\n")
    print(f"[{time()}]: Server {server_host}:{server_port} received from {in_host}:{in_port}:\n{results}\n")

    answer = f"""
    <html>
        <head>
            <title>{welcome_slogan}</title>
        </head>
        <body>
            <h1>[{time()}]: {welcome_slogan}</h1>
            <p>We glad to see you! {welcome_slogan}</p>
        </body>
    </html>
    """
    response = 'HTTP/1.0 200 OK\n\n' + answer
    writer.write(response.encode("utf8"))  # it writes data to buffer storage, rather than sending data
    await writer.drain()  # actually sends data to client

    if writer.can_write_eof():
        writer.write_eof()

    writer.close()
    print(f"[{time()}]: Server {server_host}:{server_port} successfully closed connection with {in_host}:{in_port}")


async def run_server(
    host: str,
    port: int,
    *,
    welcome_slogan: str = "The magic server!",
    chunk_read_size: int = 8192,
    client_timeout: float = 10.0,
) -> None:
    server = await asyncio.start_server(
        partial(
            server_callback,
            welcome_slogan=welcome_slogan,
            chunk_read_size=chunk_read_size,
            client_timeout=client_timeout,
        ),
        host=host,
        port=port,
        family=socket.AF_INET,  # ipv4
    )
    async with server:
        print(f"[{time()}]: Server started on {host}:{port}")
        await server.serve_forever()


async def grateful_shutdown() -> None:
    cur_task = asyncio.current_task()
    tasks = [t for t in asyncio.all_tasks() if t is not cur_task]
    for t in tasks:
        t.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)


def server_done_callback(fut: asyncio.Future, server_name: str) -> None:
    if fut.cancelled():
        print(f"Server {server_name} was stopped!")


if __name__ == '__main__':
    # FIXME raises Exception ignored in: <function _ProactorBasePipeTransport.__del__ at ...
    #  RuntimeError: Event loop is closed on Windows with ProactorEventLoop

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        server_tasks = (
            loop.create_task(run_server("0.0.0.0", 9999, chunk_read_size=10)),
            loop.create_task(run_server("0.0.0.0", 8888, welcome_slogan="Welcome to home server!")),
            loop.create_task(run_server("0.0.0.0", 7777, welcome_slogan="Welcome to borring server!")),
        )
        names = ("0.0.0.0:9999", "0.0.0.0:8888", "0.0.0.0:7777")
        [t.add_done_callback(partial(server_done_callback, server_name=name)) for name, t in zip(names, server_tasks)]
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(grateful_shutdown())
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.run_until_complete(loop.shutdown_default_executor())
        asyncio.set_event_loop(None)
        if not loop.is_closed():
            loop.close()

