from source.model.maze import Maze
from collections import deque

class MainGameLogic:
    def __init__(self):
        self._maze_ = None
        self._events_ = deque()
        self._players_ = {}
        self._bullets_ = {}

    def init_maze(self):
        self._maze_ = Maze()
    
    def init_player(self):
        main_player = Player()
        self._players_.append(main_player)

    def add_player(self):
        pass

    def add_event(self, event_id):
        self._event_.append(event_id)

    def update(self):
        if len(self._event_) >= 0:
            player_id, event_type = self._event_.popleft()

            if event_type in PLAYER_MOVEMENT:
                self._player_[player_id].update(event_type)
            elif event_type in PLAYER_SHOOT:
                bullet = self._player_[player_id].update(event_type)
                if player_id not in self_bullets_:
                    self._bullets_ = deque()
                    self._bullets_.append(bullet)

    def get_maze(self):
        return self._maze_
