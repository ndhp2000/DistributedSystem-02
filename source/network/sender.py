import json
import logging
import threading
from queue import Queue, Empty

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
            try:
                packet = self._queue_.get(block=False, timeout=0.2)
                logger.info("Sender send packet {}".format(packet))
                packet = packet.encode('utf-8')
                data_size = len(packet)
                packet = data_size.to_bytes(4, 'big', signed=True) + packet
                self._socket_.send(packet)
            except Empty:
                pass
            except OSError:
                self._shutdown_flag_.set()
                logger.warning("SERVER ERROR - STOP SENDING MESSAGES")

    def set_shutdown_flag(self):
        self._shutdown_flag_.set()