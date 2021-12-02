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
        self._logic_.init_player()

        # Init View
        self._view_ = MainGameView()
        self._view_.init_maze(self._logic_.get_maze())
        self._view_.init_player(self._logic_.get_player())

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
        return STOP

    def input_listener(self):
        key_pressed = self.getValidKey()
        self._logic_.add_event(key_pressed)

    def event_listener(self):
        pass

    def loop(self):
        while True:
            # Event Handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    
            # Input listener
            self.input_listener()
            # Update Logic
            self._logic_.update()
            # Update View
            self._view_.update()
