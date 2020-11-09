"""Menu screen"""

import pygame as pg
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU, TRANSITION_OUT


class Menu(_State):
    """Menu screen"""

    def __init__(self):
        super(Menu, self).__init__()
        self.name = MENU
        self.next = GAME

        self.background = pg.Surface((WIDTH, HEIGHT))

        self.startup(0, 0)

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill((0, 255, 0))
        super().setup_transition()

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
        self.draw()

    def get_events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                super().set_state(TRANSITION_OUT)
            if event.key == pg.K_p:
                self.game_data['count'] += 1
                print(self.game_data["count"])

    def draw(self):
        self.screen.blit(self.background, (0, 0))