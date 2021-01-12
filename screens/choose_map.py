"""Menu screen"""

import os
from os import path

import pygame as pg
from components.cursor import Cursor
from config.buttons import (HEIGHT_BUTTON, HEIGHT_SLIDER, MARGIN_BUTTON,
                            RADIUS_BUTTON, WIDTH_BUTTON, WIDTH_SLIDER)
from config.colors import BEIGE, GREEN_DARK, YELLOW_LIGHT
from config.screens import (CHARACTER_CREATION, CHOOSE_MAP, INTRODUCTION,
                            TRANSITION_OUT)
from config.window import WIDTH, HEIGHT
from logger import logger
from pygame_widgets import TextBox
from utils.random_map import generate_map
from window import _Elements


class ChooseMap(_Elements):
    """ChooseMap screen"""

    def __init__(self):
        self.name = CHOOSE_MAP
        self.next = INTRODUCTION

        game_folder = path.dirname('.')
        assets_folder = path.join(game_folder, 'assets')
        self.levels_maps = path.join(assets_folder, 'levels_maps')
        self.custom_maps = path.join(assets_folder, 'saved_maps')
        self.random_maps = path.join(assets_folder, 'saved_generated')

        self.type_maps = None

        self.maps = [
            f for f in os.listdir(
                self.levels_maps) if f.endswith('.tmx')]

        self.maps_generated = [
            f for f in os.listdir(
                self.random_maps) if f.endswith('.tmx')]

        super(ChooseMap, self).__init__(self.name, self.next, 'menu', '0.png', self.create_buttons_dict())

        self.background = pg.Surface((WIDTH, HEIGHT))
        image = pg.image.load(
            path.join(
                self.img_folder,
                'menu',
                '0.png')).convert()
        self.image = pg.transform.scale(image, (WIDTH, HEIGHT))
        self.image_screen = self.image.copy()

        self.states_dict = self.make_states_dict()
        self.size_map_width = 6
        self.size_map_height = 6

    def startup(self, dt, game_data):
        super().startup(dt, game_data)

        self.btns_dict = self.create_buttons_dict()
        self.btns = list()
        self.create_buttons(self.image_screen, width=WIDTH_BUTTON + 50)
        self.create_back_button(self.image_screen, self.load_next_state, [CHARACTER_CREATION])

    def all_events(self, events):
        if self.state == "saved_generated":
            self.map_name.listen(events)
            self.button_generate.listen(events)
            self.events_delete_btns(events)
            self.events_sliders(events)
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

    def create_button_generated_map(self):
        bt = self.create_button(
            self.image_screen,
            100,
            500,
            150,
            HEIGHT_BUTTON,
            "generated",
            self.button_font,
            self.fontsize,
            MARGIN_BUTTON,
            RADIUS_BUTTON,
            BEIGE,
            YELLOW_LIGHT,
            GREEN_DARK,
            self.generate,
            []

        )
        return bt

    def generate(self):
        for slider in self.sliders:
            if slider.name == "width":
                self.size_map_width = slider.getValue()
            elif slider.name == "height":
                self.size_map_height = slider.getValue()
        logger.info("Generate random map...")
        if self.map_name.getText() == '':
            generate_map(self.size_map_height, self.size_map_width)
        else:
            _path = path.join(self.random_maps, self.map_name.getText() + '.tmx')
            generate_map(self.size_map_height, self.size_map_width, _path)
        logger.info("Map is generated !")
        self.refresh()

    def create_slider(self, x, y, name):
        return Cursor(
            name,
            name,
            x,
            y,
            WIDTH_SLIDER,
            HEIGHT_SLIDER,
            self.background,
            1,
            30,
            1,
            1,
            self.text_font,
            self.draw_text, GREEN_DARK, YELLOW_LIGHT)

    def create_sliders_for_size_map(self):
        return [
            self.create_slider(100, 200, "height"),
            self.create_slider(100, 300, "width")
        ]

    def create_name_box(self):
        self.map_name = TextBox(
            self.background,
            70,
            400,
            WIDTH_BUTTON,
            HEIGHT_BUTTON,
            fontsize=50,
            color=GREEN_DARK,
            textColour=GREEN_DARK,
            onSubmit=self.getmap_name,
            radius=10,
            borderThickness=4

        )

    def getmap_name(self):
        return self.map_name.getText()

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
        self.create_button_generated_map().draw()

        self.delete_btns = list()
        self.create_delete_buttons()

        self.sliders = self.create_sliders_for_size_map()
        self.draw_sliders()
        self.create_name_box()

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
        pg.event.clear()
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
            self.button_generate = self.create_button_generated_map()
            self.sliders = self.create_sliders_for_size_map()
            self.create_name_box()

        else:
            self.image_screen = self.image.copy()
            self.btns_dict = self.create_buttons_dict()
            self.btns = list()
            self.create_buttons(self.image_screen, width=WIDTH_BUTTON + 50)
            self.create_back_button(self.image_screen, self.load_next_state, [CHARACTER_CREATION])

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
        self.screen.blit(self.background, (0, 0))
        self.background.blit(self.image_screen, (0, 0))
        super().events_buttons(back=True)
        super().draw_title("Random Maps")
        self.draw_random_maps()

    def draw_random_maps(self):
        self.draw_sliders()
        self.map_name.draw()
        self.back_btn.draw()
        self.draw_text("Delete", self.text_font, 26, BEIGE, WIDTH // 2 + WIDTH_BUTTON + 25, 230, align="s")
        self.button_generate.draw()
        self.draw_buttons()
        for btn in self.delete_btns:
            btn.draw()

    def draw_sliders(self):
        for slider in self.sliders:
            slider.draw()

    def events_sliders(self, events):
        """Events for sliders"""
        for slider in self.sliders:
            slider.listen(events)

    def events_delete_btns(self, events):
        """Listen for delete btns"""
        for btn in self.delete_btns:
            btn.listen(events)

    def draw(self):
        if self.state != "saved_generated":
            self.screen.blit(self.background, (0, 0))
            self.background.blit(self.image_screen, (0, 0))
            super().draw_elements("Choose a map", back=True, background=False)
