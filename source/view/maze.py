import pygame

from source.view.components.base_view import BaseView
from source.utils.assets import MazeViewAsset
from ..model.maze import Maze


class MazeView(BaseView):

    def __init__(self, maze: Maze, screen_height, screen_width):
        super().__init__(screen_height, screen_width)
        self._maze_ = maze
        self._box_length_ = int(self._screen_.get_height() / self._maze_.get_height())
        self._vertical_line = pygame.image.load(MazeViewAsset.vertical_line).convert_alpha()
        self._horizontal_line = pygame.image.load(MazeViewAsset.horizontal_line).convert_alpha()
        self._maze_tile = pygame.image.load(MazeViewAsset.maze_tile).convert_alpha()
        self._draw_maze_()

    def _draw_maze_(self):
        vertical_line = pygame.transform.scale(self._vertical_line,
                                               (self._box_length_ * 0.2, self._box_length_))
        horizontal_line = pygame.transform.scale(self._horizontal_line,
                                                 (self._box_length_, self._box_length_ * 0.2))
        maze_tile = pygame.transform.scale(self._maze_tile, (self._box_length_, self._box_length_))
        maze_tile.set_alpha(200)
        for x in range(self._maze_.get_width()):
            for y in range(self._maze_.get_height()):
                location = (
                    x * self._box_length_ + self._box_length_ / 2, y * self._box_length_ + self._box_length_ / 2)
                self._add_child(maze_tile, location)

        y = 0
        for x in range(self._maze_.get_width()):
            location = (x * self._box_length_ + self._box_length_ / 2, y * self._box_length_)
            self._add_child(horizontal_line, location)

        y = self._maze_.get_height()
        for x in range(self._maze_.get_width()):
            location = (x * self._box_length_ + self._box_length_ / 2, y * self._box_length_)
            self._add_child(horizontal_line, location)

        for y in range(self._maze_.get_height()):
            x = 0
            location = (x * self._box_length_, y * self._box_length_ + self._box_length_ / 2)
            self._add_child(vertical_line, location)
            x = self._maze_.get_width()
            location = (x * self._box_length_, y * self._box_length_ + self._box_length_ / 2)
            self._add_child(vertical_line, location)

        for y in range(self._maze_.get_height()):
            for x in range(self._maze_.get_width()):
                if not self._maze_.is_connected_to_direction((y, x), self._maze_.DIRECTION_RIGHT):
                    location = ((x + 1) * self._box_length_, y * self._box_length_ + self._box_length_ / 2)
                    self._add_child(vertical_line, location)

                if not self._maze_.is_connected_to_direction((y, x), self._maze_.DIRECTION_DOWN):
                    location = (x * self._box_length_ + self._box_length_ / 2, (y + 1) * self._box_length_)
                    self._add_child(horizontal_line, location)
