import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from bullet import Bullet

from ..model import Player

class PlayerView:
    def __init__(self):
        self.player = Player()

    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
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

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        if key_pressed[K_SPACE]:
            return SHOOT
        return STOP

    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)
        for bullet in self.bullets:
            if bullet.is_out_screen():
                continue

            bullet.render(screen)