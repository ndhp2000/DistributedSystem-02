from source.model.maze import Maze
from collections import deque
from source.model.player import Player
from source.config import *

class MainGameLogic:
    def __init__(self):
        self._maze_ = None
        self._events_ = deque()
        self._players_ = {}
        self._player_bullets_ = []
        self._enemy_bullets_ = {}
        self._events_ = []

    def init_maze(self):
        self._maze_ = Maze()
    
    def init_player(self):
        main_player = Player()
        self._players_[0] = main_player

    def add_player(self):
        pass

    def add_event(self, event_id):
        self._events_.append(event_id)

    # def update(self):
    #     if len(self._events_) >= 0:
    #         player_id, event_type = self._event_.popleft()
    #
    #         if event_type in PLAYER_MOVEMENT:
    #             self._player_[player_id].move(event_type)
    #         elif event_type in PLAYER_SHOOT:
    #             bullet = self._player_[player_id].shoot(event_type)
    #             if player_id not in self._bullets_:
    #                 self._player_bullets_ = deque()
    #                 self._player_bullets_.append(bullet)
    #
    #         elif event_type in PLAYER_HIT:
    #             pass

    def check_valid_movement(self, player_id):
        pos = self._player_[player_id].pre_move(event_type)


    def get_maze(self):
        return self._maze_

    def get_player(self):
        return self._players_[0]
