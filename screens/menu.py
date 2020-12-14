"""Menu screen"""

import pygame as pg
from window import _Elements
from config.screens import GAME, MENU, NEW_GAME, OPTIONS, LOAD_GAME
from utils.shortcuts import load_shortcuts


class Menu(_Elements):
    """Menu screen"""

    def __init__(self):
        self.name = MENU
        self.next = GAME
        super(Menu, self).__init__(self.name, self.next, 'menu', 'background.png', self.create_buttons_dict())

        self.startup(0, load_shortcuts())

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "new_game": {
                "text": "New Game",
                "on_click": self.load_next_state,
                "on_click_params": [NEW_GAME],
            },
            "load_game": {
                "text": "Load a game",
                "on_click": self.load_next_state,
                "on_click_params": [LOAD_GAME],
            },
            "options": {
                "text": "Options",
                "on_click": self.load_next_state,
                "on_click_params": [OPTIONS],
            },
            "quit": {
                "text": "Quit",
                "on_click": self.stop_window,
                "on_click_params": [],
            }
        }

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.mouse = mouse
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        super().events_buttons()
        self.draw()

    def draw(self):
        """Draw content"""
        super().draw_elements("Dungeons and Dragons")

    @staticmethod
    def stop_window():
        """Quit the window using a user event"""
        quit_event = pg.event.Event(pg.USEREVENT, code="_State", name="quit")
        pg.event.post(quit_event)
