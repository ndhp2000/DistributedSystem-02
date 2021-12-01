import pygame
from constants import *
from vector import *

class Bullet:
    def __init__(self, id=0, position, direction):
        self.position = position
        self.speed = 200
        self.radius = 2
        self.direction = direction
        self.is_disable = False

    def update(self, dt):
        self.position += DIRECTION[self.direction] * self.speed * dt

    def disable(self):
        self.is_disable = True
    
    def is_out_screen(self):
        if self.position.x < 0 or self.position.x > SCREENWIDTH:
            return True
        if self.position.y < 0 or self.position.y > SCREENHEIGHT:
            return True
        return False