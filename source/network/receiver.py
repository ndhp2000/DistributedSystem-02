import json
import logging
import socket
import threading
from queue import Queue

logger = logging.getLogger("game-socket")


class Receiver(threading.Thread):
    def __init__(self, game_socket):
        super().__init__()
        self._socket_ = game_socket
        self._queue_ = Queue(0)  # already thread-safe
        self._shutdown_flag_ = threading.Event()

    def receive(self, is_block=False):
        return self._queue_.get(block=is_block)

    def run(self):
        while not self._shutdown_flag_.is_set():
            try:
                data_size = int.from_bytes(self._socket_.recv(4), 'big', signed=False)
                if not data_size:
                    break
                raw_packet = self._socket_.recv(data_size)
                packet = json.loads(raw_packet.decode('utf-8'))
                logger.info('Receiver received packet {}'.format(packet))
                self._queue_.put(packet)
            except socket.timeout:
                pass
            except OSError:
                logger.warning('SERVER ERROR - STOP RECEIVING MESSAGES')
                self._shutdown_flag_.set()

    def set_shutdown_flag(self):
        self._shutdown_flag_.set()
