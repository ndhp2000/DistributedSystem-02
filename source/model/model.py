from collections import deque

import numpy as np

from source.model.entity_group import Group, PlayerGroup
from source.model.maze import Maze
from source.model.player import Player, Bot
from source.config import *


class MainGameLogic:
    def __init__(self):
        self._maze_ = None
        self._events_ = deque()
        self._players_ = PlayerGroup()
        self._bullets_ = Group()
        self.flag = True

    def init_maze(self):
        self._maze_ = Maze()

    def init_players(self):
        pos = np.array([0, 0])
        player_id = 0
        self._players_.add(Player(pos.astype('float64'), self._maze_, player_id))
        self._players_.add(Bot(pos.astype('float64'), self._maze_, player_id + 1))
        # self._players_.add(Bot(pos.astype('float64'), self._maze_, player_id + 2))
        # self._players_.add(Bot(pos.astype('float64'), self._maze_, player_id + 3))

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
        self.check_collisions(dt)
        self._players_.update(event, dt, self._bullets_)

        self._bullets_.update(dt)


    def check_collisions(self, dt):
        players_hit = Group.groups_collide(self._players_, self._bullets_, True, dt)

        #print(players_hit)
        for player in players_hit:
            player.hit(BULLET_DAMAGE)

