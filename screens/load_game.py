"""Load game screen"""

import pygame as pg
from window import _State
from config.screens import MENU, LOAD_GAME, TRANSITION_OUT
from config.colors import WHITE
from config.window import WIDTH, HEIGHT
from data.game_data import create_game_data


class LoadGame(_State):
    """Load game screen"""

    def __init__(self):
        super(LoadGame, self).__init__()
        self.name = LOAD_GAME
        self.next = MENU

        self.background = pg.Surface((WIDTH, HEIGHT))

        self.startup(0, create_game_data())

    def run(self, surface, keys, dt):
        """Run states"""
        super().run(surface, keys, dt)
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        self.draw()
        super().set_state(TRANSITION_OUT)

    def draw(self):
        """Draw loading page"""
        self.background.fill((0, 255, 0))
        self.draw_text("Loading", self.title_font, 30, WHITE, WIDTH // 2, HEIGHT // 2, "center")
