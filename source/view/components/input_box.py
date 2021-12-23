import pygame


class InputBox:
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')

    def __init__(self, anchor: (int, int), dim: (int, int), text=''):
        self._color = self.COLOR_INACTIVE
        self._text = text
        self._font = pygame.font.Font(None, 32)
        self._txt_surface = self._font.render(text, True, self._color)
        self._active = False

        self._rect = pygame.Rect(anchor, dim)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self._txt_surface, (self._rect.x + 5, self._rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self._color, self._rect, 2)

    def is_active(self):
        return self._active

    def get_rect(self):
        return self._rect

    def set_active(self, state):
        self._active = state
