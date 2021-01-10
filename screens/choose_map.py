"""Menu screen"""

from config.buttons import WIDTH_BUTTON
from config.window import HEIGHT, WIDTH
import pygame as pg
from window import _Elements
from config.screens import BACKGROUND_MENU, CHARACTER_CREATION, CHOOSE_MAP, CREDITS, GAME, INTRODUCTION, MENU, NEW_GAME, OPTIONS, LOAD_GAME, TRANSITION_IN, TRANSITION_OUT
from config.colors import BEIGE,YELLOW_LIGHT,GREEN_DARK
from config.buttons import WIDTH_BUTTON, HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON
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
        self.random_maps = path.join(assets_folder,'saved_generated')

        self.type_maps = None

        self.maps = [
            f for f in os.listdir(
                self.levels_maps) if f.endswith('.tmx')]
        
        self.maps_generated = [
            f for f in os.listdir(
                self.random_maps) if f.endswith('.tmx')]
        
        

        super(ChooseMap, self).__init__(self.name, self.next, 'menu', '0.png', self.create_buttons_dict())

        self.states_dict = self.make_states_dict()

    def startup(self, dt, game_data):
        super().startup(dt, game_data)

        self.btns_dict = self.create_buttons_dict()
        self.btns = list()
        self.create_buttons(self.background, width=WIDTH_BUTTON + 50)
        self.create_back_button(self.background, self.load_next_state, [CHARACTER_CREATION])

    def all_events(self, events):
        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.load_next_state(CHARACTER_CREATION)

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
            "random_maps": {
                "text": "Random Maps",
                "on_click": self.toggle_sub_state,
                "on_click_params": ['saved_generated'],
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

    def create_delete_buttons(self):
        """Create delete btn"""
        _x = WIDTH // 2 + WIDTH_BUTTON
        y_base = 250
        logger.info("Create delete buttons")
        for index, (_, value) in enumerate(self.create_delete_buttons_dict().items()):
            self.delete_btns.append(self.create_button(
                self.image_screen,
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
        for index, _ in enumerate(self.maps_generated):
            btns_dict[index] = {
                "text": "X",
                "on_click": self.delete,
                "on_click_params": [index],
            }
        return btns_dict

    def delete(self, num):
        """Delete a file using the num

        Args:
            num (int)
        """
        file_name = self.maps_generated[num]
        file_path = path.join(self.random_maps, file_name)
        if path.exists(file_path):
            os.remove(file_path)
            logger.info("Remove the file %s", file_path)
        else:
            logger.error("The file %s doesn't existe", file_path)

        pg.event.wait()
        self.refresh()
    
    def refresh(self):
        """Refresh the list"""
        self.image_screen = self.image.copy()
        self.maps_generated = [
            f for f in os.listdir(
                self.random_maps) if f.endswith('.tmx')]

        self.maps = self.maps_generated
               



        self.create_back_button(self.image_screen, self.toggle_sub_state, ['normal'])

        self.btns_dict = self.create_maps_buttons_dict()
        self.create_buttons(self.image_screen, offset=70, width=WIDTH_BUTTON + 50)
        
        
        self.delete_btns = list()
        self.create_delete_buttons()

        logger.info("Refresh the info")

    def load(self, index):
        selected = self.maps[index]
        self.game_data["game_data"]["map"] = {
            "filename": selected,
            "folder": self.type_maps
        }
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
            self.type_maps = "levels_maps"
            self.btns = list()
            self.create_buttons(self.image_screen, width=WIDTH_BUTTON + 50)
        elif state == 'custom_maps':
            self.maps = [
                f for f in os.listdir(
                    self.custom_maps) if f.endswith('.tmx')]
            self.image_screen = self.image.copy()
            self.btns_dict = self.create_maps_buttons_dict()
            self.create_back_button(self.image_screen, self.toggle_sub_state, ['normal'])
            self.type_maps = "saved_maps"
            self.btns = list()
            self.create_buttons(self.image_screen, width=WIDTH_BUTTON + 50)
        elif state == 'saved_generated':
            self.maps = [
                f for f in os.listdir(
                    self.random_maps) if f.endswith('.tmx')]
            self.image_screen = self.image.copy()
            self.btns_dict = self.create_maps_buttons_dict()
            self.create_back_button(self.image_screen, self.toggle_sub_state, ['normal'])
            self.type_maps = "saved_generated"
            self.btns = list()
            self.create_buttons(self.image_screen, width=WIDTH_BUTTON + 50)
            self.delete_btns = list()
            self.create_delete_buttons()
        else:
            self.btns_dict = self.create_buttons_dict()
            self.btns = list()
            self.create_buttons(self.background, width=WIDTH_BUTTON + 50)
            self.create_back_button(self.background, self.load_next_state, [CHARACTER_CREATION])

    def make_states_dict(self):
        previous_dict = super().make_states_dict().copy()
        add_dict = {
            "levels_maps": self.levels_maps_run,
            "custom_maps": self.custom_maps_run,
            "saved_generated": self.random_maps_run,
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

    def random_maps_run(self):
        for btn in self.delete_btns:
            btn.draw()
        self.screen.blit(self.image_screen, (0, 0))
        super().events_buttons(back=True)
        super().draw_title("Random Maps")
        self.back_btn.draw()
        self.draw_text("Delete", self.text_font, 26, BEIGE, WIDTH // 2 + WIDTH_BUTTON + 25, 230, align="s")
        self.events_delete_btns()

        

    def events_delete_btns(self):
        """Listen for delete btns"""
        events = pg.event.get()
        for btn in self.delete_btns:
            btn.listen(events)


    def draw(self):
        super().draw_elements("Choose a map", back=True)
