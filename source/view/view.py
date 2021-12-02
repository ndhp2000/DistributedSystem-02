import pygame

from source.config import WIN_WIDTH, WIN_HEIGHT
from source.view.maze import MazeView


class MainGameView:
    _MAZE_SCREEN_RATIO_ = (2 / 3, 1)
    _MAZE_SCREEN_OFFSET_ = (0, 0)

    _NOTIFICATION_SCREEN_RATIO_ = (1 / 3, 3 / 4)
    _NOTIFICATION_SCREEN_OFFSET_ = (2 / 3, 0)

    _SCOREBOARD_SCREEN_RATIO_ = (1 / 3, 1 / 4)
    _SCOREBOARD_SCREEN_OFFSET_ = (2 / 3, 3 / 4)

    def __init__(self):
        pygame.init()
        self._screen_display_ = pygame.display
        self._screen_display_.set_caption('Zace Maze')
        self._screen_ = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)
        self._maze_screen_ = None

    def update(self):
        self._screen_display_.update()

    def init_maze(self, maze):
        maze_screen_height = int(self._screen_.get_height() * self._MAZE_SCREEN_RATIO_[0])
        maze_screen_width = int(self._screen_.get_width() * self._MAZE_SCREEN_RATIO_[1])
        maze_screen_offset_y = self._MAZE_SCREEN_OFFSET_[0] * self._screen_.get_height()
        maze_screen_offset_x = self._MAZE_SCREEN_OFFSET_[1] * self._screen_.get_width()
        self._maze_screen_ = MazeView(maze, maze_screen_height, maze_screen_width)
        self._maze_screen_.add_to_parent(self._screen_, (maze_screen_offset_y, maze_screen_offset_x))

    def init_player(self):
        pass

    def init_score_board(self):
        pass

    def init_notification(self):
        pass
