import struct
from typing import Optional, Tuple

# list of messages which is used in the app

DELIMITER = struct.Struct("!4s")   # indicates what kind of message we expect to receive

ACTION_ONE = struct.Struct("!III")  # sends 3 `unsigned integer` digits

ACTION_TWO = struct.Struct("!IIIII")  # sends 5 `unsigned integer` digits

ACTION_THREE = struct.Struct("!10s")  # send char[10]

RESULT = struct.Struct("!II20s")  # send

# it is written this way deliberately, it shows order of messages in "client message"
CLIENT_MESSAGE_SIZE = DELIMITER.size + ACTION_ONE.size\
                      + DELIMITER.size + ACTION_TWO.size\
                      + DELIMITER.size + ACTION_THREE.size

SERVER_MESSAGE_SIZE = DELIMITER.size + RESULT.size


ACTIONS = {
    b"ACT1": ACTION_ONE,
    b"ACT2": ACTION_TWO,
    b"ACT3": ACTION_THREE,
    b"REST": RESULT,
    b"DLMR": DELIMITER,
}


class ServerSidePrepareResultOps:
    """Handles messages from client, and prepares result messages."""
    def __init__(self, incoming_bytearray: bytearray) -> None:
        self.incoming_bytearray = incoming_bytearray  # array we read from
        self.offset = 0  # current read position

    def _handle_delimiter(self) -> bytes:
        delimiter = DELIMITER.unpack_from(self.incoming_bytearray, self.offset)
        delimiter = delimiter[0]
        self.offset += DELIMITER.size
        return delimiter

    def _handle_action_one(self) -> int:
        a, b, c = ACTION_ONE.unpack_from(self.incoming_bytearray, self.offset)
        self.offset += ACTION_ONE.size
        return a + b + c

    def _handle_action_two(self) -> int:
        a, b, c, d, e = ACTION_TWO.unpack_from(self.incoming_bytearray, self.offset)
        self.offset += ACTION_TWO.size
        return abs(a - b + c - d + e)

    def _handle_action_three(self) -> bytes:
        res = ACTION_THREE.unpack_from(self.incoming_bytearray, self.offset)
        res = res[0].strip(b'\x00').decode("utf8")
        self.offset += ACTION_THREE.size
        return f"!!!{res}!!!".encode("utf8")

    def create_result_message(self, result_bytearray: bytearray, offset: int = 0) -> Optional[int]:
        """
        result_bytearray - we write results to the array
        offset - is the current offset in result_bytearray
        """
        if self.offset == len(self.incoming_bytearray):
            return  # we reached the end of array

        if self.offset + CLIENT_MESSAGE_SIZE > len(self.incoming_bytearray):
            # arrays contains not full message, which we'll cause error
            # we do not consider the situation in the app
            return None

        res1, res2, res3 = None, None, None
        while True:
            if not (res1 is None or res2 is None or res3 is None):
                break  # if all parts of message sequence were found

            delimiter = self._handle_delimiter()
            if delimiter == b"ACT1":
                res1 = self._handle_action_one()
            elif delimiter == b"ACT2":
                res2 = self._handle_action_two()
            elif delimiter == b"ACT3":
                res3 = self._handle_action_three()
            else:
                return None  # if the rest of bytearray is field with b"\x00"

        if res1 is None or res2 is None or res3 is None:
            # indicates that part of message in another bunch of data,
            # but we ignore the situation in this test app
            # we expect that the whole message in the same bunch of information
            return None

        # pack results into result_bytearray
        DELIMITER.pack_into(result_bytearray, offset, b"REST")
        offset += DELIMITER.size
        RESULT.pack_into(result_bytearray, offset, res1, res2, res3)
        offset += RESULT.size

        return offset


class ClientSideCreateInitialMessagesOps:
    """Creates client messages which will be sent to server."""
    def __init__(
        self,
        outcoming_bytearray: bytearray,  # messages are written to this bytearray
        phase_one_args: Tuple[int, int, int],
        phase_two_args: Tuple[int, int, int, int, int],
        phase_three_arg: Tuple[bytes],
        offset: int = 0  # current array offset
    ) -> None:
        self.outcoming_bytearray = outcoming_bytearray
        self.offset = offset

        self.phase_one_args = phase_one_args
        self.phase_two_args = phase_two_args
        self.phase_three_arg = phase_three_arg

    def create_outcomming_message_sequence(self) -> int:
        phases = [b"ACT1", b"ACT2", b"ACT3"]
        phases_args = [self.phase_one_args, self.phase_two_args, self.phase_three_arg]

        for phase, args in zip(phases, phases_args):
            DELIMITER.pack_into(self.outcoming_bytearray, self.offset, phase)
            self.offset += DELIMITER.size
            ACTIONS[phase].pack_into(self.outcoming_bytearray, self.offset, *args)
            self.offset += ACTIONS[phase].size

        return self.offset


class ClientSideHandleServerAnswerOps:
    """Handles server messages to read."""
    def __init__(self, incoming_bytearray: bytearray) -> None:
        self.incoming_bytearray = incoming_bytearray  # array from server we read from
        self.offset = 0  # current offset position in self.incoming_bytearray

    def read_server_answer(self) -> Optional[Tuple[int, int, str]]:
        if self.offset == len(self.incoming_bytearray):
            return None  # we reached the end of array

        if self.offset + SERVER_MESSAGE_SIZE > len(self.incoming_bytearray):
            # arrays contains not full message, which we'll cause error
            # we do not consider the situation in the app
            return None

        delimiter = DELIMITER.unpack_from(self.incoming_bytearray, self.offset)[0]
        if delimiter != b'REST':
            return None  # array has some empty bytes

        self.offset += DELIMITER.size
        res = RESULT.unpack_from(self.incoming_bytearray, self.offset)
        self.offset += RESULT.size

        val1, val2, val3 = res

        val3 = val3.strip(b'\x00').decode("utf8")

        return val1, val2, val3


def _main():
    # STAGE#1 create client side messages:
    client_outcoming_bytearray = bytearray(CLIENT_MESSAGE_SIZE * 2)  # len should be >= CLIENT_MESSAGE_SIZE * 2

    offset = 0
    offset = ClientSideCreateInitialMessagesOps(
        outcoming_bytearray=client_outcoming_bytearray,
        phase_one_args=(1, 2, 3),
        phase_two_args=(1, 2, 3, 4, 15),
        phase_three_arg=("Hello".encode("utf8"), ),
        offset=offset,
    ).create_outcomming_message_sequence()

    ClientSideCreateInitialMessagesOps(
        outcoming_bytearray=client_outcoming_bytearray,
        phase_one_args=(7, 7, 7),
        phase_two_args=(1, 2, 3, 4, 0),
        phase_three_arg=("Big".encode("utf8"), ),
        offset=offset,
    ).create_outcomming_message_sequence()

    # STAGE#2 create server side messages:
    server_results_bytearray = bytearray(SERVER_MESSAGE_SIZE * 2)  # len should be >= SERVER_MESSAGE_SIZE * 2
    offset = 0
    server_ops = ServerSidePrepareResultOps(client_outcoming_bytearray)
    while offset is not None:
        offset = server_ops.create_result_message(server_results_bytearray, offset=offset)

    # STAGE#3 read server side messages:
    get_results = ClientSideHandleServerAnswerOps(server_results_bytearray)
    while True:
        res = get_results.read_server_answer()
        if res is None:
            break
        print(f"Res1: {res[0]} | Res2: {res[1]} | Res3: {res[2]}")


if __name__ == '__main__':
    _main()
