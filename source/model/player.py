import pygame
from pygame.locals import *
from source.model.bullet import Bullet
import numpy as np
from source.config import *

class Player:
    def __init__(self, pos, id=0):
        self.id = id
        self.hp = 10
        self.position = pos
        self.speed = 1
        self.radius = 10
        self.action = STOP
        self.direction = STOP
        self.bullets = []

    def pre_move(self, event_type=None, dt=1):
        position = self.position
        if event_type is None:
            position += DIRECTIONS[self.direction] * self.speed * dt
            return position

        if self.direction == STOP:
            position += DIRECTIONS[event_type] * self.speed * dt

        if abs(event_type) == abs(self.direction):
            position += DIRECTIONS[event_type] * self.speed * dt
        elif event_type == STOP:
            pass

        return position

    def move(self, pos, event_type=None):
        if self.direction == STOP:
            self.direction = event_type
        if event_type == -self.direction:
            self.direction = event_type
        elif event_type == STOP:
            self.action = STOP

        self.position = pos

    def shoot(self):
        bullet = Bullet(self.position, self.bullet_direction)
        return bullet

