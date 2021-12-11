import pygame
from source.config import *
from source.model.maze import Maze
from source.view.utils import convert_maze_to_world_pos
from source.utils.group import Group

class Bullet:
    def __init__(self, bullets_group, id, position, target, direction):
        self._group = {}
        self.position = position.copy()
        self.speed = 5
        self.id = id
        self.radius = 5
        self.direction = direction
        self.is_disable = False
        self.target = target
        self.player_id = 0

        bullets_group.add(self)
        self._group[bullets_group] = 0

    def move(self, dt):
        self.position += DIRECTIONS[self.direction] * self.speed * dt

        if self.meet_target(dt):
            self.remove()
        else:
            world_position = convert_maze_to_world_pos(self.position[0], self.position[1])
            self.rect = self.image.get_rect(center=world_position)

    def is_out_screen(self):
        if self.position[0] < 0 or self.position[0] > MAP_WIDTH:
            return True
        if self.position[1] < 0 or self.position[1] > MAP_HEIGHT:
            return True
        return False

    def meet_target(self, dt):
        distance = np.linalg.norm(self.position - self.target)
        if distance < self.speed * dt * 0.55:
            return True
        return False

    def update(self, dt):
        self.move(dt)
