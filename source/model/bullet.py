import pygame
from source.config import *
from source.model.maze import Maze
from source.view.utils import convert_maze_to_world_pos

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullets_group, id, position, target, direction):
        pygame.sprite.Sprite.__init__(self, bullets_group)
        self.position = position.copy()
        self.speed = 5
        self.id = id
        self.radius = 5
        self.direction = direction
        self.is_disable = False
        self.target = target
        self.player_id = 0

        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(pygame.Color("black"))
        pygame.draw.circle(self.image, pygame.Color("orange"),
                            (int(self.image.get_width() /2),
                            int(self.image.get_height() /2)),
                            self.radius)
        self.rect = self.image.get_rect(center=self.position)

    def move(self, dt):
        self.position += DIRECTIONS[self.direction] * self.speed * dt

        if self.meet_target(dt):
            self.kill()
        else:
            world_position = convert_maze_to_world_pos(self.position[0], self.position[1])
            self.rect = self.image.get_rect(center=world_position)

    def is_out_screen(self):
        if self.position[0] < 0 or self.position[0] > MAP_WIDTH:
            return True
        if self.position[1] < 0 or self.position[1] > MAP_HEIGHT:
            return True
        return False

    def meet_target(self, dt):
        distance = np.linalg.norm(self.position - self.target)
        if distance < self.speed * dt * 0.55:
            return True
        return False

    def update(self, dt):
        self.move(dt)



