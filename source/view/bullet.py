from ..model import Bullet

class BulletView:
    def __init__(self):
        self.bullet = Bullet()

    def render(self, screen):
        bullet_pos = self.bullet.position.asInt()
        pygame.draw.circle(screen, WHITE, bullet_pos, self.radius)