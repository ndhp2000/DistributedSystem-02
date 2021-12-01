import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from bullet import Bullet
import numpy as np
from config 

class Player:
    def __init__(self):
        self.name = PACMAN
        self.hp = 10
        self.position = np.array([200, 400])
        self.speed = 100
        self.radius = 10
        self.color = YELLOW
        self.direction = STOP
        self.bullet_direction = UP
        self.bullets = []

    def move(self, event_type, dt):
        if event_type == -self.direction:
            self.direction = event_type
            self.position += DIRECTIONS[self.direction] * self.speed * dt
        elif event_type == self.direction:
            self.position += DIRECTIONS[self.direction] * self.speed * dt
        elif event_type == STOP:
            self.direction = STOP

    def shoot(self):
        pass

    def update(self, event_type, dt):
        if event_type in PLAYER_MOVEMENT:
            self.move(event_type, dt)
            return None

        if event_type in PLAYER_SHOOT:
            bullet = self.shoot(event_type)
            return bullet