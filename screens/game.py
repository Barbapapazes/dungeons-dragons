"""Game screen"""

import pygame as pg
from window import _State
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY


class Game(_State):
    """Game screen"""

    def __init__(self):
        super(Game, self).__init__()
        self.next = None

        self.all_sprites = None

        self.load_data()

    def load_data(self):
        pass

    def startup(self, dt, game_data):
        self.all_sprites = pg.sprite.Group()

    def events(self, event):
        pass

    def update(self, keys):
        pass

    @staticmethod
    def draw_grid(surface):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self, surface):
        self.draw_grid(surface)
