"""Online game screen"""

import pygame as pg
from os import path
from window import _State
from logger import logger
from sprites.player import Player
from server.network import Network
from config.window import WIDTH, HEIGHT, TILESIZE
from config.colors import LIGHTGREY, BLACK, WHITE
from config.screens import CREDITS, MENU, GAME, TRANSITION_IN, TRANSITION_OUT


class OnlineGame(_State):
    """Online game screen"""

    def __init__(self):
        self.name = "online_game"
        super(OnlineGame, self).__init__(self.name)
        self.next = None

        self.all_sprites = None

    def startup(self, dt, game_data):
        self.dt = dt
        self.game_data = game_data
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        self.n = Network()
        (x, y) = self.n.get_p()
        self.player = Player(self, x, y)
        logger.info(self.player)
        super().setup_transition()

    def get_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                self.next = MENU
                super().set_state(TRANSITION_OUT)
            if event.key == pg.K_RIGHT:
                self.next = 'online_game'
                super().set_state(TRANSITION_OUT)

    def run(self, surface, keys, mouse, dt):
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
        try:
            self.n.send(self.player.pos)
        except BaseException as e:
            self.next = MENU
            super().set_state(TRANSITION_OUT)
            logger.exception(e)

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
