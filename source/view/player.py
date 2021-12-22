import pygame

from source.config import *
from source.model.player import Player
from source.view.base_view import BaseView
from source.view.utils import convert_maze_to_world_pos
from source.view.spritesheet import SpriteSheet


class PlayerView(BaseView):
    TILE_WIDTH = 32
    TILE_HEIGHT = 32

    def __init__(self, player):
        self._player = player
        self.name = "Player"

        self.r = self._player.get_maze_radius() * (WIN_WIDTH / MAP_WIDTH) * 0.5
        super().__init__(self.r * 2, self.r * 2)

        self._image = None

        self.get_sprite()
        self._image = pygame.transform.scale(self._image, (self.r * 2, self.r * 2))

        self._add_child(self._image,
                        (int(self._screen_.get_height() / 2),
                         int(self._screen_.get_width() / 2)))


    def get_sprite(self):
        direction = self._player.get_current_direction()
        x = 0

        if self._player.is_main_player():
            x = 1 * self.TILE_WIDTH
        else:
            x = 0

        dim = (self.TILE_WIDTH, self.TILE_HEIGHT)

        if direction == UP:
            anchor = (x, 2 * self.TILE_HEIGHT)
        elif direction == DOWN:
            anchor = (x, 3 * self.TILE_HEIGHT)
        elif direction == LEFT:
            anchor = (x, 4 * self.TILE_HEIGHT)
        elif direction == RIGHT:
            anchor = (x, 5 * self.TILE_HEIGHT)

        self._image = SpriteSheet.image_at(anchor, dim, 'PLAYER', -1)

    def get_world_position(self):
        position = self._player.get_position()
        world_position = convert_maze_to_world_pos(position[0], position[1])
        return world_position

    def add_to_parent(self, parent: pygame.Surface, location=None, is_centered=None):
        self.get_sprite()
        self._image = pygame.transform.scale(self._image, (self.r * 2, self.r * 2))
        self._add_child(self._image,
                        (int(self._screen_.get_height() / 2),
                         int(self._screen_.get_width() / 2)))
        super().add_to_parent(parent, location, is_centered=True)
