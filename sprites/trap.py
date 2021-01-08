"""Define a trap"""
from config.sprites import ASSETS_TRAP
import pygame as pg


class Trap(pg.sprite.Sprite):
    """Create a trap"""

    def __init__(self, game, x, y, ):
        self.layer = 0
        self.groups = game.all_sprites, game.game.traps
        super(Trap, self).__init__(self.groups)

        self.x = x
        self.y = y
        self.game = game.game

        self.opening_trap = ASSETS_TRAP
        self.to_open = True

        self.image = self.opening_trap[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.frame_count = 0

    def update(self):
        """Update the trap"""
        if self.to_open:
            self.frame_count += 1
            if self.frame_count > 60:
                self.frame_count = 0
            else:
                self.image = self.opening_trap[self.frame_count // 10]
        else:
            self.image = self.opening_trap[0]
