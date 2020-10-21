"""The tile class"""

import pygame as pg
from settings import TILESIZE, MAPSIZE, WIDTH


class Tile():
    """A tile"""

    def __init__(self, tileset, image, x, y, ):
        self.image = image
        self.rect = pg.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        self.gid = self.calc_gid(tileset, x, y)
        self.x = x
        self.y = y

    def __str__(self):
        return f"gid: {self.gid}, pos: {self.x} {self.y}"

    def set_pos(self, x, y):
        """Set the pos of the rect

        Args:
            x (int): postition sur l'écran
            y (int)
        """
        self.x = x - self.get_offset_x()  # pos on the map
        self.y = y
        self.rect.top = y * TILESIZE  # pos on the screen
        self.rect.left = x * TILESIZE

    @staticmethod
    def get_offset_x():
        """Get the offset of the map

        Returns:
            int
        """
        return WIDTH // TILESIZE - MAPSIZE

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
        gid = y * cols + x + 1
        return gid
