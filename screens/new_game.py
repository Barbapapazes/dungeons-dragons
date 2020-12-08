"""Menu screen"""

from config.buttons import HEIGHT_BUTTON, WIDTH_BUTTON
from config.window import HEIGHT, WIDTH
from config.colors import BLACK
from logger import logger
import pygame as pg
from pygame_widgets import TextBox
from window import _Elements
from config.screens import NEW_GAME, CHARACTER_CREATION


class NewGame(_Elements):
    """Menu screen"""

    def __init__(self):
        self.name = NEW_GAME
        self.next = CHARACTER_CREATION
        super(NewGame, self).__init__(self.name, self.next, 'menu',
                                      'background.jpg', self.create_buttons_dict())

        self.create_text_box()

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "lambda": {
                "text": None,
                "on_click": (lambda _: None),
                "on_click_params": [],
            },
            "lambda_2": {
                "text": None,
                "on_click": (lambda _: None),
                "on_click_params": [],
            },
            "continue": {
                "text": "Continue",
                "on_click": self.save_next,
                "on_click_params": [CHARACTER_CREATION],
            }
        }

    def save_next(self, state):
        self.game_data['file_name'] = self.get_text_info() + '.json'
        self.load_next_state(state)

    def create_text_box(self):
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        _y = HEIGHT // 2 - HEIGHT_BUTTON // 2
        self.text_name = TextBox(self.background, _x, _y, WIDTH_BUTTON, HEIGHT_BUTTON, fontsize=50,
                                 color=BLACK, textColour=BLACK, onSubmit=self.get_text_info, radius=10, borderThickness=4)

    def get_text_info(self):
        logger.info(self.text_name.getText())
        return self.text_name.getText()

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

    def all_events(self, events):
        self.text_name.listen(events)

    def draw(self):
        """Draw content"""
        self.text_name.draw()
        super().draw_elements("Create a game")
