import pygame

from source.config import *
from source.model.bullet import Bullet
from source.model.maze import Maze
from source.model.utils import convert_player_direction_to_maze_direction
from source.view.utils import convert_maze_to_world_pos


class Player:
    def __init__(self, pos, maze: Maze, player_id=0):
        self._maze_ = maze
        self._id = player_id
        self._hp = PLAYER_HP
        self._speed = PLAYER_MOVING_SPEED
        self._radius = PLAYER_RADIUS
        self._position = pos.copy()  # MAZE

        self._previous_anchor = pos.copy()
        self._next_anchor = pos.copy()

        self._current_direction = STOP
        self._next_direction = STOP
        # self._bullets_group = bullets_group

        # self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        # self.image.fill(pygame.Color("black"))
        # pygame.draw.circle(self.image, pygame.Color("white"),
        #                    (int(self.image.get_width() / 2),
        #                     int(self.image.get_height() / 2)),
        #                    self.radius)
        # self.rect = self.image.get_rect(center=self.position)

    def _set_next_direction(self, input_direction):
        self._next_direction = input_direction

        # if self.current_direction == STOP and self.future_change_direction == STOP:
        #     return
        #
        # if self.current_direction == STOP and self.future_change_direction != STOP:
        #     if self.is_valid_direction(self.future_change_direction):
        #         self.current_direction = self.future_change_direction
        #         self._previous_anchor = self._target
        #     else:
        #         self.future_change_direction = STOP
        #         return

    def _meet_next_anchor(self):
        if self._next_anchor and self._previous_anchor:
            distance_between_anchors = np.sum(np.abs(self._next_anchor - self._previous_anchor))
            distance_to_position = np.sum(np.abs(self._position - self._previous_anchor))
            return distance_to_position >= distance_between_anchors
        return False

    def set_position(self, pos):
        self._position = pos.copy()

    def update(self, event, dt):
        if event in PLAYER_MOVEMENT:
            self._set_next_direction(event)
        elif event in PLAYER_SHOOT:
            self.shoot()
        self._move(dt)

    def _move(self, dt):

        self._position += DIRECTIONS[self._current_direction] * self._speed * dt

        if self._next_direction == -self._current_direction:
            self._reverse_direction()
            self._next_direction = None

        if self._meet_next_anchor():
            if self._next_direction:
                self._position = self._next_anchor.copy()  # TODO Fix position
                if self._is_valid_direction(self._next_direction):
                    # Check new input direction
                    self._previous_anchor = self._next_anchor
                    self._next_anchor = self._get_next_anchor(self._previous_anchor, self._next_direction)
                    self.current_direction = self._next_direction
                elif self._is_valid_direction(self._current_direction):
                    # If new input direction is not valid use older direction:
                    self._previous_anchor = self._next_anchor
                    self._next_anchor = self._get_next_anchor(self._previous_anchor, self.current_direction)
                else:
                    # If older direction lead to dead-end => stop
                    self.current_direction = STOP
                    self._next_direction = STOP
                self._next_direction = None
            else:
                pass

    def _reverse_direction(self):
        self._current_direction *= -1
        self._previous_anchor, self._next_anchor = self._next_anchor, self._previous_anchor

    def _is_valid_direction(self, player_direction):
        maze_direction = convert_player_direction_to_maze_direction(player_direction)
        return self._maze_.is_connected_to_direction((int(self._position[1]), int(self._position[0])), maze_direction)

    def _get_next_anchor(self, pos, player_direction):
        if player_direction == STOP:
            return np.array([pos[0], pos[1]])

        direction = convert_player_direction_to_maze_direction(player_direction)
        if self._maze_.is_connected_to_direction((int(pos[1]), int(pos[0])), direction):
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

    ## OK
    def get_bullet_target(self):
        cell_pos = np.array([int(self.position[0]), int(self.position[1])])

        if self.current_direction == STOP:
            return None
        direction = Maze.convert_player_direction_2_maze(self.current_direction)
        while self._maze_map[cell_pos[1], cell_pos[0], direction] == 1:
            cell_pos += DIRECTIONS[self.current_direction]
        return cell_pos

    def shoot(self):
        target = self.get_bullet_target()

        if target is None:
            return

        bullet = Bullet(self._bullets_group, 0, self.position, target, self.current_direction)

    def hit(self, damage):
        print(self.name, 'hit')


# class Player(Entity):
#     def __init__(self, pos, bullets_group, adj_matrix, id=0):
#         super().__init__(pos, bullets_group, adj_matrix, None, id)
#         self.name = 'Player'
#
#
# class Enemy(Entity):
#     def __init__(self, pos, bullets_group, enemies_group, adj_matrix, id=0):
#         super().__init__(pos, bullets_group, adj_matrix, enemies_group, id)
#         self.name = 'Enemy'
