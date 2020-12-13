"""Define a key"""

from config.sprites import ASSETS_ITEMS, BOB_RANGE, BOB_SPEED
import pygame as pg
import pytweening as tween


class Item(pg.sprite.Sprite):
    """Create a key"""

    def __init__(self, game, pos, _type):
        self._layer = 1
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.transform.scale(ASSETS_ITEMS[_type], (32, 32))
        self.rect = self.image.get_rect()
        self.type = _type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        """Update the item"""
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1