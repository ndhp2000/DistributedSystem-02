import pygame

from source.config import *
from source.view.maze import MazeView
from source.view.player import PlayerView
from source.config import *
from source.view.utils import convert_maze_to_world_pos


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
        self._player_view_ = None
        self._enemies_view_ = None
        self._bullets_ = None

    # To do rewrite into using pygame sprite group
    # def __init__(self, main_game_logic):
    #     pygame.init()
    #     self.

    def update(self, player):
        self._maze_screen_.add_to_parent(self._screen_, (self.maze_screen_offset_y, self.maze_screen_offset_x))
        world_pos = convert_maze_to_world_pos(player.position[0], player.position[1])
        self._player_view_.add_to_parent(self._screen_, location=world_pos)
        self._bullets_.draw(self._screen_)
        self._enemies_view_.draw(self._screen_)
        self._screen_display_.update()

    def init_maze(self, maze):
        maze_screen_height = int(self._screen_.get_height() * self._MAZE_SCREEN_RATIO_[0])
        maze_screen_width = int(self._screen_.get_width() * self._MAZE_SCREEN_RATIO_[1])
        self.maze_screen_offset_y = self._MAZE_SCREEN_OFFSET_[0] * self._screen_.get_height()
        self.maze_screen_offset_x = self._MAZE_SCREEN_OFFSET_[1] * self._screen_.get_width()
        self._maze_screen_ = MazeView(maze, maze_screen_height, maze_screen_width)
        self._maze_screen_.add_to_parent(self._screen_, (self.maze_screen_offset_y, self.maze_screen_offset_x))

    def init_player(self, player, enemies_group):
        self._player_view_ = PlayerView(player)
        world_pos = convert_maze_to_world_pos(player.position[0], player.position[1])
        self._player_view_.add_to_parent(self._screen_, location=world_pos)
        self._enemies_view_ = enemies_group

    def init_bullets(self, bullets_group):
        self._bullets_ = bullets_group

    # @staticmethod
    # def convert_maze_to_world_pos(maze_x, maze_y):
    #     maze_screen_height = int(WIN_HEIGHT * MainGameView._MAZE_SCREEN_RATIO_[0])
    #     maze_screen_width = int(WIN_WIDTH * MainGameView._MAZE_SCREEN_RATIO_[1])
    #
    #     cell_height = int( maze_screen_height / MAP_HEIGHT)
    #     cell_width = int( maze_screen_width / MAP_WIDTH )
    #     world_x = (maze_x * cell_height + cell_height / 2)
    #     world_y = (maze_y * cell_width + cell_width / 2)
    #
    #     return world_x, world_y

    def init_score_board(self):
        pass

    def init_notification(self):
        pass

