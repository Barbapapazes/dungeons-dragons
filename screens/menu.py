"""Menu screen"""

from utils.music import load_music
from config.window import HEIGHT, WIDTH
import pygame as pg
from window import _Elements
from config.screens import BACKGROUND_MENU, CREDITS, GAME, MENU, NEW_GAME, OPTIONS, LOAD_GAME
from utils.shortcuts import load_shortcuts
from itertools import cycle


class Menu(_Elements):
    """Menu screen"""

    def __init__(self):
        self.name = MENU
        self.next = GAME
        super(Menu, self).__init__(self.name, self.next, 'menu', '0.png', self.create_buttons_dict())

        self.frames = list()
        for frame in BACKGROUND_MENU:
            self.frames.append(pg.transform.scale(frame, (WIDTH, HEIGHT)))

        self.frames = cycle(self.frames)
        self.background = next(self.frames)

        self.frame_time = 80 / 1000
        self.frame_timer = 0

        self.win = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.win.fill((0, 0, 0, 0))
        self.create_buttons(self.win)

        self.startup(0, load_shortcuts() | load_music())

    def create_buttons_dict(self):
        """Create the dict for all buttons


        Returns:
            dict
        """
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
            "online_game": {
                "text": "Online game",
                "on_click": self.load_next_state,
                "on_click_params": ["online_game"],
            },
            "options": {
                "text": "Options",
                "on_click": self.load_next_state,
                "on_click_params": [OPTIONS],
            },
            "credits": {
                "text": "Credits",
                "on_click": self.load_next_state,
                "on_click_params": [CREDITS],
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
        self.update_background()
        super().events_buttons()
        self.draw()

    def update_background(self):
        """Used to update the background"""
        self.frame_timer += self.dt
        if self.frame_timer >= self.frame_time:
            self.frame_timer -= self.frame_time
            self.background = next(self.frames)

    def draw(self):
        """Draw content"""
        super().draw_elements("Dungeons and Dragons")
        self.screen.blit(self.win, (0, 0))

    @staticmethod
    def stop_window():
        """Quit the window using a user event"""
        quit_event = pg.event.Event(pg.USEREVENT, code="_State", name="quit")
        pg.event.post(quit_event)
