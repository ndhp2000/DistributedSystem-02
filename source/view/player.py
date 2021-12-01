import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from bullet import Bullet

from ..model import Player

class PlayerView:
    def __init__(self):
        self.player = Player()

        r = self.player.radius
        self._view_ = pygame.Surface((r * 2, r * 2))
        self._view_.fill(pygame.Color("white"))
        pygame.draw.circle(self._view_, pygame.Color("black"),
                            (int(self._view_.get_width() /2),
                            int(self._view_.get_height() /2)),
                            r)

    def update(self, dt):
        pass

    def add_to_parent(self, parent: pygame.Surface, location):
        parent.blit(self._view_, location)
