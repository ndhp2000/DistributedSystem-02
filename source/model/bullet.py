import pygame
from source.config import *

class Bullet:
    def __init__(self, id, position, target, direction):
        self.position = position
        self.speed = 200
        self.id = id
        self.radius = 2
        self.direction = direction
        self.is_disable = False
        self.target = target

    def move(self, dt):
        self.position += DIRECTIONS[self.direction] * self.speed * dt

        if self.meet_target():
            self.is_disable = True

    def disable(self):
        self.is_disable = True
    
    def is_out_screen(self):
        if self.position[0] < 0 or self.position[0] > MAP_WIDTH:
            return True
        if self.position[1] < 0 or self.position[1] > MAP_HEIGHT:
            return True
        return False

    def meet_target(self):
        pass


