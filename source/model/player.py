import random

from source.config import *
from source.model.base_entity import Entity
from source.model.bullet import Bullet
from source.model.maze import Maze
from source.model.utils import convert_player_direction_to_maze_direction


class Player(Entity):
    def __init__(self, position, maze: Maze, player_id, players_group=None):
        super().__init__(PLAYER_RADIUS, position, PLAYER_MOVING_SPEED, None)
        self._maze_ = maze
        self._id = player_id
        self._hp = PLAYER_HP
        self._previous_anchor = position.copy()
        self._next_anchor = None
        self._current_direction = None
        self._recent_running_bullet = None
        self._player_type = 'human'
        self._group = players_group

        for direction in DIRECTIONS:
            if self._get_next_anchor(position, direction) is not None:
                print(self._get_next_anchor(position, direction))
                self._next_anchor = self._get_next_anchor(position, direction)
                self._current_direction = direction
                break
        self._next_direction = None
        print(self._current_direction, self._next_direction, self._previous_anchor, self._next_anchor)

    def _remove(self):
        if self._group is not None:
            self._group.remove(self)

        self._is_removed = True

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
            return np.array([pos[0] + Maze.DELTA[direction][1], pos[1] + Maze.DELTA[direction][0]])
        else:
            return None

    def set_position(self, pos):
        self._position = pos.copy()

    def get_origin_id(self):
        return self._id

    def get_id(self):
        return self._id

    def get_hp(self):
        return self._hp

    def get_player_type(self):
        return self._player_type

    def update(self, event, dt, bullets_group):
        if event in PLAYER_MOVEMENT:
            self._set_next_direction(event)
        elif event in PLAYER_SHOOT:
            self.shoot(bullets_group)
        self._move(dt)

    def _get_bullet_target(self):
        target_cell_pos = np.array([int(self._position[0]), int(self._position[1])])

        maze_direction = convert_player_direction_to_maze_direction(self._current_direction)
        while self._maze_.is_connected_to_direction((target_cell_pos[1], target_cell_pos[0]), maze_direction):
            target_cell_pos += DIRECTIONS[self._current_direction]

        if np.array_equal(target_cell_pos, self._position):
            return None
        return target_cell_pos

    def shoot(self, bullets_group):
        #print(self._recent_running_bullet)
        if self._recent_running_bullet is None or self._recent_running_bullet.is_out_of_range():
            target = self._get_bullet_target()
            if target is None:
                return

            print('SHOOT')
            print(len(bullets_group))
            print(self._id)
            print('\n')
            bullet = Bullet(bullets_group, 0, self._id, self._position, target, self._current_direction)
            self._recent_running_bullet = bullet

    def hit(self, damage):
        print('Player 1', 'hit')


class Bot(Player):
    COOLDOWN_COMMAND = 20

    def __init__(self, position, maze: Maze, player_id):
        super().__init__(position, maze, player_id)
        self._counter = self.COOLDOWN_COMMAND
        self._player_type = 'machine'

    def update(self, event, dt, bullets_group):  # Upgrade later
        event = self.create_command()
        if event in PLAYER_MOVEMENT:
            self._set_next_direction(event)
        elif event in PLAYER_SHOOT:
            self.shoot(bullets_group)
        self._move(dt)

    def create_command(self):
        self._counter -= 1
        if self._counter == 0:
            self._counter = self.COOLDOWN_COMMAND
            rand_num = random.randint(-N_TYPE_COMMANDS, N_TYPE_COMMANDS - 1)  # TODO UPDATE FOR BACKEND
            if rand_num < 0:
                return SHOOT
            else:
                return list(PLAYER_MOVEMENT.keys())[rand_num - 1]
        return None
