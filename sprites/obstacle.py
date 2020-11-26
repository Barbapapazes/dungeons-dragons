"""Obstacle for a map"""
import pygame as pg


class Obstacle(pg.sprite.Sprite):
    """Create an obstacle"""

    def __init__(self, game, x, y, w, h):
        # self._layer = WALL_LAYER
        self.group = game.walls
        pg.sprite.Sprite.__init__(self, self.group)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
