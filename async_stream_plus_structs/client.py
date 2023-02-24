import asyncio
from time import monotonic
import logging

from async_stream_plus_structs.structs_for_server_clients import (
    CLIENT_MESSAGE_SIZE,
    ClientSideCreateInitialMessagesOps,
    ClientSideHandleServerAnswerOps,
)
from async_stream_plus_structs.logger import logger as log

RESULT_COUNTER = 0

MESSAGE_NUMBER = 7000

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7676

WORKERS_NUM = 100

CLIENT_TIMEOUT = 30
CLIENT_CHUNK_SIZE = 1024


async def main():
    start = monotonic()
    log.debug(f"Started time passed: {monotonic() - start}")
    global RESULT_COUNTER
    reader, writer = await asyncio.open_connection(host=SERVER_HOST, port=SERVER_PORT)
    log.debug(f"Created connection time passed: {monotonic() - start}")

    client_outcoming_bytearray = bytearray(CLIENT_MESSAGE_SIZE * MESSAGE_NUMBER)

    offset = 0
    for i in range(0, MESSAGE_NUMBER):
        offset = ClientSideCreateInitialMessagesOps(
            outcoming_bytearray=client_outcoming_bytearray,
            phase_one_args=(i, i, i),
            phase_two_args=(i, i, i, i, i),
            phase_three_arg=(f"{i}".encode("utf8"),),
            offset=offset,
        ).create_outcomming_message_sequence()

    log.debug(f"Prepared message time passed: {monotonic() - start}")

    log.debug(f"Outcomming message bytes number: {len(client_outcoming_bytearray)}")
    writer.write(client_outcoming_bytearray)  # prepare data
    await writer.drain()  # send data

    if writer.can_write_eof():
        writer.write_eof()  # tell server that we sent all data

    log.debug(f"Sent data to server time passed: {monotonic() - start}")

    server_results_bytearray = bytearray()

    try:
        while True:
            data = await asyncio.wait_for(reader.read(CLIENT_CHUNK_SIZE), timeout=CLIENT_TIMEOUT)
            server_results_bytearray.extend(data)
            # if server told use that no more data
            if reader.at_eof():
                break

        log.debug(f"Received data to server time passed: {monotonic() - start}")

        get_results = ClientSideHandleServerAnswerOps(server_results_bytearray)
        while True:
            res = get_results.read_server_answer()
            if res is None:
                break

            if res[2] == f"!!!{MESSAGE_NUMBER-1}!!!":
                RESULT_COUNTER += 1

            # log.debug(f"Res1: {res[0]} | Res2: {res[1]} | Res3: {res[2]}")

        writer.close()
    except ConnectionAbortedError:
        # if our client was too slow
        log.error("Server timed out connection")
        writer.close()
    except (asyncio.TimeoutError, asyncio.CancelledError):
        # if server was too slow
        log.error("Did not get answer from server due to timeout")
        writer.close()


async def amain():
    start = monotonic()
    try:
        global RESULT_COUNTER
        await asyncio.gather(*[main() for _ in range(WORKERS_NUM)])
        log.info(f"Successfully finished workers: {RESULT_COUNTER}. Total Messages: {RESULT_COUNTER * MESSAGE_NUMBER}")
    finally:
        log.info(f"Time passed: {monotonic() - start}")


if __name__ == '__main__':
    log.setLevel(logging.INFO)
    asyncio.run(amain())
