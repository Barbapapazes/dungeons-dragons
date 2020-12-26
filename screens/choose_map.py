"""Menu screen"""

from config.window import HEIGHT, WIDTH
import pygame as pg
from window import _Elements
from config.screens import BACKGROUND_MENU, CHARACTER_CREATION, CHOOSE_MAP, CREDITS, GAME, INTRODUCTION, MENU, NEW_GAME, OPTIONS, LOAD_GAME, TRANSITION_IN, TRANSITION_OUT
import os
from os import path
from logger import logger


class ChooseMap(_Elements):
    """ChooseMap screen"""

    def __init__(self):
        self.name = CHOOSE_MAP
        self.next = INTRODUCTION

        game_folder = path.dirname('.')
        assets_folder = path.join(game_folder, 'assets')
        self.levels_maps = path.join(assets_folder, 'levels_maps')
        self.custom_maps = path.join(assets_folder, 'saved_maps')

        self.maps = [
            f for f in os.listdir(
                self.levels_maps) if f.endswith('.tmx')]

        super(ChooseMap, self).__init__(self.name, self.next, 'menu', '0.png', self.create_buttons_dict())

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        super().startup(dt, game_data)

        self.btns_dict = self.create_buttons_dict()
        self.btns = list()
        self.create_buttons(self.background)
        self.create_back_button(self.background, self.load_next_state, [CHARACTER_CREATION])

    def create_buttons_dict(self):
        """Create the dict for the main screen"""
        return {
            "levels": {
                "text": "Levels",
                "on_click": self.toggle_sub_state,
                "on_click_params": ['levels_maps'],
            },
            "custom_maps": {
                "text": "Custom Maps",
                "on_click": self.toggle_sub_state,
                "on_click_params": ['custom_maps'],
            },
        }

    def create_maps_buttons_dict(self):
        """Create the dict for all buttons"""
        btns_dict = dict()
        for index, game in enumerate(self.maps):
            name = game.split(".")[0]
            btns_dict[name] = {
                "text": name,
                "on_click": self.load,
                "on_click_params": [index],
            }
        return btns_dict

    def load(self, index):
        selected = self.maps[index]
        self.game_data["game_data"]["map"] = selected
        logger.debug("%s", self.game_data["game_data"]["map"])
        logger.info("Select %s", selected)
        self.next = INTRODUCTION
        super().set_state(TRANSITION_OUT)

    def toggle_sub_state(self, state):
        super().toggle_sub_state(state)
        pg.event.wait()
        if state == "levels_maps":
            self.maps = [
                f for f in os.listdir(
                    self.levels_maps) if f.endswith('.tmx')]
            self.image_screen = self.image.copy()
            self.btns_dict = self.create_maps_buttons_dict()
            self.create_back_button(self.image_screen, self.toggle_sub_state, ['normal'])
            self.btns = list()
            self.create_buttons(self.image_screen)
        elif state == 'custom_maps':
            self.maps = [
                f for f in os.listdir(
                    self.custom_maps) if f.endswith('.tmx')]
            self.image_screen = self.image.copy()
            self.btns_dict = self.create_maps_buttons_dict()
            self.create_back_button(self.image_screen, self.toggle_sub_state, ['normal'])
            self.btns = list()
            self.create_buttons(self.image_screen)
        else:
            self.btns_dict = self.create_buttons_dict()
            self.btns = list()
            self.create_buttons(self.background)
            self.create_back_button(self.background, self.load_next_state, [CHARACTER_CREATION])

    def make_states_dict(self):
        previous_dict = super().make_states_dict().copy()
        add_dict = {
            "levels_maps": self.levels_maps_run,
            "custom_maps": self.custom_maps_run,
        }
        return previous_dict | add_dict

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
        super().events_buttons(back=True)
        self.draw()

    def levels_maps_run(self):
        self.screen.blit(self.image_screen, (0, 0))
        super().events_buttons(back=True)
        super().draw_title("Levels")
        self.back_btn.draw()

    def custom_maps_run(self):
        self.screen.blit(self.image_screen, (0, 0))
        super().events_buttons(back=True)
        super().draw_title("Custom maps")
        self.back_btn.draw()

    def draw(self):
        super().draw_elements("Choose a map", back=True)
