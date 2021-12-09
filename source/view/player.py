import pygame
from pygame.locals import *
from source.config import *

from source.model.player import Player

class PlayerView:
    def __init__(self, player):
        self.player = player

        r = self.player.radius
        self._view_ = pygame.Surface((r * 2, r * 2))
        self._view_.fill(pygame.Color("black"))
        pygame.draw.circle(self._view_, pygame.Color("white"),
                            (int(self._view_.get_height() /2),
                            int(self._view_.get_width() /2)),
                            r)

    def add_to_parent(self, parent: pygame.Surface, location):
        parent.blit(self._view_, (location[0] - self._view_.get_width() / 2, location[1] - self._view_.get_height() /2))

