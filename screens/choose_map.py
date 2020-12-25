"""Menu screen"""

from config.window import HEIGHT, WIDTH
import pygame as pg
from window import _Elements
from config.screens import BACKGROUND_MENU, CHOOSE_MAP, CREDITS, GAME, INTRODUCTION, MENU, NEW_GAME, OPTIONS, LOAD_GAME, TRANSITION_IN, TRANSITION_OUT
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

        self.maps = [
            f for f in os.listdir(
                self.levels_maps) if f.endswith('.tmx')]

        super(ChooseMap, self).__init__(self.name, self.next, 'menu', '0.png', self.create_buttons_dict())

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        btns_dict = dict()
        for index, game in enumerate(self.maps):
            name = game.split(".")[0]
            btns_dict[name] = {
                "text": name,
                "on_click": self.load,
                "on_click_params": [index],
            }  # sur l'action, il faut ajouter le nom de la map dans le game data, la save et passer à l'écran suivant
        return btns_dict

    def load(self, index):
        selected = self.maps[index]
        self.game_data["game_data"]["map"] = selected
        logger.info("Select %s", selected)
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
        super().events_buttons()
        self.draw()

    def draw(self):
        """Draw content"""
        super().draw_elements("Choose a map")
