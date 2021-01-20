"""Used to check the end of a level"""
from config.sprites import ITEMS
import pygame as pg
from config.window import HEIGHT, TILESIZE
from logger import logger


class MapCheck(pg.sprite.Sprite):
    def __init__(self, game, x, y, name):
        self._layer = -1
        self.game = game
        self.groups = game.all_sprites, game.map_checks
        super(MapCheck, self).__init__(self.groups)

        self.image = pg.transform.scale(ITEMS["stairs"], (TILESIZE, TILESIZE))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.name = name
        self.create_name()

    def create_name(self):
        """Cut the name to optain data"""
        data_spliced = self.name.split("-")
        self.folder = data_spliced[1]
        self.filename = data_spliced[2]

    def collide(self):
        """Call action when collide"""
        if self.filename == "finish":
            self.game.create_dim()
            self.game.btns_dict = self.game.create_buttons_dict("finish")
            self.game.create_buttons(self.game.screen, start_y_offset=8 * HEIGHT / 10)
            self.game.toggle_sub_state("finish")
        else:
            self.game.save_data()
            data = {
                "game_data": {
                    "heros": self.game.game_data["game_data"]["heros"],
                    "map": {
                        "folder": self.folder,
                        "filename": self.filename
                    },
                    "difficulty": self.game.difficulty
                },
                "minimap": {
                    "fog": None,
                    "cover": None,
                },
                "next": True,
                "loaded": False,
                "shortcuts": self.game.game_data["shortcuts"],
                "music": self.game.game_data["music"],
            }
            self.game.game_data = data
            self.game.new()

    def event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass
