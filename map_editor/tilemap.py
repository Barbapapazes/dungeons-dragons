"""Setup the tilemap and the camera"""

import pygame as pg
from settings import TILESIZE, MAPSIZE, VIEWSIZE
from tile import Tile


class Camera():
    """A camera like"""

    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def apply(self, rect):
        """Update the pos of a rect

        Args:
            rect (Rect): the rect to move

        Returns:
            Rect
        """
        return rect.move(self.camera.topleft)

    def update(self):
        """Used to move the camera"""
        keys = pg.key.get_pressed()
        if keys[pg.K_i]:
            self.y += TILESIZE
        if keys[pg.K_k]:
            self.y -= TILESIZE
        if keys[pg.K_j]:
            self.x += TILESIZE
        if keys[pg.K_l]:
            self.x -= TILESIZE

        self.x = min(self.x, 0)
        self.y = min(self.y, 0)
        self.x = max(self.x, (VIEWSIZE - MAPSIZE) * TILESIZE)
        self.y = max(self.y, (VIEWSIZE - MAPSIZE) * TILESIZE)

        self.camera = pg.Rect(self.x, self.y, self.width, self.height)

    def get_x(self):
        """Get the number of tile moved in x

        Returns:
            int
        """
        return self.x // TILESIZE

    def get_y(self):
        """Get the number of tile moved in y

        Returns:
            int
        """
        return self.y // TILESIZE
