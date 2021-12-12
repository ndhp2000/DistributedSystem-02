from collections import deque

import numpy as np

from source.model.enity_group import Group
from source.model.maze import Maze
from source.model.player import Player


class MainGameLogic:
    def __init__(self):
        self._maze_ = None
        self._events_ = deque()
        self._players_ = Group()
        self._bullets_ = Group()

        self.flag = True

    def init_maze(self):
        self._maze_ = Maze()

    def init_players(self, player_id=0):
        pos = np.array([0, 0])
        self._players_.add(Player(pos.astype('float64'), self._maze_, player_id))

    def init_bullets(self):
        pass

    def get_maze(self):
        return self._maze_

    def get_players(self):
        return self._players_

    def get_bullets(self):
        return self._bullets_

    def add_player(self, new_player):
        self._players_.add(new_player)

    def update(self, event=None, dt=0):
        player_id = 0  # FAKE
        self._players_.update(event, dt, self._bullets_)

        self._bullets_.update(dt)

        # if self.flag:
        #     enemy = Player(np.array([10, 5]), self._enemies_bullets_, self._enemies_, self._maze_)

        # self.check_collision()

    # def check_collision(self):
    #     collided_bullet = pygame.sprite.spritecollide(self._players_, self._enemies_bullets_, True)
    #     enemies_hit = pygame.sprite.groupcollide(self._enemies_, self._player_bullets_, False, True)
    #
    #     for enemy in enemies_hit:
    #         enemy.hit(DAMAGE)
    #
    #     for bullet in collided_bullet:
    #         self._player_.hit(DAMAGE)
