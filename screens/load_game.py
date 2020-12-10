"""Load game screen"""

from config.buttons import WIDTH_BUTTON
import os
import json
from os import path
import pygame as pg
from logger import logger
from window import _Elements
from config.screens import GAME, LOAD_GAME, MENU, TRANSITION_OUT
from config.window import WIDTH
from config.buttons import WIDTH_BUTTON, HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON
from config.colors import GREEN_DARK, YELLOW_LIGHT, BEIGE


class LoadGame(_Elements):
    """Load game screen"""

    def __init__(self):
        self.next = GAME
        self.name = LOAD_GAME
        self.state = 'normal'

        self.selected = 0
        game_folder = path.dirname('.')
        assets_folder = path.join(game_folder, 'assets')
        self.saved_games = path.join(assets_folder, 'saved_games')

        self.games = [
            f for f in os.listdir(
                self.saved_games) if f.endswith('.json')]

        super(LoadGame, self).__init__(self.name, self.next, 'load_game', "background.jpg",
                                       self.create_buttons_dict(), btns_offset=70, btns_width=WIDTH_BUTTON + 50)

        self.delete_btns = list()
        self.create_delete_buttons()
        self.create_back_button(self.background, self.load_next_state, [MENU])

    def create_delete_buttons(self):
        """Create delete btn"""
        _x = WIDTH // 2 + WIDTH_BUTTON
        y_base = 250
        logger.info("Create delete buttons")
        for index, (_, value) in enumerate(self.create_delete_buttons_dict().items()):
            self.delete_btns.append(self.create_button(
                self.background,
                _x,
                y_base + index * 70,
                50,
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

    def create_delete_buttons_dict(self):
        """"Create dict for the delete button"""
        btns_dict = dict()
        for index, _ in enumerate(self.games):
            btns_dict[index] = {
                "text": "X",
                "on_click": self.delete,
                "on_click_params": [index],
            }
        return btns_dict

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

    def delete(self, num):
        """Delete a file using the num

        Args:
            num (int)
        """
        file_name = self.games[num]
        file_path = path.join(self.saved_games, file_name)
        if path.exists(file_path):
            os.remove(file_path)
            logger.info("Remove the file %s", file_path)
        else:
            logger.error("The file %s doesn't existe", file_path)

        minimap_types = ["cover", "fog"]
        for _type in minimap_types:
            name = file_name.split('.json')[0]
            name_path = path.join(self.saved_minimap, f"{name}-{_type}.png")
            if path.exists(name_path):
                os.remove(name_path)
                logger.info("Remove the file %s", name_path)
            else:
                logger.error("The file %s doesn't existe", name_path)

        pg.event.wait()
        self.refresh()

    def refresh(self):
        """Refresh the list"""
        self.background = self.image.copy()
        self.games = [
            f for f in os.listdir(
                self.saved_games) if f.endswith('.json')]

        self.delete_btns = list()
        self.create_delete_buttons()

        self.create_back_button(self.background, self.load_next_state, [MENU])

        self.btns_dict = self.create_buttons_dict()
        self.create_buttons(self.background, offset=70)

        logger.info("Refresh the info")

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
        self.events_delete_btns()
        self.draw()

    def events_delete_btns(self):
        """Listen for delete btns"""
        events = pg.event.get()
        for btn in self.delete_btns:
            btn.listen(events)

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
            file_name = f"{file_name}-{minimap_type}.png"
            self.game_data["minimap"][minimap_type] = pg.image.load(
                path.join(self.saved_minimap, file_name)).convert_alpha()
            logger.info("Load the minimap %s", file_name)

    def draw(self):
        """Draw loading page"""
        super().draw_elements("Load a game", back=True)
        self.draw_text("Delete", self.text_font, 26, BEIGE, WIDTH // 2 + WIDTH_BUTTON + 25, 230, align="s")
        for btn in self.delete_btns:
            btn.draw()
