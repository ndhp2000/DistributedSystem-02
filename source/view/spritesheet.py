import pygame
from source.assets import PlayerViewAsset, MenuViewAsset, MazeViewAsset


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
    def image_at(anchor, dim, sheet_name, colorkey = None):
        if SpriteSheet._not_init:
            SpriteSheet._sheets['PLAYER'] = SpriteSheet(PlayerViewAsset.player)
            SpriteSheet._sheets['MAZE_BACKGROUND'] = SpriteSheet(MazeViewAsset.background)
            SpriteSheet._sheets['MENU'] = SpriteSheet(MenuViewAsset.menu)
            SpriteSheet._sheets['MENU_BACKGROUND'] = SpriteSheet(MenuViewAsset.background)
            SpriteSheet._not_init = False

        rect = pygame.Rect(anchor, dim)
        image = pygame.Surface(rect.size)
        image.set_colorkey(0)
        image.blit(SpriteSheet._sheets[sheet_name].get_sheet(), (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

