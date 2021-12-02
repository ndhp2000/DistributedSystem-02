from sys import exit

import pygame
from pygame.locals import *

from ..model.maze import Maze
from ..model.model import MainGameLogic
from ..view.view import MainGameView


class Controller:
    def __init__(self):
        # Init Logic
        self._logic_ = MainGameLogic()
        self._logic_.init_maze()

        # Init View
        self._view_ = MainGameView()
        self._view_.init_maze(self._logic_.get_maze())

    def loop(self):
        while True:
            # Event Handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            # Update Logic
            # Update View
            self._view_.update()
