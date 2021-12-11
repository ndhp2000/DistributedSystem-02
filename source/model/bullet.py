import pygame
from source.config import *
from source.model.maze import Maze
from source.view.utils import convert_maze_to_world_pos
from source.utils.group import Group


class Bullet:
    def __init__(self, bullets_group, bullet_id, position, target, direction):
        self._group = {}
        self._position = position.copy()
        self._speed = 5
        self._id = bullet_id
        self._radius = 5
        self._direction = direction
        self._is_disable = False
        self._target = target
        self._player_id = 0

        bullets_group.add(self)
        self._group[bullets_group] = 0

    def move(self, dt):
        self.position += DIRECTIONS[self.direction] * self.speed * dt

        if self._meet_target(dt):
            self.remove()

    def _meet_target(self, dt):
        distance = np.linalg.norm(self.position - self.target)
        if distance < self.speed * dt * 0.55:
            return True
        return False

    def update(self, dt):
        self.move(dt)
