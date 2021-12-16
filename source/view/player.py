import pygame

from source.config import *
from source.model.player import Player
from source.view.base_view import BaseView
from source.view.utils import convert_maze_to_world_pos
from source.view.spritesheet import SpriteSheet


class PlayerView(BaseView):
    def __init__(self, player: Player):
        self._player = player
        self.name = "Player"
        r = self._player.get_maze_radius() * (WIN_WIDTH / MAP_WIDTH) * 0.5
        super().__init__(r * 2, r * 2)
        self._screen_.fill(pygame.Color("black"))

        self._image = None
        self._name_tag_font_ = pygame.font.SysFont('notomono', PLAYER_TAG_FONT_SIZE)

        self.get_sprite()
        self._image = pygame.transform.scale(self._image, (r * 2, r * 2))
        self._add_child(self._image,
                        (int(self._screen_.get_height() / 2),
                         int(self._screen_.get_width() / 2)))

        text_location = (0, 0)
        self._text_surface = self._name_tag_font_.render(f'P{self._player.get_id()}', True, (255, 255, 255))
        self._add_child(self._text_surface, (text_location[0], text_location[1]))

    def get_sprite(self):
        direction = self._player.get_current_direction()
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
