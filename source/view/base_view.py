import pygame


class BaseView:
    def __init__(self, screen_height, screen_width):
        self._screen_ = pygame.Surface((screen_width, screen_height), 0, 32)

    def _clear_view(self):
        self._screen_.fill((0, 0, 0))

    def _add_child(self, child: pygame.Surface, location):
        self._screen_.blit(child, child.get_rect(center=location))

    def add_to_parent(self, parent: pygame.Surface, location):
        parent.blit(self._screen_, location)
