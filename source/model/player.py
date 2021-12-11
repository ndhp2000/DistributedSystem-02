import pygame
from pygame.locals import *
from source.model.bullet import Bullet
import numpy as np
from source.config import *
from source.model.maze import Maze

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, bullets_group, adj_matrix, id=0):
        pygame.sprite.Sprite.__init__(self)
        self._id = id
        self._hp = 10
        self._speed = 1
        self._action = STOP
        self._bullets = []
        self._target = pos.copy()
        self._previous_target = None
        self._maze_map = adj_matrix
        self._bullets_group = bullets_group
        self.clock = pygame.time.Clock()

        self.future_change_direction = STOP
        self.direction = STOP
        self.position = pos
        self.radius = 15

    def set_position(self, pos):
        self.position = pos.copy()

    def update(self, event, dt):
        if event in PLAYER_MOVEMENT:
            self.move(event, dt)
            return

        if event in PLAYER_SHOOT:
            self.shoot()

        self.move(None, dt)

    def move(self, direction, dt):
        if direction is not None:
            self.future_change_direction = direction

        if self.direction == STOP and self.future_change_direction == STOP:
            return

        if self.direction == STOP and self.future_change_direction != STOP:
            if self.is_valid_direction(self.future_change_direction):
                self.direction = self.future_change_direction
                self._previous_target = self._target
            else:
                self.future_change_direction = STOP
                return

        self.position += DIRECTIONS[self.direction] * self._speed * dt

        if self.meet_target():
            # check new input direction
            if self.is_valid_direction(self.future_change_direction):
                self._previous_target = self._target
                self._target = self.get_next_target(self._previous_target, self.future_change_direction)
                self.direction = self.future_change_direction

            # if new input direction is not valid use older direction:
            elif self.is_valid_direction(self.direction):
                self._previous_target = self._target
                self._target = self.get_next_target(self._previous_target, self.direction)

            # if older direction lead to deadend => stop
            else:
                self.direction = STOP
                self.future_change_direction = STOP

        else:
            if self.future_change_direction == -self.direction:
                self.reverse_direction()

    def reverse_direction(self):
        self.direction *= -1
        temp = self._previous_target
        self._previous_target = self._target
        self._target = temp

    def is_valid_direction(self, player_direction):
        maze_direction = None
        if player_direction == UP:
            maze_direction = Maze.DIRECTION_UP
        if player_direction == DOWN:
            maze_direction = Maze.DIRECTION_DOWN
        if player_direction == LEFT:
            maze_direction = Maze.DIRECTION_LEFT
        if player_direction == RIGHT:
            maze_direction = Maze.DIRECTION_RIGHT
        if player_direction == STOP:
            return True

        if self._maze_map[int(self.position[1]), int(self.position[0]), maze_direction] == 0:
            return False
        return True

    def meet_target(self):
        if self._previous_target is None:
            return False

        if (self._target != self._previous_target).any():
            distance_target = np.sum(np.square(self._previous_target - self._target))
            self_previous = np.sum(np.square(self._previous_target - self.position))

            return self_previous >= distance_target
        else:
            return True

    def get_next_target(self, pos, player_direction):
        if player_direction == STOP:
            return np.array([pos[0], pos[1]])

        direction = Maze.convert_player_direction_2_maze(player_direction)
        if self._maze_map[int(pos[1]), int(pos[0]), direction] == 1:
            new_pos = (-1, -1)
            if direction == Maze.DIRECTION_UP:
                new_pos = (pos[0], pos[1] - 1)
            elif direction == Maze.DIRECTION_DOWN:
                new_pos = (pos[0], pos[1] + 1)
            elif direction == Maze.DIRECTION_LEFT:
                new_pos = (pos[0] - 1, pos[1])
            elif direction == Maze.DIRECTION_RIGHT:
                new_pos = (pos[0] + 1, pos[1])
            return np.array([new_pos[0], new_pos[1]])
        else:
            return np.array([pos[0], pos[1]])

    def get_bullet_target(self):
        cell_pos = np.array([int(self.position[0]), int(self.position[1])])

        if self.direction == STOP:
            return None
        direction = Maze.convert_player_direction_2_maze(self.direction)
        while self._maze_map[cell_pos[1], cell_pos[0], direction] == 1:
            cell_pos += DIRECTIONS[self.direction]
        return cell_pos

    def shoot(self):
        target = self.get_bullet_target()

        if target is None:
            return

        bullet = Bullet(self._bullets_group, 0, self.position, target, self.direction)

    def collision_bullet(self):
        pass

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, bullets_group, adj_matrix, id=0):
        pygame.sprite.Sprite.__init__(self)
        self._id = id
        self._hp = 10
        self._speed = 1
        self._action = STOP
        self._bullets = []
        self._target = pos.copy()
        self._previous_target = None
        self._maze_map = adj_matrix
        self._bullets_group = bullets_group
        self.clock = pygame.time.Clock()

        self.future_change_direction = STOP
        self.direction = STOP
        self.position = pos
        self.radius = 15

    def set_position(self, pos):
        self.position = pos.copy()

    def update(self, event, dt):
        if event in PLAYER_MOVEMENT:
            self.move(event, dt)
            return

        if event in PLAYER_SHOOT:
            self.shoot()

        self.move(None, dt)

    def move(self, direction, dt):
        if direction is not None:
            self.future_change_direction = direction

        if self.direction == STOP and self.future_change_direction == STOP:
            return

        if self.direction == STOP and self.future_change_direction != STOP:
            if self.is_valid_direction(self.future_change_direction):
                self.direction = self.future_change_direction
                self._previous_target = self._target
            else:
                self.future_change_direction = STOP
                return

        self.position += DIRECTIONS[self.direction] * self._speed * dt

        if self.meet_target():
            # check new input direction
            if self.is_valid_direction(self.future_change_direction):
                self._previous_target = self._target
                self._target = self.get_next_target(self._previous_target, self.future_change_direction)
                self.direction = self.future_change_direction

            # if new input direction is not valid use older direction:
            elif self.is_valid_direction(self.direction):
                self._previous_target = self._target
                self._target = self.get_next_target(self._previous_target, self.direction)

            # if older direction lead to deadend => stop
            else:
                self.direction = STOP
                self.future_change_direction = STOP

        else:
            if self.future_change_direction == -self.direction:
                self.reverse_direction()

    def reverse_direction(self):
        self.direction *= -1
        temp = self._previous_target
        self._previous_target = self._target
        self._target = temp

    def is_valid_direction(self, player_direction):
        maze_direction = None
        if player_direction == UP:
            maze_direction = Maze.DIRECTION_UP
        if player_direction == DOWN:
            maze_direction = Maze.DIRECTION_DOWN
        if player_direction == LEFT:
            maze_direction = Maze.DIRECTION_LEFT
        if player_direction == RIGHT:
            maze_direction = Maze.DIRECTION_RIGHT
        if player_direction == STOP:
            return True

        if self._maze_map[int(self.position[1]), int(self.position[0]), maze_direction] == 0:
            return False
        return True

    def meet_target(self):
        if self._previous_target is None:
            return False

        if (self._target != self._previous_target).any():
            distance_target = np.sum(np.square(self._previous_target - self._target))
            self_previous = np.sum(np.square(self._previous_target - self.position))

            return self_previous >= distance_target
        else:
            return True

    def get_next_target(self, pos, player_direction):
        if player_direction == STOP:
            return np.array([pos[0], pos[1]])

        direction = Maze.convert_player_direction_2_maze(player_direction)
        if self._maze_map[int(pos[1]), int(pos[0]), direction] == 1:
            new_pos = (-1, -1)
            if direction == Maze.DIRECTION_UP:
                new_pos = (pos[0], pos[1] - 1)
            elif direction == Maze.DIRECTION_DOWN:
                new_pos = (pos[0], pos[1] + 1)
            elif direction == Maze.DIRECTION_LEFT:
                new_pos = (pos[0] - 1, pos[1])
            elif direction == Maze.DIRECTION_RIGHT:
                new_pos = (pos[0] + 1, pos[1])
            return np.array([new_pos[0], new_pos[1]])
        else:
            return np.array([pos[0], pos[1]])

    def get_bullet_target(self):
        cell_pos = np.array([int(self.position[0]), int(self.position[1])])

        if self.direction == STOP:
            return None
        direction = Maze.convert_player_direction_2_maze(self.direction)
        while self._maze_map[cell_pos[1], cell_pos[0], direction] == 1:
            cell_pos += DIRECTIONS[self.direction]
        return cell_pos

    def shoot(self):
        target = self.get_bullet_target()

        if target is None:
            return

        bullet = Bullet(self._bullets_group, 0, self.position, target, self.direction)

    def collision_bullet(self):
        pass

# class Player(Entity):
#     def __init__(self, pos, bullets_group, adj_matrix, id=0):
#         super.__init__()

class Enemy:
    def __init__(self):
        pass

