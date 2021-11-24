from source.model.maze import Maze


class MainGameLogic:
    def __init__(self):
        self._maze_ = None

    def init_maze(self):
        self._maze_ = Maze()

    def get_maze(self):
        return self._maze_
