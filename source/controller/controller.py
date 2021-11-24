from sys import exit

import pygame
from pygame.locals import *

from ..model.maze import Maze
from ..view.view import MainGameView


class Controller:
    def __init__(self):
        # Init Logic
        self.maze = Maze()

        # Init View
        self.view = MainGameView()
        self.view.init_maze(self.maze)

    def loop(self):
        while True:
            # Event Handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            # Update Logic

            # Update View
            self.view.update()
