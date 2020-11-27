"""Container, base class for slot"""
import pygame as pg


class Container:
    """Create a container"""

    def __init__(self, x, y, size, bg_color):
        self.x = x
        self.y = y
        self.bg_color = bg_color
        self.size = size
        self.item = None
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)

    def draw(self, screen):
        """Return the drawing of an inventoryslot

        Args:
            screen (surface)

        Returns:
            Rect: the slot
        """
        return pg.draw.rect(
            screen, self.bg_color, self.rect)

    def draw_items(self, screen):
        """Used to draw a item in the container"""
