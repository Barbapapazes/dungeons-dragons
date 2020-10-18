"""Class to manage a tileset"""

import pygame as pg
from os import path
from settings import TILESIZE


class Tileset():
    """Manage the tileset"""

    def __init__(self, assets_folder, filename):
        self.tileset = pg.image.load(path.join(assets_folder, filename)).convert_alpha()
        self.tileset_width = self.tileset.get_width()
        self.tileset_height = self.tileset.get_height()
        self.move_x = 2
        self.move_y = -10

    def get_tileset(self):
        """Get the tileset

        Returns:
            Surface: the image loaded
        """
        return self.tileset

    def get_move_x(self):
        """Get the x offset to move the tileset

        Returns:
            int: the x offset in pixel using the tilesize
        """
        return self.move_x * TILESIZE

    def get_move_y(self):
        """Get the y offset to move the tileset

        Returns:
            int: the y offset in pixel using the tilesize
        """
        return self.move_y * TILESIZE

    def update(self):
        """Update the map"""

    def get_keys(self):
        """Use the key to move the tileset"""
        keys = pg.key.get_pressed()
