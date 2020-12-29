"""Define a spell"""

import pygame as pg
from config.window import TILESIZE
from random import randint


class EffectsZone(pg.sprite.Sprite):
    """Create a effect zone"""

    def __init__(self, game, x, y, _type, time_to_live, number_dice, dice_value):
        self.groups = game.all_sprites, game.effects_zones
        super(EffectsZone, self).__init__(self.groups)

        self.game = game
        self.x = x
        self.y = y
        self.type = _type
        self.time_to_live = time_to_live
        self.number_dice = number_dice
        self.dice_value = dice_value

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def get_dice_value(self):
        value = 0
        for _ in range(self.number_dice):
            value += randint(1, self.dice_value)
        return value

    def check_time_to_live(self):
        self.time_to_live -= 1
        if self.time_to_live == 0:
            self.kill()
