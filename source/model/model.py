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
        self._players_ = {}
        self._player_bullets_ = []
        self._enemy_bullets_ = {}
        self.clock = pygame.time.Clock()

    def init_maze(self):
        self._maze_ = Maze()
    
    def init_player(self):
        pos = np.array([0, 0])
        main_player = Player(pos.astype('float64'), self._maze_._adj_matrix_)
        self._players_[0] = main_player

    def add_player(self):
        pass

    def add_event(self, player_id, event_id):
        self._events_.append((player_id, event_id))

    # def update(self, key_pressed=None):
    #     if len(self._events_) > 0:
    #         player_id, event_type = self._events_.popleft()
    #         player = self._players_[player_id]
    #
    #         if event_type in PLAYER_MOVEMENT:
    #             new_pos = player.pre_move(event_type, 0.5)
    #             direction = event_type
    #             print(new_pos)
    #             is_valid = self._maze_.is_player_pos_valid(new_pos, direction)
    #
    #             if is_valid:
    #                 player.move(event_type)
    #                 return
    #             else:
    #                 player.action = STOP
    #                 return
    #
    #         elif event_type in PLAYER_SHOOT:
    #             bullet = self._player_[player_id].shoot(event_type)
    #             if player_id not in self._bullets_:
    #                 self._player_bullets_ = deque()
    #                 self._player_bullets_.append(bullet)
    #
    #     player.move()
    #
    #         # elif event_type in PLAYER_HIT:
    #         #     pass

    # def update(self, key_pressed=None):
    #     dt = self.clock.tick(20) / 1000.0
    #     player_id = 0
    #     player = self._players_[0]
    #
    #     if key_pressed is not None:
    #         new_pos = player.pre_move(key_pressed, dt)
    #         direction = key_pressed
    #         is_valid = self._maze_.is_player_pos_valid(new_pos, direction)
    #
    #         if is_valid:
    #             player.move(new_pos, direction)
    #             return
    #         else:
    #             player.action = STOP
    #             player.direction = STOP
    #             return
    #
    #     if player.direction != STOP:
    #         new_pos = player.pre_move(player.direction, 0.5)
    #         is_valid = self._maze_.is_player_pos_valid(new_pos, player.direction)
    #
    #         if not is_valid:
    #             player.action = STOP
    #             player.direction = STOP
    #         else:
    #             player.move(new_pos, player.direction)

    def update(self, key_pressed=None):
        dt = self.clock.tick(30) / 1000.0
        player_id = 0
        player = self._players_[0]

        if key_pressed is not None:
            player.move(key_pressed, dt)
            return

        if player.future_change_direction != STOP:
            player.move(player.future_change_direction, dt)
            return

    def get_maze(self):
        return self._maze_

    def get_player(self):
        return self._players_[0]
