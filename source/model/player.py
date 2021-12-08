import pygame
from pygame.locals import *
from source.model.bullet import Bullet
import numpy as np
from source.config import *
from source.model.maze import Maze

class Player:
    def __init__(self, pos, adj_matrix, id=0):
        self._id = id
        self._hp = 10
        self._speed = 1
        self._action = STOP
        self._bullets = []
        self._target = None
        self._previous_target = pos.copy()
        self._maze_map = adj_matrix

        self.future_change_direction = STOP
        self.direction = STOP
        self.position = pos
        self.radius = 15

    # def pre_move(self, event_type=None, dt=1):
    #     position = self.position
    #     if event_type is None:
    #         position += DIRECTIONS[self.direction] * self.speed * dt
    #         return position
    #
    #     if self.direction == STOP:
    #         position += DIRECTIONS[event_type] * self.speed * dt
    #
    #     if abs(event_type) == abs(self.direction):
    #         position += DIRECTIONS[event_type] * self.speed * dt
    #     elif event_type == STOP:
    #         pass
    #
    #     return position

    # def move(self, pos, event_type=None):
    #     if self.direction == STOP:
    #         self.direction = event_type
    #     if event_type == -self.direction:
    #         self.direction = event_type
    #     elif event_type == STOP:
    #         self.action = STOP
    #
    #     self.position = pos

    def set_position(self, pos):
        self.position = pos.copy()

    def move(self, direction, dt):
        self.position += DIRECTIONS[self.direction] * self._speed * dt
        self.future_change_direction = direction

        if self.meet_target():
            self._previous_target = self._target
            self._target = self.get_next_target(self._previous_target, direction)

            if (self._target != self._previous_target).any():
                self.direction = direction
            else:
                self._target = self.get_next_target(self.position, self.direction)

            if (self._target == self._previous_target).all():
                self.direction = STOP
            self.set_position(self._previous_target)
        else:
            if self.is_opposite_direction(direction):
                self.reverse_direction()

    def is_opposite_direction(self, direction):
        if (direction == -self.direction):
            self.direction *= -1
            temp = self._previous_target
            self._previous_target = self._target
            self._target = temp

    def meet_target(self):
        if self._target == self.:
            distance2Target = np.sum(np.square(self._previous_target - self._target))
            self2Previous = np.sum(np.square(self._previous_target - self.position))

            return self2Previous >= distance2Target
        return False

    def get_next_target(self, pos, player_direction):
        if player_direction == STOP:
            return np.array([pos[0], pos[1]])

        direction = Maze.convert_player_direction_2_maze(player_direction)
        if self._maze_map[int(pos[0]), int(pos[1]), direction] == 1:
            new_pos = (-1, -1)
            if direction == Maze.DIRECTION_UP:
                new_pos = (pos[0] - 1, pos[1])
            elif direction == Maze.DIRECTION_DOWN:
                new_pos = (pos[0] + 1, pos[1])
            elif direction == Maze.DIRECTION_LEFT:
                new_pos = (pos[0], pos[1] - 1)
            elif direction == Maze.DIRECTION_RIGHT:
                new_pos = (pos[0], pos[1] + 1)
            return np.array([new_pos[0], new_pos[1]])
        else:
            return np.array([pos[0], pos[1]])

    def shoot(self):
        bullet = Bullet(self.position, self.bullet_direction)
        return bullet

    def collision_bullet(self):
        pass