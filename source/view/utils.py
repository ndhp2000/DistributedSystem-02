from source.config import *
import pygame

class BaseView:
    def __init__(self, screen_height, screen_width):
        self._screen_ = pygame.Surface((screen_width, screen_height), 0, 32)

    def _add_child_(self, child: pygame.Surface, location):
        self._screen_.blit(child, child.get_rect(center=location))