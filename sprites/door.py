"""Define a door"""

from os import path
import pygame as pg
from config.sprites import ASSETS_DOOR
from config.window import TILESIZE
from logger import logger


class Door(pg.sprite.Sprite):
    """Create a door"""

    def __init__(self, game, x, y, wall, is_open=False):
        self._layer = y
        self.groups = game.doors, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.wall = wall
        self.game = game

        self.close_image = pg.transform.scale(
            pg.image.load(path.join(game.sprites_folder, "door", "door_closed.png")),
            (TILESIZE, TILESIZE))
        self.open_image = pg.transform.scale(
            pg.image.load(path.join(game.sprites_folder, "door", "door_fullyopen.png")),
            (TILESIZE, TILESIZE))
        self.opening_image = ASSETS_DOOR

        self.image = self.close_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.to_open = False
        self.is_open = is_open
        self.frame_count = 0

    def save(self):
        """Used the save the door data

        Returns:
            dict
        """
        return {
            "pos": {
                "x": self.x,
                "y": self.y
            },
            "is_open": self.is_open,
        }

    def update(self):
        """Used to update the door"""
        if self.to_open and not self.is_open:
            self.frame_count += 1
            if self.frame_count > 78:
                self.frame_count = 0
                self.is_open = True
                self.to_open = False
                self.game.walls.remove(self.wall)
            else:
                self.image = self.opening_image[self.frame_count // 6]

        elif self.is_open:
            self.image = self.open_image
        else:
            self.image = self.close_image

    def try_open(self, player):
        """Try to open the door

        Args:
            player (Player)
        """
        for slot in player.inventory.slots:
            if slot.item and slot.item.name == "bronze_key_small":
                self.game.logs.add_log("Open a door")
                player.inventory.remove_item(slot.item)
                self.to_open = True
                break
        self.game.logs.add_log("You need a key to open the door")
