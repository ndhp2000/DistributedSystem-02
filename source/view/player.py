import pygame
from pygame.locals import *
from source.config import *
from source.model.player import Player
from source.view.base_view import BaseView
from source.view.utils import convert_maze_to_world_pos


class PlayerView(BaseView):
    def __init__(self, player):
        self._player = player
        self.name = "Player"

        r = self._player.get_radius()
        if self._player.is_main_player():
            color = pygame.Color("green")
        else:
            color = pygame.Color("red")

        super().__init__(r * 2, r * 2)
        self._screen_.fill(pygame.Color("black"))
        pygame.draw.circle(self._screen_, color,
                            (int(self._screen_.get_height() /2),
                            int(self._screen_.get_width() /2)),
                            r)

    def get_world_position(self):
        position = self._player.get_position()
        world_position = convert_maze_to_world_pos(position[0], position[1])
        return world_position

