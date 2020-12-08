"""Load game screen"""

from config.buttons import WIDTH_BUTTON
import os
import json
from os import path
import pygame as pg
from logger import logger
from window import _Elements
from config.screens import GAME, LOAD_GAME, MENU, TRANSITION_OUT


class LoadGame(_Elements):
    """Load game screen"""

    def __init__(self):
        self.next = GAME
        self.name = LOAD_GAME
        self.state = 'normal'

        self.selected = 0
        game_folder = path.dirname('.')
        assets_folder = path.join(game_folder, 'assets')
        saved_games = path.join(assets_folder, 'saved_games')

        self.games = [
            f for f in os.listdir(
                saved_games) if f.endswith('.json')]

        super(LoadGame, self).__init__(self.name, self.next, 'load_game', "background.jpg",
                                       self.create_buttons_dict(), btns_offset=70, btns_width=WIDTH_BUTTON + 50)

        self.create_back_button(self.background, self.load_next_state, [MENU])

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        btns_dict = dict()
        for index, game in enumerate(self.games):
            name = game.split(".")[0]
            btns_dict[name] = {
                "text": name,
                "on_click": self.load,
                "on_click_params": [index],
            }
        return btns_dict

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

    def load(self, index):
        """Load the selected files

        Args:
            selected (string): name of the file
        """
        selected = self.games[index]
        try:
            with open(path.join(self.saved_games, selected)) as f:
                self.game_data['game_data'] = json.load(f)
                self.game_data['file_name'] = selected
                super().set_state(TRANSITION_OUT)
                logger.info('Load : %s', selected)
        except EnvironmentError as e:
            logger.exception(e)

        try:
            self.load_minimap()
        except EnvironmentError as e:
            logger.exception(e)

    def load_minimap(self):
        """Load images to create the fog of war"""
        minimap_types = ['cover', 'fog']
        self.game_data["minimap"] = {"fog": None, "cover": None}
        file_name = self.game_data["file_name"].split(".json")[0]
        for minimap_type in minimap_types:
            self.game_data["minimap"][minimap_type] = pg.image.load(
                path.join(self.saved_minimap, f"{file_name}-{minimap_type}.png")).convert_alpha()

    def draw(self):
        """Draw loading page"""
        super().draw_elements("Load a game", back=True)
