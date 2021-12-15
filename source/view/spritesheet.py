import pygame
from source.assets import PlayerViewAsset


class SpriteSheet:
    _instance_ = None
    TILE_WIDTH = 16
    TILE_HEIGHT = 16

    def __init__(self, filename):
        self._sheet_ = pygame.image.load(filename).convert()

    def _get_sheet(self):
        return self._sheet_

    @staticmethod
    def image_at(x, y, colorkey = None):
        if SpriteSheet._instance_ is None:
            SpriteSheet._instance_ = SpriteSheet(PlayerViewAsset.player)

        rect = pygame.Rect((x * SpriteSheet.TILE_WIDTH,
                            y * SpriteSheet.TILE_HEIGHT,
                            2 * SpriteSheet.TILE_WIDTH,
                            2 * SpriteSheet.TILE_HEIGHT))
        image = pygame.Surface(rect.size).convert()
        image.blit(SpriteSheet._instance_._get_sheet(), (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

