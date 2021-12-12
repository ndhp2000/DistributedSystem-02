import pygame

from source.config import *
from source.model.bullet import Bullet
from source.model.maze import Maze
from source.model.utils import convert_player_direction_to_maze_direction
from source.view.utils import convert_maze_to_world_pos
from source.model.base_entity import Entity


class Player(Entity):
    def __init__(self, position, maze: Maze, player_id=0):
        super().__init__(PLAYER_RADIUS, position, PLAYER_MOVING_SPEED, None)
        self._maze_ = maze
        self._id = player_id
        self._hp = PLAYER_HP
        self._previous_anchor = position.copy()
        self._next_anchor = None
        self._current_direction = None
        self._recent_running_bullet = None

        for direction in DIRECTIONS:
            if self._get_next_anchor(position, direction) is not None:
                print(self._get_next_anchor(position, direction))
                self._next_anchor = self._get_next_anchor(position, direction)
                self._current_direction = direction
                break
        self._next_direction = None
        print(self._current_direction, self._next_direction, self._previous_anchor, self._next_anchor)

    def _set_next_direction(self, input_direction):
        self._next_direction = input_direction

    def _meet_next_anchor(self):
        if self._next_anchor is not None and self._previous_anchor is not None:
            distance_between_anchors = np.sum(np.abs(self._next_anchor - self._previous_anchor))
            distance_to_position = np.sum(np.abs(self._position - self._previous_anchor))
            # print("distance = ", distance_to_position)
            return distance_to_position >= distance_between_anchors
        return False

    def _move(self, dt):
        # print("CALL UPDATE")
        self._position += DIRECTIONS[self._current_direction] * self._speed * dt

        if self._meet_next_anchor():
            # print("MEET AN ANCHOR")
            # print('Position: ', self._position)
            # print('Direction: ', self._current_direction, self._next_direction)
            # print('Anchor: ', self._previous_anchor, self._next_anchor)
            self._position = self._next_anchor.copy()  # TODO: Add delta
            if self._next_direction and self._is_valid_direction(self._next_direction):
                # print("CHANGE DIRECTION FOR INPUT")
                # Check new input direction
                self._previous_anchor = self._next_anchor
                self._next_anchor = self._get_next_anchor(self._previous_anchor, self._next_direction)
                self._current_direction = self._next_direction
            elif self._is_valid_direction(self._current_direction):  # Use current - direction
                # print("MOVE SAME DIRECTION")
                self._previous_anchor = self._next_anchor
                self._next_anchor = self._get_next_anchor(self._previous_anchor, self._current_direction)
            self._next_direction = None
            # print('Position: ', self._position)
            # print('Direction: ', self._current_direction, self._next_direction)
            # print('Anchor: ', self._previous_anchor, self._next_anchor)

        if self._next_direction == -self._current_direction:
            # print("MOVE REVERSE DIRECTION")
            # print('Position: ', self._position)
            # print('Direction: ', self._current_direction, self._next_direction)
            # print('Anchor: ', self._previous_anchor, self._next_anchor)
            self._reverse_direction()
            self._next_direction = None
            # print('Position: ', self._position)
            # print('Direction: ', self._current_direction, self._next_direction)
            # print('Anchor: ', self._previous_anchor, self._next_anchor)

    def _reverse_direction(self):
        self._current_direction = self._current_direction * -1
        self._previous_anchor, self._next_anchor = self._next_anchor, self._previous_anchor

    def _is_valid_direction(self, player_direction):
        maze_direction = convert_player_direction_to_maze_direction(player_direction)
        return self._maze_.is_connected_to_direction((int(self._position[1]), int(self._position[0])), maze_direction)

    def _get_next_anchor(self, pos, player_direction):
        direction = convert_player_direction_to_maze_direction(player_direction)
        if self._maze_.is_connected_to_direction((int(pos[1]), int(pos[0])), direction):
            # print("GET NEXT ANCHOR ", pos, direction)
            return np.array([pos[0] + Maze.DELTA[direction][1], pos[1] + Maze.DELTA[direction][0]])
        else:
            return None

    def set_position(self, pos):
        self._position = pos.copy()

    def get_radius(self):
        return self._radius

    def get_position(self):
        return self._position.copy()

    def update(self, event, dt, bullets_group):
        if event in PLAYER_MOVEMENT:
            self._set_next_direction(event)
        elif event in PLAYER_SHOOT:
            self.shoot(bullets_group)
        self._move(dt)

    def get_bullet_target(self):
        cell_pos = np.array([int(self._position[0]), int(self._position[1])])

        direction = convert_player_direction_to_maze_direction(self._current_direction)
        while self._maze_.is_connected_to_direction((cell_pos[1], cell_pos[0]), direction):
            cell_pos += DIRECTIONS[self._current_direction]

        if np.array_equal(cell_pos, self._position):
            return None
        return cell_pos

    def shoot(self, bullets_group):


        # print("SHOOT")
        # print(len(bullets_group))
        # print(self._position)
        # print(target)
        # print(self._current_direction)

        if self._recent_running_bullet is None or self._recent_running_bullet.is_out_of_range():
            target = self.get_bullet_target()

            if target is None:
                return

            bullet = Bullet(bullets_group, 0, self._position, target, self._current_direction)
            self._recent_running_bullet = bullet

    def hit(self, damage):
        print(self.name, 'hit')

