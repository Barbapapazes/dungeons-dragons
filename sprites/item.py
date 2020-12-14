"""Define a placable item"""

from config.sprites import ITEMS, BOB_RANGE, BOB_SPEED
import pygame as pg
import pytweening as tween


class PlacableItem(pg.sprite.Sprite):
    """Create a Placable item"""

    def __init__(self, game, pos, _type):
        self._layer = 1
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.transform.scale(ITEMS[_type], (32, 32))
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
