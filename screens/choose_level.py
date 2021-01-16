"""Choose level screen"""

import pygame as pg
from config.screens import CHOOSE_LEVEL, INTRODUCTION, TRANSITION_OUT
from logger import logger
from window import _Elements


class ChooseLevel(_Elements):
    """Choose level screen"""

    def __init__(self):
        self.next = INTRODUCTION
        self.name = CHOOSE_LEVEL
        self.state = 'normal'

        super(ChooseLevel, self).__init__(self.name, self.next, 'menu', '0.png', self.create_buttons_dict())

    def startup(self, dt, game_data):
        super().startup(dt, game_data)

        self.create_back_button(self.background, self.load_next_state, [CHOOSE_LEVEL])

    def all_events(self, events):
        """Listen for all events

        Args:
            events (Event[])
        """
        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.load_next_state(CHOOSE_LEVEL)

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        btns_dict = dict()
        difficulties = ["sandbox", "easy", "medium", "hard", "hardcore"]
        for index, value in enumerate(difficulties):
            btns_dict[value] = {
                "text": value,
                "on_click": self.load,
                "on_click_params": [index],
            }
        return btns_dict

    def load(self, index):
        self.game_data["game_data"]["difficulty"] = index
        logger.info("Difficulty %s", index)
        super().set_state(TRANSITION_OUT)
        logger.debug(self.game_data)

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        super().run(surface, keys, mouse, dt)
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        super().events_buttons(back=True)
        self.draw()

    def draw(self):
        """Draw the page"""
        super().draw_elements('Choose a difficulty')
