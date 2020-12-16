"""Define a chest"""

from config.window import TILESIZE
from os import path
import pygame as pg
from logger import logger
from config.sprites import ASSETS_CHEST


class Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = y
        self.groups = game.all_sprites, game.chests
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.game = game

        self.opening_images = ASSETS_CHEST
        self.open_image = pg.transform.scale(
            pg.image.load(path.join(game.sprites_folder, "chest", "open.png")),
            (TILESIZE, TILESIZE))

        self.is_open = False

        self.image = self.opening_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.frame_count = 0

    def update(self):
        if not self.is_open:
            self.frame_count += 1
            if self.frame_count > 47:
                self.frame_count = 0
            else:
                self.image = self.opening_images[self.frame_count // 6]
        else:
            self.image = self.open_image

    def try_open(self, player):
        if not self.is_open:
            for slot in player.inventory.slots:
                if slot.item and slot.item.name == "key":
                    logger.info("Open a chest")
                    player.inventory.slots.remove(slot)
                    self.is_open = True
                    break
            logger.info("You need a key to open the chest")
