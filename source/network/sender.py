import json
import logging
import threading
from queue import Queue

logger = logging.getLogger("game-socket")


class Sender(threading.Thread):
    def __init__(self, game_socket):
        super().__init__()
        self._socket_ = game_socket
        self._queue_ = Queue(0)  # already thread-safe
        self._shutdown_flag_ = threading.Event()

    def send(self, packet: dict):
        self._queue_.put(json.dumps(packet))

    def run(self):
        logger.info('SENDER started to make connection'.format())

        while not self._shutdown_flag_.is_set():
            packet = self._queue_.get(block=True)
            self._socket_.send(packet.encode('utf-8'))
