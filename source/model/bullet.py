import pygame
from source.config import *
from source.model.maze import Maze
from source.view.utils import convert_maze_to_world_pos
from source.model.entity_group import Group
from source.model.base_entity import Entity


class Bullet(Entity):
    def __init__(self, bullets_group, bullet_id, player_id, position, target, direction):
        super().__init__(BULLET_RADIUS, BULLET_MAZE_RADIUS, position, BULLET_MOVING_SPEED, direction)
        self._group = bullets_group
        self._id = bullet_id
        self._target = target
        self._player_id = player_id
        self._initial_position = self._position.copy()

        bullets_group.add(self)

    def remove(self):
        if self._group is not None:
            self._group.remove(self)

        self._is_removed = True

    def _move(self, dt):
        # print("BULLET MOVE")
        # print(self._position)
        # print(self._direction)
        # print(self._speed * dt)
        self._position += DIRECTIONS[self._direction] * self._speed * dt

        if self._meet_target(dt):
            self.remove()

    def _meet_target(self, dt):
        distance_from_start = np.linalg.norm(self._position - self._initial_position)
        start_to_target = np.linalg.norm(self._target - self._initial_position)

        return start_to_target <= distance_from_start

    def update(self, dt):
        self._move(dt)

    def get_origin_id(self):
        return self._player_id

    def is_out_of_range(self):
        if self._is_removed:
            return True

        distance = np.linalg.norm(self._position - self._initial_position)
        return distance > COOLDOWN_RANGE
