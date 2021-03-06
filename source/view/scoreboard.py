import pygame

from source.utils.assets import MazeViewAsset
from source.config import NAME_TAG_FONT_SIZE, CONSOLE_FONT_SIZE
from source.model.entity_group import PlayerGroup
from source.view.components.base_view import BaseView


class ScoreboardView(BaseView):
    NAME_TAG_HEIGHT_RATIO = 1 / 4
    COLUMNS_WIDTH_RATIO = [2 / 7, 2 / 7, 2 / 7]
    COLUMNS_WIDTH_OFFSET = [1 / 14, 5 / 14, 9 / 14]
    COLUMNS_HEIGHT_RATIO = 1 / 10

    def __init__(self, screen_height, screen_width, players_logic: PlayerGroup):
        super().__init__(screen_height, screen_width)
        self._players_logic_ = players_logic
        self._name_tag_font_ = pygame.font.SysFont('notomono', NAME_TAG_FONT_SIZE)
        self._text_font_ = pygame.font.SysFont('notomono', CONSOLE_FONT_SIZE)
        self._draw_borders_()

    def _print_(self, text, row, col, set_special=False):
        if set_special:
            color = (255, 0, 0)
        else:
            color = (255, 255, 255)
        text_surface = self._text_font_.render(text, True, color)
        x = self._screen_.get_width() * (self.COLUMNS_WIDTH_OFFSET[col] + self.COLUMNS_WIDTH_RATIO[1] / 2)
        y = self._screen_.get_height() * (
                self.NAME_TAG_HEIGHT_RATIO + self.COLUMNS_HEIGHT_RATIO * row + self.COLUMNS_HEIGHT_RATIO / 2)
        self._add_child(text_surface, (x, y))

    def _draw_borders_(self):
        vertical_line = pygame.image.load(MazeViewAsset.vertical_line).convert_alpha()
        vertical_line = pygame.transform.scale(vertical_line,
                                               (vertical_line.get_width() * 0.2, self._screen_.get_height()))
        horizontal_line = pygame.image.load(MazeViewAsset.horizontal_line).convert_alpha()
        horizontal_line = pygame.transform.scale(horizontal_line,
                                                 (self._screen_.get_width(), horizontal_line.get_height() * 0.1))
        maze_tile = pygame.image.load(MazeViewAsset.maze_tile).convert_alpha()
        maze_tile = pygame.transform.scale(maze_tile, (self._screen_.get_width(), self._screen_.get_height()))
        maze_tile.set_alpha(128)

        self._add_child(maze_tile, (self._screen_.get_width() / 2, self._screen_.get_height() / 2))
        self._add_child(vertical_line, (vertical_line.get_width() / 2, self._screen_.get_height() / 2))
        self._add_child(vertical_line,
                        (self._screen_.get_width() - vertical_line.get_width() / 2, self._screen_.get_height() / 2))
        self._add_child(horizontal_line, (self._screen_.get_width() / 2, horizontal_line.get_height() / 2))

        name_tag = self._name_tag_font_.render('SCOREBOARD', True, (255, 255, 255))
        self._add_child(name_tag, (self._screen_.get_width() / 2, self._screen_.get_height() *
                                   self.NAME_TAG_HEIGHT_RATIO / 2))

        self._print_("NAME", 0, 0)
        self._print_("SCORE", 0, 1)
        self._print_("TYPE", 0, 2)

    def reload_scoreboard(self):
        self._clear_view()
        self._draw_borders_()
        scoreboard = self._players_logic_.get_scores()
        for row, record in enumerate(scoreboard):
            self._print_(str(record[0]), row + 1, 0, record[3])
            self._print_(str(record[1]), row + 1, 1, record[3])
            self._print_(str(record[2]), row + 1, 2, record[3])
