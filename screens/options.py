"""Options screen"""

from config.buttons import HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON, WIDTH_BUTTON
from config.colors import BEIGE, GREEN_DARK, YELLOW_LIGHT
from os import path
import pygame as pg
from window import _State
from logger import logger
from config.window import WIDTH, HEIGHT
from config.screens import OPTIONS, SHORTCUTS, TRANSITION_OUT


class Options(_State):
    """Options screen"""

    def __init__(self):
        self.name = OPTIONS
        super(Options, self).__init__(self.name)
        self.next = None

        # Background image
        image = pg.image.load(
            path.join(
                self.img_folder, 'options',
                "background.jpg")).convert()
        self.image = pg.transform.scale(image, (WIDTH, HEIGHT))

        # Buttons
        self.fontsize = 50

        self.create_buttons()

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "shortcuts": {
                "text": "Shortcuts",
                "on_click": self.load_next_state,
                "on_click_params": [SHORTCUTS],
            },
        }

    def create_buttons(self):
        """Create buttons"""
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        y_base = 250
        self.btns = list()
        logger.info("Create all buttons from menu")
        for index, (_, value) in enumerate(
                self.create_buttons_dict().items()):
            self.btns.append(self.create_button(
                self.image,
                _x,
                y_base + index * 100,
                WIDTH_BUTTON,
                HEIGHT_BUTTON,
                value["text"],
                self.button_font,
                self.fontsize,
                MARGIN_BUTTON,
                RADIUS_BUTTON,
                BEIGE,
                YELLOW_LIGHT,
                GREEN_DARK,
                value["on_click"],
                value["on_click_params"]
            ))

    def load_next_state(self, *next_state):
        """Load the new state"""
        self.next = next_state[0]
        super().set_state(TRANSITION_OUT)

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
        self.events_buttons()
        self.draw()

    def get_events(self, event):
        """Events loop"""

    def events_buttons(self):
        """Used to manage the event for buttons"""
        events = pg.event.get()
        for btn in self.btns:
            btn.listen(events)

    def draw(self):
        """Draw content"""
        self.draw_background()
        self.draw_title()
        self.draw_buttons()

    def draw_background(self):
        """Draw the background"""
        self.screen.blit(self.image, (0, 0))

    def draw_title(self):
        """Draw the title"""
        self.draw_text(
            "Options",
            self.title_font,
            150,
            YELLOW_LIGHT,
            WIDTH // 2,
            15,
            align="n")

    def draw_buttons(self):
        """Draw all buttons"""
        for btn in self.btns:
            btn.draw()
