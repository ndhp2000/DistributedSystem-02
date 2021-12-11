from source.model.maze import Maze
from collections import deque
from source.model.player import Player
from source.config import *
import numpy as np
import pygame

class MainGameLogic:
    def __init__(self):
        self._maze_ = None
        self._events_ = deque()
        self._enemies_ = pygame.sprite.Group()
        self._player_bullets_ = pygame.sprite.Group()
        self._player_ = None
        self._enemy_bullets_ = pygame.sprite.Group()

    def init_maze(self):
        self._maze_ = Maze()
    
    def init_player(self):
        pos = np.array([0, 0])
        self._player_ = Player(pos.astype('float64'), self._player_bullets_, self._maze_._adj_matrix_)

    def add_player(self):
        pass

    def add_event(self, player_id, event_id):
        self._events_.append((player_id, event_id))

    def update(self, event=None, dt=0):
        player_id = 0
        self._player_.update(event, dt)

        for bullet in self._player_bullets_:
            bullet.update(dt)

    def get_maze(self):
        return self._maze_

    def get_player(self):
        return self._player_

    def get_bullets(self):
        return self._player_bullets_

    def check_player_collision(self):
        collided_bullet = pygame.sprite.groupcollide(self._player_, self._enemy_bullets_)