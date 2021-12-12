class Entity:
    def __init__(self, radius, position, speed, direction):
        self._radius = radius
        self._speed = speed
        self._direction = direction
        self._position = position.copy()

    def get_radius(self):
        return self._radius

    def get_speed(self):
        return self._speed

    def get_position(self):
        return self._position.copy()
