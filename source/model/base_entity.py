import numpy as np


class Entity:
    def __init__(self, radius, maze_radius, position, speed, direction):
        self._radius = radius
        self._speed = speed
        self._direction = direction
        self._position = position.copy()
        self._is_removed = False
        self._maze_radius = maze_radius

    def get_radius(self):
        return self._radius

    def get_maze_radius(self):
        return self._maze_radius

    def get_speed(self):
        return self._speed

    def get_position(self):
        return self._position.copy()

    def is_removed(self):
        return self._is_removed

    @staticmethod
    def collide(entity1, entity2):
        if entity1.get_origin_id() == entity2.get_origin_id():
            return False

        if entity1.is_removed() or entity2.is_removed():
            return False

        entity1_position = entity1.get_position()
        entity2_position = entity2.get_position()

        distance_between_entity = np.linalg.norm(entity1_position - entity2_position)
        sum_radius = entity1.get_maze_radius() + entity2.get_maze_radius()

        if distance_between_entity <= sum_radius:
            return True

        return False
