"""Credits screen"""

import pygame as pg
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, CREDITS, TRANSITION_OUT


class Credits(_State):
    """Credits screen"""

    def __init__(self):
        self.name = CREDITS
        super(Credits, self).__init__(self.name)
        self.next = GAME

        self.background = pg.Surface((WIDTH, HEIGHT))

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill((255, 0, 0))
        super().setup_transition()

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
        self.draw()

    def get_events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                super().set_state(TRANSITION_OUT)

    def draw(self):
        """Draw content"""
        self.screen.blit(self.background, (0, 0))
