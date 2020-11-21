"""Shortcuts screen"""

import pygame as pg
from window import _State
from config.window import WIDTH, HEIGHT
from config.colors import BLACK
from config.screens import SHORTCUTS, TRANSITION_OUT


class Shortcuts(_State):
    """Shortcuts screen"""

    def __init__(self):
        self.name = SHORTCUTS
        super(Shortcuts, self).__init__(self.name)
        self.next = None

        self.background = pg.Surface((WIDTH, HEIGHT))

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill((255, 0, 255))
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

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("shortcuts".upper(), self.title_font, 48, BLACK, WIDTH // 2, 0, align="n")
