"""Credits screen"""

import pygame as pg
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME


class Credits(_State):
    """Credits screen"""

    def __init__(self):
        super(Credits, self).__init__()
        self.name = 'credits'
        self.next = GAME

        self.background = pg.Surface((WIDTH, HEIGHT))

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill((255, 0, 0))
        super().setup_transition()

    def update(self):
        """Update states"""
        update_level = self.states_dict[self.state]
        update_level()

    def draw(self, surface):
        self.draw_scene(surface)

    def normal_update(self):
        """Update the normal state"""

    def events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                super().set_state('transition out')

    def draw_scene(self, surface):
        """Draw all graphics to the window surface."""
        surface.blit(self.background, (0, 0))
        super().transtition_active(surface)