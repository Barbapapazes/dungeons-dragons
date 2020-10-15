"""Game screen"""

import pygame as pg
from window import _State
from sprites.player import Player
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK
from config.screens import CREDITS, MENU, GAME


class Game(_State):
    """Game screen"""

    def __init__(self):
        super(Game, self).__init__()
        self.name = GAME
        self.next = None

        self.all_sprites = None

        self.load_data()

    def load_data(self):
        pass

    def startup(self, dt, game_data):
        self.dt = dt
        self.all_sprites = pg.sprite.Group()

        Player(self, 2, 4)
        super().setup_transition()

    def events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.next = MENU
                super().set_state('transition out')
            if event.key == pg.K_RIGHT:
                self.next = CREDITS
                super().set_state('transition out')

    def update(self, dt):
        """Update states"""
        update_level = self.states_dict[self.state]

        self.dt = dt
        update_level()

    def normal_update(self):
        self.all_sprites.update()

    @staticmethod
    def draw_grid(surface):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self, surface):
        surface.fill(BLACK)
        self.draw_grid(surface)
        self.all_sprites.draw(surface)
        super().transtition_active(surface)
