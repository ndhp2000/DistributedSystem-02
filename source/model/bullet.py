import pygame
from source.config import *
from source.model.maze import Maze
from source.view.utils import convert_maze_to_world_pos
from source.utils.group import Group


class Bullet:
    def __init__(self, bullets_group, bullet_id, position, target, direction):
        self._group = {}
        self._position = position.copy()
        self._speed = BULLET_MOVING_SPEED
        self._id = bullet_id
        self._radius = BULLET_RADIUS
        self._direction = direction
        self._is_disable = False
        self._target = target
        self._player_id = 0

        bullets_group.add(self)
        self._group[bullets_group] = 0

    def _remove(self):
        for group in self._group:
            group.remove(self)

    def _move(self, dt):
        # print("BULLET MOVE")
        # print(self._position)
        # print(self._direction)
        # print(self._speed * dt)
        self._position += DIRECTIONS[self._direction] * self._speed * dt

        if self._meet_target(dt):
            self._remove()

    def _meet_target(self, dt):
        distance = np.linalg.norm(self._position - self._target)
        if distance < self._speed * dt * 0.55: # TODO: check ds of bullet
            return True
        return False

    def update(self, dt):
        self._move(dt)

    def get_radius(self):
        return self._radius

    def get_position(self):
        return self._position.copy()
