import pygame
from constants import *
from vector import *

class Bullet:
    def __init__(self, position, direction):
        self.position = position
        self.directions = {STOP:Vector2(), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        self.speed = 200
        self.radius = 2
        self.color = WHITE
        self.direction = direction
        self.is_disable = False

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

    def disable(self):
        self.is_disable = True
    
    def is_out_screen(self):
        if self.position.x < 0 or self.position.x > SCREENWIDTH:
            return True
        if self.position.y < 0 or self.position.y > SCREENHEIGHT:
            return True
        return False