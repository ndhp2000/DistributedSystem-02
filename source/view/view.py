import pygame

from source.config import *
from source.view.maze import MazeView
from source.view.notification import NotificationView
from source.view.player import PlayerView
from source.view.scoreboard import ScoreboardView


class MainGameView:
    _MAZE_SCREEN_RATIO_ = (2 / 3, 1)
    _MAZE_SCREEN_OFFSET_ = (0, 0)

    _NOTIFICATION_SCREEN_RATIO_ = (1 / 3, 2 / 3)
    _NOTIFICATION_SCREEN_OFFSET_ = (2 / 3, 0)

    _SCOREBOARD_SCREEN_RATIO_ = (1 / 3, 1 / 3)
    _SCOREBOARD_SCREEN_OFFSET_ = (2 / 3, 2 / 3)

    def __init__(self):
        pygame.init()
        self._screen_display_ = pygame.display
        self._screen_display_.set_caption('Zace Maze')
        self._screen_ = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)
        self._maze_screen_ = None
        self._scoreboard_screen_ = None
        self._player_view_ = None
        self._notification_screen_ = None
        self._enemy_view_ = []

    def update(self, player=None):
        # self._maze_screen_.add_to_parent(self._screen_, (self.maze_screen_offset_y, self.maze_screen_offset_x))
        # world_pos = self.convert_maze_to_world_pos(player.position[0], player.position[1])
        # self._player_view_.add_to_parent(self._screen_, location=world_pos)

        # Update Notification View
        notification_screen_offset_y = self._NOTIFICATION_SCREEN_OFFSET_[0] * self._screen_.get_height()
        notification_screen_offset_x = self._NOTIFICATION_SCREEN_OFFSET_[1] * self._screen_.get_width()
        self._notification_screen_.add_to_parent(self._screen_,
                                                 (notification_screen_offset_x, notification_screen_offset_y))

        # Update Scoreboard View
        scoreboard_screen_offset_y = self._SCOREBOARD_SCREEN_OFFSET_[0] * self._screen_.get_height()
        scoreboard_screen_offset_x = self._SCOREBOARD_SCREEN_OFFSET_[1] * self._screen_.get_width()
        self._scoreboard_screen_.add_to_parent(self._screen_, (scoreboard_screen_offset_x, scoreboard_screen_offset_y))

        self._screen_display_.update()

    def init_maze(self, maze):
        maze_screen_height = int(self._screen_.get_height() * self._MAZE_SCREEN_RATIO_[0])
        maze_screen_width = int(self._screen_.get_width() * self._MAZE_SCREEN_RATIO_[1])
        maze_screen_offset_y = self._MAZE_SCREEN_OFFSET_[0] * self._screen_.get_height()
        maze_screen_offset_x = self._MAZE_SCREEN_OFFSET_[1] * self._screen_.get_width()
        self._maze_screen_ = MazeView(maze, maze_screen_height, maze_screen_width)
        self._maze_screen_.add_to_parent(self._screen_, (maze_screen_offset_y, maze_screen_offset_x))

    def init_player(self, player, enemies=[]):
        self._player_view_ = PlayerView(player)
        world_pos = self.convert_maze_to_world_pos(player.position[0], player.position[1])
        self._player_view_.add_to_parent(self._screen_, location=world_pos)

        for p in enemies:
            enemy_view = PlayerView(p)
            enemy_view.add_to_parent(self._screen_)
            self._enemy_view_.append(enemy_view)

    @staticmethod
    def convert_maze_to_world_pos(maze_x, maze_y):
        maze_screen_height = int(WIN_HEIGHT * MainGameView._MAZE_SCREEN_RATIO_[0])
        maze_screen_width = int(WIN_WIDTH * MainGameView._MAZE_SCREEN_RATIO_[1])

        cell_height = int(maze_screen_height / MAP_HEIGHT)
        cell_width = int(maze_screen_width / MAP_WIDTH)
        world_x = (maze_x * cell_height + cell_height / 2)
        world_y = (maze_y * cell_width + cell_width / 2)

        return (world_x, world_y)

    def init_scoreboard(self):
        scoreboard_screen_height = int(self._screen_.get_height() * self._SCOREBOARD_SCREEN_RATIO_[0])
        scoreboard_screen_width = int(self._screen_.get_width() * self._SCOREBOARD_SCREEN_RATIO_[1])
        scoreboard_screen_offset_y = self._SCOREBOARD_SCREEN_OFFSET_[0] * self._screen_.get_height()
        scoreboard_screen_offset_x = self._SCOREBOARD_SCREEN_OFFSET_[1] * self._screen_.get_width()
        self._scoreboard_screen_ = ScoreboardView(scoreboard_screen_height, scoreboard_screen_width)
        self._scoreboard_screen_.add_to_parent(self._screen_, (scoreboard_screen_offset_x, scoreboard_screen_offset_y))

    def init_notification(self):
        notification_screen_height = int(self._screen_.get_height() * self._NOTIFICATION_SCREEN_RATIO_[0])
        notification_screen_width = int(self._screen_.get_width() * self._NOTIFICATION_SCREEN_RATIO_[1])
        notification_screen_offset_y = self._NOTIFICATION_SCREEN_OFFSET_[0] * self._screen_.get_height()
        notification_screen_offset_x = self._NOTIFICATION_SCREEN_OFFSET_[1] * self._screen_.get_width()
        self._notification_screen_ = NotificationView(notification_screen_height, notification_screen_width)
        self._notification_screen_.add_to_parent(self._screen_,
                                                 (notification_screen_offset_x, notification_screen_offset_y))

    def print_log(self, text):
        self._notification_screen_.print(text)
