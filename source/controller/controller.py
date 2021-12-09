from sys import exit
import time
import pygame
from pygame.locals import *

from ..model.maze import Maze
from ..model.model import MainGameLogic
from ..view.view import MainGameView
from ..network.network import GameNetwork
from source.config import *


class Controller:
    def __init__(self):
        # Init Logic
        self._logic_ = MainGameLogic()
        self._logic_.init_maze()
        self._logic_.init_player()

        # Init View
        self._view_ = MainGameView()
        self._view_.init_maze(self._logic_.get_maze())
        self._view_.init_player(self._logic_.get_player())

        # Init Network
        self._game_network_ = GameNetwork()
        self._instance_id_ = self._game_network_.join_game()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        if key_pressed[K_SPACE]:
            return SHOOT
        return None

    # def input_listener(self):
    #     key_pressed = self.getValidKey()
    #
    #     if key_pressed is not None:
    #         self._logic_.add_event(0, key_pressed)
    #
    # def event_listener(self):
    #     pass

    def loop(self):
        while True:
            # Event Handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    
            # Input listener
            # self.input_listener()
            # Update Logic
            key_pressed = self.getValidKey()
            self._logic_.update(key_pressed)
            # Update View
            self._view_.update(self._logic_.get_player())

            time.sleep(0.5)
            self._game_network_.send({'type': '_EXAMPLE_BROADCAST_', 'instance_id': self._instance_id_})

