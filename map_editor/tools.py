"""All tools to create a better map"""

import pygame as pg
from tile import Tile
from settings import RED, TILESIZE, MAPSIZE, YELLOW, GREEN


class tool(pg.sprite.Sprite):
    """A tool"""

    def __init__(self, game, x, y, name):
        self.groups = game.tools
        pg.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.game = game
        self.image = game.tool_images[name]
        self.rect = self.image.get_rect()
        self.rect.top = y * TILESIZE
        self.rect.left = x * TILESIZE
        self.selected = False

    def update(self):
        """Update the sprite"""

    def clicked(self, paint_x, paint_y):
        """Check if the sprite is clicked

        Args:
            paint_x (int)
            paint_y (int)

        Returns:
            bool
        """
        return self.rect.left == paint_x * TILESIZE and self.rect.top == paint_y * TILESIZE

    def action(self, *args):
        """Do something"""


class Rubber(tool):
    """A Rubber to erase all tiles from a layer"""

    def __init__(self, game, x, y, name):
        super(Rubber, self).__init__(game, x, y, name)
        self.image.fill(YELLOW)

    @staticmethod
    # pylint: disable=arguments-differ
    def action():
        """Remove all tiles from the layer

        Returns:
            list: empty list
        """
        return []


class Paint(tool):
    """A paint pot to filled all tiles from a layer"""

    def __init__(self, game, x, y, name):
        super(Paint, self).__init__(game, x, y, name)
        self.image.fill((RED))

    # pylint: disable=arguments-differ
    def action(self, layer, cut_surface):
        """Filled empty space in a layer using a cet surface

        Args:
            layer (list): all tiles
            cut_surface (dict): the surface used to filled the map

        Returns:
            list(Tile): contain all tiles from the layer
        """
        found = False
        for row in range(MAPSIZE):
            for col in range(MAPSIZE):
                for tile in layer:
                    if tile.x == col and tile.y == row:
                        found = True
                        break
                if found:
                    found = False
                else:
                    tile = Tile(
                        self.game.tileset, cut_surface['image'].copy(),
                        cut_surface['pos'][0],
                        cut_surface['pos'][1])
                    tile.set_pos(col + Tile.get_offset_x(), row)
                    layer.append(tile)
        return layer


class Player(tool):
    """Create a player"""

    def __init__(self, game, x, y, name):
        super(Player, self).__init__(game, x, y, name)
        self.image.fill((GREEN))

    def action(self, players, mouse_x, mouse_y):
        """Create a rect which représente a user

        Args:
            players (list): list which contains all created players
            mouse_x (int)
            mouse_y (int)
        """
        players.append(pg.Rect(mouse_x - TILESIZE // 2, mouse_y - TILESIZE // 2, TILESIZE, TILESIZE))
