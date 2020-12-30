"""Define a chest"""

import pygame as pg
from logger import logger
from config.sprites import ASSETS_MERCHANT
from store.shop import Shop


class Merchant(pg.sprite.Sprite):
    """Create a merchant"""

    def __init__(self, game, x, y, width, consumable=None, weapons=None, armor=None):
        self._layer = y
        self.groups = game.all_sprites, game.merchants
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.game = game
        self.width = width

        frames = list()
        for frame in ASSETS_MERCHANT:
            frames.append(pg.transform.scale(frame, (self.width, int(width * frame.get_height() / frame.get_width()))))

        self.idles_images = frames

        self.image = self.idles_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.shop = Shop(game, consumable, weapons, armor)

        self.frame_count = 0

    def save(self):
        """Used to save the merchant data

        Returns:
            dict
        """
        return {
            "pos": {
                "x": self.x,
                "y": self.y
            },
            "shop": self.shop.save()
        }

    def update(self):
        """Used to update the merchant"""
        self.frame_count += 1
        if self.frame_count > 59:
            self.frame_count = 0
        else:
            self.image = self.idles_images[self.frame_count // 15]

    def try_open(self):
        """Try to open a merchant"""
        logger.info("Open a merchant")
        self.game.merchant_open = True
        self.game.opened_merchant = self
