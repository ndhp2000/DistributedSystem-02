import logging
import socket
import time
from queue import Empty

from source.config import SERVER_IP, SERVER_PORT
from source.network.receiver import Receiver
from source.network.sender import Sender

logger = logging.getLogger("game-socket")


class GameNetWork:
    _server_ip_ = SERVER_IP
    _server_port_ = SERVER_PORT

    def __init__(self):
        self._socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._make_connection_()
        self._sender_ = Sender(self._socket_)
        self._receiver_ = Receiver(self._socket_)
        self._instance_id_ = None

    def _make_connection_(self, retries=10):
        counter = 0
        while True:
            try:
                logger.info('Create connection to {}:{}'.format(self._server_ip_, self._server_port_))
                self._socket_.connect((self._server_ip_, self._server_port_))
                break
            except ConnectionRefusedError:
                counter = counter + 1
                if counter == retries:
                    raise ConnectionRefusedError
                logger.warning(
                    'Connection to {}:{} failed, retry after 500 milliseconds.'.format(self._server_ip_,
                                                                                       self._server_port_))
                time.sleep(0.5)
        logger.info('Made connection successfully'.format())

    def join_game(self):
        sent_packet = {'type': '_JOIN_GAME_'}
        self.send(sent_packet)
        result = []
        while len(result) == 0:
            result.extend(self.receive(1))
            if len(result) == 0:
                time.sleep(0.5)
        received_packet = result[0]
        self._instance_id_ = received_packet['_instance_id_']
        return self._instance_id_

    def send(self, packet):
        packet = {
            '_instance_id_': self._instance_id_,
            'game': packet
        }
        self._sender_.send(packet)

    def receive(self, max_nums_packets: int):
        result = []
        for i in range(max_nums_packets):
            try:
                packet = self._receiver_.receive()
                result.append(packet['game'])
            except Empty:
                return result
        return result
