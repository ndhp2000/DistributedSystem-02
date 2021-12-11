from source.model.bullet import Bullet
import pygame


class BulletView:
    def __init__(self, bullet):
        self.bullet = bullet

        r = self.bullet.radius
        self._view_ = pygame.Surface((r * 2, r * 2))
        self._view_.fill(pygame.Color("black"))
        pygame.draw.circle(self._view_, pygame.Color("orange"),
                            (int(self._view_.get_width() /2),
                            int(self._view_.get_height() /2)),
                            r)
 
    def add_to_parent(self, parent: pygame.Surface, location):
        parent.blit(self._view_, location)

