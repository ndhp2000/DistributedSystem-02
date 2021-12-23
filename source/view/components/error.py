import pygame.font

from source.config import *


class Error:
    def __init__(self, text):
        self._text = text
        self._text_font = pygame.font.SysFont('notomono', NAME_TAG_FONT_SIZE)
        color = pygame.Color('red')
        self._text_surface = self._text_font.render(self._text, True, color)

    def add_to_parent(self, parent: pygame.Surface, location=None, is_centered=None):
        text_location = (self._text_surface.get_width() / 2, self._text_surface.get_height() / 2)
        parent.blit(self._text_surface, self._text_surface.get_rect(center=text_location))