import pygame

from source.view.components.base_view import BaseView
from source.utils.assets import MenuViewAsset
from source.config import *


class Button(BaseView):
    def __init__(self,  dim, text):
        self._background = pygame.image.load(MenuViewAsset.button_background).convert_alpha()
        self._text = text
        self._text_font = pygame.font.Font(MenuViewAsset.font, NAME_TAG_FONT_SIZE)
        self._size = dim
        super().__init__(dim[0], dim[1])
        self._screen_ = pygame.Surface(dim, pygame.SRCALPHA)
        self._background = pygame.transform.scale(self._background, (self._screen_.get_width(), self._screen_.get_height()))

    def add_to_parent(self, parent: pygame.Surface, location):
        text_surface = self._text_font.render(self._text, True, (255, 255, 255))
        text_location = (self._background.get_width() / 2, self._background.get_height() / 2)
        background_button_location = (self._background.get_width() / 2, self._background.get_height() / 2)

        self._background.blit(text_surface, text_surface.get_rect(center=text_location))
        self._screen_.blit(self._background, self._background.get_rect(center=background_button_location))
        parent.blit(self._screen_, self._screen_.get_rect(center=location))

    def get_rect(self, center=None):
        return self._screen_.get_rect(center=center)
