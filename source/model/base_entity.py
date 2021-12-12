import numpy as np


class Entity:
    def __init__(self, radius, position, speed, direction):
        self._radius = radius
        self._speed = speed
        self._direction = direction
        self._position = position.copy()
        self._is_removed = False

    def get_radius(self):
        return self._radius

    def get_speed(self):
        return self._speed

    def get_position(self):
        return self._position.copy()

    def is_removed(self):
        return self._is_removed

    @staticmethod
    def collide(entity1, entity2, dt):
        if entity1.get_origin_id() == entity2.get_origin_id():
            return False

        if entity1.is_removed() or entity2.is_removed():
            return False

        entity1_position = entity1.get_position()
        entity1_speed = entity1.get_speed()

        entity2_position = entity2.get_position()
        entity2_speed = entity2.get_speed()

        distance_between_entity = np.linalg.norm(entity1_position - entity2_position) - entity1_speed * dt - entity2_speed * dt
        sum_radius = entity1.get_radius() + entity2.get_radius()

        if distance_between_entity <= sum_radius:
            return True

        return False
