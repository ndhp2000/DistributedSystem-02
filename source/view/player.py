import pygame
from pygame.locals import *
from source.config import *
from source.model.player import Player
from

from source.view.utils import convert_maze_to_world_pos


class PlayerView(BaseView):
    def __init__(self, player):
        self.player = player

        r = self.player.radius
        self._view_ = pygame.Surface((r * 2, r * 2))
        self._view_.fill(pygame.Color("black"))
        pygame.draw.circle(self._view_, pygame.Color("white"),
                            (int(self._view_.get_height() /2),
                            int(self._view_.get_width() /2)),
                            r)

    def get_world_position(self):
        world_pos = convert_maze_to_world_pos(self.player.position[0], self.player.position[1])
        return world_pos

    def add_to_parent(self, parent: pygame.Surface):
        parent.blit(self._view_, (location[0] - self._view_.get_width() / 2, location[1] - self._view_.get_height() /2))

