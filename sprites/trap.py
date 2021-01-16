"""Define a trap"""
from config.window import TILESIZE
from config.sprites import ASSETS_TRAP
import pygame as pg
from logger import logger


class Trap(pg.sprite.Sprite):
    """Create a trap"""

    def __init__(self, game, x, y):
        self._layer = 0
        self.groups = game.all_sprites, game.traps
        super(Trap, self).__init__(self.groups)

        self.x = x
        self.y = y
        self.game = game

        self.opening_trap = list()
        for frame in ASSETS_TRAP:
            frame = pg.transform.scale(frame, (TILESIZE // 2, TILESIZE // 2))
            self.opening_trap.append(frame)
        self.to_open = True

        self.image = self.opening_trap[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.frame_count = 0

    def update(self):
        """Update the trap"""
        if self.to_open:
            self.frame_count += 1
            if self.frame_count > 29:
                self.frame_count = 0
                self.to_open = False
            else:
                self.image = self.opening_trap[self.frame_count // 3]
        else:
            self.image = self.opening_trap[0]
