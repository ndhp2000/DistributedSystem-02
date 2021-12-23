import pygame

from source.config import CONSOLE_FONT_SIZE
from source.model.notification import Notification
from source.view.base_view import BaseView


class NotificationView(BaseView):
    NAME_TAG_HEIGHT_RATIO = 1 / 5
    N_LOG_ROWS = 12
    COLUMNS_HEIGHT_RATIO = 1 / N_LOG_ROWS
    ROWS_PADDING_RATIO = 1 / 20
    TEXT_PREFIX = "$maze-game: "

    def __init__(self, screen_height, screen_width, notification: Notification):
        super().__init__(screen_height, screen_width)
        self._notification_ = notification
        self._text_font_ = pygame.font.SysFont('notomono', CONSOLE_FONT_SIZE)
        self._text_list_ = []

    def _print_row_(self, text, row):
        text_surface = self._text_font_.render(self.TEXT_PREFIX + text, True, (255, 255, 255))
        x = text_surface.get_width() / 2
        y = self._screen_.get_height() * (self.COLUMNS_HEIGHT_RATIO * row + self.COLUMNS_HEIGHT_RATIO / 2)
        self._add_child(text_surface, (x, y))

    def print(self, text=None):
        if text == 'None':
            return
        self._text_list_.append(text)
        if len(self._text_list_) <= self.N_LOG_ROWS:
            self._print_row_(text, len(self._text_list_) - 1)
        else:
            self._text_list_ = self._text_list_[1:]
            self._clear_view()

            for row, text in enumerate(self._text_list_):
                self._print_row_(text, row)

    def reload(self):
        for message in self._notification_.get_messages():
            self.print(message)
        self._notification_.clear()
