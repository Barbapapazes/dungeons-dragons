"""The tile class"""

import pygame as pg
from settings import TILESIZE


class Tile():
    """A tile"""

    def __init__(self, tileset, image, x, y, ):
        self.image = image
        self.rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        self.gid = self.calc_gid(tileset, x, y)

    def __str__(self):
        return f"gid: {self.gid}"

    def set_pos(self, x, y):
        """Set the pos of the rect

        Args:
            x (int)
            y (int)
        """
        self.rect.top = y * TILESIZE
        self.rect.left = x * TILESIZE

    @staticmethod
    def calc_gid(tileset, x, y):
        """Calcul the gid

        Args:
            tileset (Tileset): the tileset used
            x (int)
            y (int)

        Returns:
            int: the gid
        """
        cols = tileset.tileset_width // TILESIZE
        # rows = tileset.tileset_height // TILESIZE
        gid = y * cols + x
        return gid
