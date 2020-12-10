"""Menu screen"""

from os import path
from components.cursor import Cursor
from config.buttons import HEIGHT_BUTTON, HEIGHT_SLIDER, WIDTH_BUTTON, WIDTH_SLIDER
from config.window import HEIGHT, WIDTH
from config.colors import BEIGE, BLACK, BLUE_GREY
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
        super(NewGame, self).__init__(self.name, self.next, 'menu', 'background.jpg', {})

        self.background = pg.Surface((WIDTH, HEIGHT))
        image = pg.image.load(
            path.join(
                self.img_folder,
                'menu',
                'background.jpg')).convert()
        self.image = pg.transform.scale(image, (WIDTH, HEIGHT))

        self.create_slider()
        self.btns_dict = self.create_buttons_dict()
        self.create_buttons(self.image, start_y_offset=8 * HEIGHT // 10)
        self.create_text_box()

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "continue": {
                "text": "Continue",
                "on_click": self.save_next,
                "on_click_params": [CHARACTER_CREATION],
            }
        }

    def save_next(self, state):
        self.game_data['file_name'] = self.get_text_info() + '.json'
        self.game_data['num_heros'] = self.slider.getValue()
        logger.info("Filename : %s, Number of heros : %s", self.game_data['file_name'],  self.game_data['num_heros'])
        self.load_next_state(state)

    def create_slider(self):
        _x = WIDTH // 2 - WIDTH_SLIDER // 2
        _y = 6 * HEIGHT // 10
        self.slider = Cursor("", "", _x, _y, WIDTH_SLIDER, HEIGHT_SLIDER,
                             self.background, 1, 3, 1, 1, self.text_font, self.draw_text, BLACK, BLUE_GREY)

    def create_text_box(self):
        _x = WIDTH // 2 - WIDTH_BUTTON // 2
        _y = 4 * HEIGHT // 10 - HEIGHT_BUTTON // 2
        self.text_name = TextBox(self.background, _x, _y, WIDTH_BUTTON, HEIGHT_BUTTON, fontsize=50,
                                 color=BLACK, textColour=BLACK, onSubmit=self.get_text_info, radius=10, borderThickness=4)

    def get_text_info(self):
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
        self.slider.listen(events)
        self.text_name.listen(events)

    def draw(self):
        """Draw content"""
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image, (0, 0))
        self.text_name.draw()
        self.slider.draw()
        self.draw_text("Name your game", self.text_font, 24, BEIGE, WIDTH //
                       2, 3 * HEIGHT // 10, align="n", screen=self.background)
        self.draw_text(f"Number of heroes : {self.slider.getValue()}", self.text_font, 24, BEIGE, WIDTH //
                       2, 11 * HEIGHT // 20, align="n", screen=self.background)
        super().draw_elements("Create a game")
