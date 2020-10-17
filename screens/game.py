"""Game screen"""

import pygame as pg
from window import _State
from sprites.player import Player
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT


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

    def get_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.next = MENU
                super().set_state(TRANSITION_OUT)
            if event.key == pg.K_RIGHT:
                self.next = CREDITS
                super().set_state(TRANSITION_OUT)

    def run(self, surface, keys, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.update()
        self.draw()

    @staticmethod
    def draw_grid(surface):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(surface, LIGHTGREY, (0, y), (WIDTH, y))

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid(self.screen)
        self.all_sprites.draw(self.screen)
        super().transtition_active(self.screen)
