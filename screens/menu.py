"""Menu screen"""

import pygame as pg
from window import _State
from config.window import WIDTH, HEIGHT


class Menu(_State):
    """Menu screen"""

    def __init__(self):
        super(Menu, self).__init__()
        self.name = 'menu'
        self.next = 'credits'

        self.background = pg.Surface((WIDTH, HEIGHT))

    def startup(self, current_time, game_data):
        """Initialize data at scene start."""
        self.game_data = game_data
        self.current_time = current_time
        self.background.fill((0, 255, 0))
        super().setup_transition()

    def update(self, surface, keys, current_time):
        """Update states"""
        update_level = self.states_dict[self.state]
        update_level(keys)
        self.draw_scene(surface)

    def normal_update(self, *args):
        """Update the normal state"""

    def events(self, event):
        """Events loop"""
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                super().set_state('transition out')

    def draw_scene(self, surface):
        """Draw all graphics to the window surface."""
        surface.blit(self.background, (0, 0))
        super().transtition_active(surface)
