"""Menu screen"""

import pygame as pg
from window import _State
from config.window import WIDTH, HEIGHT
from config.screens import GAME, MENU


class Menu(_State):
    """Menu screen"""

    def __init__(self):
        super(Menu, self).__init__()
        self.name = MENU
        self.next = None

        self.background = pg.Surface((WIDTH, HEIGHT))

        self.startup(0, 0)

    def startup(self, dt, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.dt = dt
        self.background.fill((0, 255, 0))
        super().setup_transition()

    def update(self, dt):
        """Update states"""
        self.dt = dt
        update_level = self.states_dict[self.state]
        update_level()

    def draw(self, surface):
        self.draw_scene(surface)

    def normal_update(self):
        """Update the normal state"""

    def events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.next = GAME
                super().set_state('transition out')

    def draw_scene(self, surface):
        """Draw all graphics to the window surface."""
        surface.blit(self.background, (0, 0))
        super().transtition_active(surface)
