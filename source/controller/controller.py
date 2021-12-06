import time
from sys import exit

import pygame
from pygame.locals import *

from ..model.maze import Maze
from ..model.model import MainGameLogic
from ..network.network import GameNetwork
from ..view.view import MainGameView


class Controller:
    def __init__(self):
        # Init Logic
        self._logic_ = MainGameLogic()
        self._logic_.init_maze()

        # Init View
        self._view_ = MainGameView()
        self._view_.init_maze(self._logic_.get_maze())

        # Init Network
        self._game_network_ = GameNetwork()
        self._instance_id_ = self._game_network_.join_game()

    def loop(self):
        while True:
            # Event Handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    self._game_network_.safety_closed()
                    exit()
            # Update Logic
            # Update View
            self._view_.update()
            time.sleep(0.5)
            self._game_network_.send({'type': '_EXAMPLE_BROADCAST_', 'instance_id': self._instance_id_
                                      })
