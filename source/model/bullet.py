import pygame
from source.config import *

class Bullet:
    def __init__(self, id, position, direction):
        self.position = position
        self.speed = 200
        self.id = id
        self.radius = 2
        self.direction = direction
        self.is_disable = False

    def update(self, dt):
        self.position += DIRECTION[self.direction] * self.speed * dt

    def disable(self):
        self.is_disable = True
    
    def is_out_screen(self):
        if self.position.x < 0 or self.position.x > MAP_WIDTH:
            return True
        if self.position.y < 0 or self.position.y > MAP_HEIGHT:
            return True
        return False

    def collision_with_wall(self):
        pass

