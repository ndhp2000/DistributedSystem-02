from source.config import WIN_WIDTH, MAP_WIDTH
from source.model.bullet import Bullet
import pygame
from source.view.components.base_view import BaseView
from source.view.utils import convert_maze_to_world_pos


class BulletView(BaseView):
    def __init__(self, bullet: Bullet):
        self._bullet = bullet
        self._group = {}
        self.name = "Bullet"

        r = self._bullet.get_maze_radius() * (WIN_WIDTH / MAP_WIDTH)

        super().__init__(r * 2, r * 2)

        self._screen_.fill(pygame.Color("white"))
        pygame.draw.circle(self._screen_, pygame.Color("orange"),
                           (int(self._screen_.get_width() / 2),
                            int(self._screen_.get_height() / 2)),
                           r)

    def get_world_position(self):
        position = self._bullet.get_position()
        world_position = convert_maze_to_world_pos(position[0], position[1])
        return world_position
