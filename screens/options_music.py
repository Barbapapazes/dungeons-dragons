"""Menu screen"""

import pygame as pg
from window import _Elements
from config.screens import GAME, MENU, NEW_GAME, OPTIONS, LOAD_GAME,OPTIONS_MUSIC
from utils.shortcuts import load_shortcuts
from data.music_data import DATA_MUSIC
from logger import logger
from config.buttons import HEIGHT_BUTTON, MARGIN_BUTTON, RADIUS_BUTTON, HEIGHT_SLIDER, WIDTH_BUTTON, WIDTH_SLIDER
from components.cursor import Cursor
from config.window import WIDTH, HEIGHT
from config.colors import LIGHTGREY, YELLOW_LIGHT, BLACK, BEIGE, GREEN_DARK, WHITE


class Options_music(_Elements):
    """Menu screen"""

    def __init__(self):
        self.name = OPTIONS_MUSIC
        self.next = None
        print(DATA_MUSIC["is_enable"])
        super(Options_music, self).__init__(self.name, self.next, 'options', 'background.jpg', self.create_buttons_dict())
        self.create_back_button(self.background, self.load_next_state, [OPTIONS])
        self.create_sliders()
        self.startup(0, load_shortcuts())

    def create_buttons_dict(self):
        """Create the dict for all buttons"""
        return {
            "song": {
                "text": "Song : On /Off ",
                "on_click": self.status_music,
                "on_click_params": "1",
            },
            "sound": {
                "text": "Sound : On/Off",
                "on_click": self.status_music,
                "on_click_params": "1",
            },
        }
    
    def create_sliders_dict(self):
        """Create the dict for all sliders

        Returns:
            dict
        """
        return {
            "Music": {
                "name": "str",
                "max": 3,
                "start": 2,
            },
            "Sound": {
                "name": "dex",
                "max": 3,
                "start": 2,
            },
        }

    def create_sliders(self):
        """Create sliders"""
        self.sliders = list()
        logger.info("Create all sliders from character creation")
        for index, (key, value) in enumerate(
                self.create_sliders_dict().items()):
            x = 0
            y = 6 * HEIGHT // 10 + (index % 3) * 70
            if index in [0, 1, 2]:
                x = 13 * WIDTH // 20
            else:
                x = 1 * WIDTH // 20
            self.sliders.append(
                self.create_slider(
                    key.upper(),
                    "None",
                    x,
                    y,
                    WIDTH_SLIDER,
                    HEIGHT_SLIDER,
                    self.background,
                    0,
                    100,
                    1,
                    value["start"],
                    self.text_font,
                    self.draw_text, BLACK, LIGHTGREY

                ))
    
    def status_music(self,none):
        if(DATA_MUSIC["is_enable"]):
            DATA_MUSIC["is_enable"]=False
            DATA_MUSIC["current_playing"]=None
            logger.info("Musique false")
        else:
            DATA_MUSIC["is_enable"]=True
            DATA_MUSIC["current_playing"]=None
            logger.info("Musique true")
        self.create_buttons_dict()
        self.load_next_state(OPTIONS_MUSIC)
        

    def run(self, surface, keys, mouse, dt):
        """Run states"""
        self.screen = surface
        self.keys = keys
        self.mouse = mouse
        self.dt = dt
        update_level = self.states_dict[self.state]
        if self.state != 'normal':
            self.draw()
            self.back_btn.draw()
        update_level()

    def normal_run(self):
        """Run the normal state"""
        super().events_buttons(back=True)
        self.events_sliders()
        self.update()
        self.draw()

    def update(self):
        """Update the content"""
        for slider in self.sliders:
            slider.update()


    def draw_sliders(self):
        """Draw sliders"""
        for slider in self.sliders:
            slider.draw_without_text()
    
    def events_sliders(self):
        """Events for sliders"""
        events = pg.event.get()
        for slider in self.sliders:
            slider.listen(events)

    def draw(self):
        """Draw content"""
        super().draw_elements("Options")
        super().draw_subtitle("Musics & Sounds")
        self.draw_sliders()

    @staticmethod
    def stop_window():
        """Quit the window using a user event"""
        quit_event = pg.event.Event(pg.USEREVENT, code="_State", name="quit")
        pg.event.post(quit_event)

    @staticmethod
    def create_slider(
            title,
            name,
            x,
            y,
            width,
            height,
            surface,
            min,
            max,
            step,
            start,
            font,
            draw_text, color, handle_color):
        """Create a slider

        Args:
            title (str)
            name (str)
            x (int)
            y (int)
            width (int)
            height (int)
            surface (Surface)
            min (int)
            max (int)
            step (int)
            start (int)
            font (str)
            draw_text (func)
            color (tuple)
            handle_color (tuple)

        Returns:
            Cursor
        """
        return Cursor(
            title,
            name,
            x,
            y,
            width,
            height,
            surface,
            min,
            max,
            step,
            start,
            font,
            draw_text, color, handle_color)