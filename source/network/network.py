from datetime import datetime
import logging
import socket
import time
from queue import Empty

from source.config import SERVER_IP, SERVER_PORT
from source.network.receiver import Receiver
from source.network.sender import Sender

logger = logging.getLogger("game-socket")


class GameNetwork:
    _server_ip_ = SERVER_IP
    _server_port_ = SERVER_PORT

    def __init__(self):
        self._socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket_.settimeout(0.2)
        self._make_connection_()
        self._sender_ = Sender(self._socket_)
        self._receiver_ = Receiver(self._socket_)
        self._sender_.start()
        self._receiver_.start()

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
                    logger.warning(
                        'Connection to {}:{} failed for {} time. Exit game.'.format(self._server_ip_,
                                                                                    self._server_port_, retries))
                    break
                logger.warning(
                    'Connection to {}:{} failed, retry after 500 milliseconds.'.format(self._server_ip_,
                                                                                       self._server_port_))
                time.sleep(0.5)
        logger.info('Made connection successfully'.format())

    def join_game(self):
        sent_packet = {'type': '_JOIN_GAME_'}
        self.send(sent_packet)
        # Block until receive
        print("Please wait to log in...")
        received_packet = self.receive(1, is_block=True)
        print(received_packet)
        return received_packet[0]['instance_id'], received_packet[0]['user_id']

    def get_game_state(self, instance_id, user_id):
        sent_packet = {'type': '_GET_STATE_', 'instance_id': instance_id, 'user_id': user_id}
        self.send(sent_packet)
        # Block until receive
        print("Please wait to load game state")
        received_packet = self.receive(1, is_block=True)
        return received_packet[0]

    def send_action(self, instance_id, user_id, event_key):
        sent_packet = {'type': '_GAME_ACTION_', 'instance_id': instance_id, 'user_id': user_id, 'action': event_key}
        self.send(sent_packet)

    def send(self, packet):
        packet = {
            '__time_sent__': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'game': packet
        }
        self._sender_.send(packet)

    def receive(self, max_nums_packets: int, is_block=False):
        result = []
        for i in range(max_nums_packets):
            try:
                packet = self._receiver_.receive(is_block)
                result.append(packet['game'])
            except Empty:
                return result
        return result

    def safety_closed(self):
        logger.warning('Network close')
        self._sender_.set_shutdown_flag()
        self._receiver_.set_shutdown_flag()
        self._socket_.close()
