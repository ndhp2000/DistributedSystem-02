import pygame
from source.utils.assets import PlayerViewAsset, MenuViewAsset, MazeViewAsset


class SpriteSheet:
    # _instance_ = None
    _sheets = {
        'PLAYER': None,
        'MAZE': None,
        'MENU': None,
        'MENU_BACKGROUND': None
    }
    _not_init = True
    TILE_WIDTH = 16
    TILE_HEIGHT = 16

    def __init__(self, filename):
        self._sheet_ = pygame.image.load(filename).convert_alpha()

    def get_sheet(self):
        return self._sheet_

    @staticmethod
    def image_at(anchor, dim, sheet_name):
        if SpriteSheet._not_init:
            SpriteSheet._sheets['PLAYER'] = SpriteSheet(PlayerViewAsset.player)
            SpriteSheet._sheets['MAZE_BACKGROUND'] = SpriteSheet(MazeViewAsset.background)
            SpriteSheet._sheets['MENU'] = SpriteSheet(MenuViewAsset.menu)
            SpriteSheet._sheets['MENU_BACKGROUND'] = SpriteSheet(MenuViewAsset.background)
            SpriteSheet._not_init = False

        rect = pygame.Rect(anchor, dim)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(SpriteSheet._sheets[sheet_name].get_sheet(), (0, 0), rect)
        image = image.convert_alpha()

        return image
