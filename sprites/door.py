"""Define a door"""

from os import path
import pygame as pg
from config.sprites import ASSETS_DOOR
from config.window import TILESIZE


class Door(pg.sprite.Sprite):
    """Create a door"""

    def __init__(self, game, x, y):
        self._layer = 0
        self.groups = game.doors, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y

        self.close_image = pg.transform.scale(
            pg.image.load(path.join(game.sprites_folder, "door", "door_closed.png")),
            (TILESIZE, TILESIZE))
        self.open_image = pg.transform.scale(
            pg.image.load(path.join(game.sprites_folder, "door", "door_fullyopen.png")),
            (TILESIZE, TILESIZE))
        self.opening_image = ASSETS_DOOR

        self.image = self.close_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        pass

    # def draw(self):
    #     pass
