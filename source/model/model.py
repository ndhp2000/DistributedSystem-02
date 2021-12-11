from source.model.maze import Maze
from collections import deque
from source.model.player import Player, Enemy
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
        self.flag = True

    def init_maze(self):
        self._maze_ = Maze()
    
    def init_player(self):
        pos = np.array([0, 0])
        self._player_ = Player(pos.astype('float64'), self._player_bullets_, self._maze_._adj_matrix_)

    def get_maze(self):
        return self._maze_

    def get_player(self):
        return self._player_

    def get_bullets(self):
        return self._player_bullets_

    def get_enemies_group(self):
        return self._enemies_

    def add_player(self):
        pass

    def add_event(self, player_id, event_id):
        self._events_.append((player_id, event_id))

    def update(self, event=None, dt=0):
        player_id = 0
        self._player_.update(event, dt)
        self._enemies_.update(None, dt)

        self._player_bullets_.update(dt)
        self._enemy_bullets_.update(dt)

        if self.flag:
            enemy = Enemy(np.array([10, 5]), self._enemy_bullets_, self._enemies_, self._maze_._adj_matrix_)



    def check_collision(self):
        collided_bullet = pygame.sprite.spritecollide(self._player_, self._enemy_bullets_, True)
        enemies_hit = pygame.sprite.groupcollide(self._enemies_, self._player_bullets_, False, True)

        for enemy in enemies_hit:
            enemy.hit(DAMAGE)

        for bullet in collided_bullet:
            self._player_.hit(DAMAGE)