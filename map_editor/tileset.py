"""Class to manage a tileset"""

import pygame as pg
from os import path
from settings import TILESIZE, HEIGHT


class Tileset():
    """Manage the tileset"""

    def __init__(self, assets_folder, filename):
        self.tileset = pg.image.load(path.join(assets_folder, filename)).convert_alpha()
        self.tileset_width = self.tileset.get_width()
        self.tileset_height = self.tileset.get_height()
        self.gid_max = self.tileset_height // TILESIZE * self.tileset_height // TILESIZE - 1
        self.move_x = 0
        self.move_y = 0

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
        self.get_keys()

    def get_keys(self):
        """Use the key to move the tileset"""
        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
            pass
        if keys[pg.K_d]:
            pass
        if keys[pg.K_z] and self.move_y < 0:
            self.move_y += 1
        if keys[pg.K_s] and self.move_y > - (self.tileset_height - HEIGHT) // TILESIZE:
            self.move_y -= 1

    def get_mouse(self, event):
        """Use the mouse to move the tileset

        Args:
            event (dict): the event from the events function
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4 and self.move_y < 0:
                self.move_y += 1
            elif event.button == 5 and self.move_y > - (self.tileset_height - HEIGHT) // TILESIZE:
                self.move_y -= 1
