import pygame
from pygame.locals import *
from source.config import *
from source.model.player import Player
from source.view.base_view import BaseView
from source.view.utils import convert_maze_to_world_pos
from source.view.spritesheet import SpriteSheet


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
        self._image = None

        self.get_sprite()
        # pygame.draw.circle(self._screen_, color,
        #                     (int(self._screen_.get_height() /2),
        #                     int(self._screen_.get_width() /2)),
        #                     r)

        self._image = pygame.transform.scale(self._image, (r * 2, r * 2))
        self._add_child(self._image,
                        (int(self._screen_.get_height() /2),
                        int(self._screen_.get_width() /2)))

    def get_sprite(self):
        direction = self._player.get_current_direction()
        x = 0
        if self._player.is_main_player():
            x = 2
        else:
            x = 0

        if direction == UP:
            self._image = SpriteSheet.image_at(x, 4, -1)
        elif direction == DOWN:
            self._image = SpriteSheet.image_at(x, 6, -1)
        elif direction == LEFT:
            self._image = SpriteSheet.image_at(x, 8, -1)
        elif direction == RIGHT:
            self._image = SpriteSheet.image_at(x, 10, -1)

    def get_world_position(self):
        position = self._player.get_position()
        world_position = convert_maze_to_world_pos(position[0], position[1])
        return world_position

