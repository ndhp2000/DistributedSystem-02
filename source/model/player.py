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
        self.position = np.array([200, 400])
        self.speed = 100
        self.radius = 10
        self.color = YELLOW
        self.direction = STOP
        self.bullet_direction = UP
        self.bullets = []

    def update(self, dt):
        self.position += DIRECTIONS[self.direction]*self.speed*dt
        for bullet in self.bullets:
            if bullet.is_disable:
                continue

            bullet.update(dt)
            if bullet.is_out_screen():
                bullet.disable()

        self.bullets = [bullet for bullet in self.bullets if bullet.is_out_screen() or not bullet.is_disable]
        button_press = self.getValidKey()
        if button_press != SHOOT:
            self.direction = button_press
            if self.direction != STOP:
                self.bullet_direction = button_press
        else:
            self.direction = STOP
            new_bullet = Bullet(self.position, self.bullet_direction)
            self.bullets.append(new_bullet)

    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)
        for bullet in self.bullets:
            if bullet.is_out_screen():
                continue

            bullet.render(screen)